import os
import textwrap
from google.cloud import spanner
from langchain_google_spanner import (
    SpannerGraphStore,
    SpannerVectorStore,
    SpannerGraphVectorContextRetriever,
)
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# === Configuration ===
os.environ["SPANNER_PROJECT_ID"] = "anne-test-project1"
os.environ["GOOGLE_CLOUD_PROJECT"] = "anne-test-project1"

PROJECT_ID = "anne-test-project1"
INSTANCE = "properties"
DATABASE = "graph-rag-colab"
GRAPH_NAME = "my_graph"
TABLE_NAME = "my_conventional_rag"

# === Global Components ===
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")
llm = ChatVertexAI(model="gemini-2.0-flash", temperature=0)

# === Lazy Loading Cache ===
_cached_graph_chain = None
_cached_rag_chain = None
_cached_graph_retriever = None
_cached_graph_schema = None


# ------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------
def format_docs(docs):
    """Safely flatten retrieved document objects or lists into plain text."""
    if not docs:
        return ""
    if isinstance(docs, list):
        return "\n\n".join(
            getattr(d, "page_content", str(d))
            for d in docs
            if hasattr(d, "page_content") or isinstance(d, str)
        )
    return str(docs)


def wrap_answer(text, width=100):
    """Pass through string unmodified so Markdown formatting is preserved."""
    return text.strip() if text else ""


# ------------------------------------------------------------
# GRAPH RAG CHAIN
# ------------------------------------------------------------
def run_graph_chain(question: str = "What are good beginner drones?"):
    """Executes a graph-based RAG chain and returns a formatted answer."""
    global _cached_graph_chain
    global _cached_graph_retriever
    global _cached_graph_schema

    if _cached_graph_retriever is None:
        print(f"🔄 Initializing Spanner Graph connection for project: {PROJECT_ID}...")
        spanner.Client(project=PROJECT_ID)

        # Initialize graph store
        graph_store = SpannerGraphStore(
            instance_id=INSTANCE,
            database_id=DATABASE,
            graph_name=GRAPH_NAME,
        )
        _cached_graph_schema = graph_store.get_schema
        
        embedding_service = VertexAIEmbeddings(model_name="text-embedding-004")
        _cached_graph_retriever = SpannerGraphVectorContextRetriever.from_params(
            graph_store=graph_store,
            embedding_service=embedding_service,
            label_expr="Product",
            expand_by_hops=1,
            top_k=3,
            k=50,
        )
        print("✅ Spanner Graph retriever initialized.")

    # --- Updated Prompt Template ---
    SPANNERGRAPH_QA_TEMPLATE = """
You are a helpful and friendly AI assistant for question answering tasks for an electronics retail online store.

Create a beautifully formatted Markdown answer for the question.
You should only use the information provided in the context and not use your internal knowledge.
Don't add any information.

Format your answer with bolding and bullet-point lists when listing features, bundles, or accessories.
Always use line breaks and Markdown lists (*) for multiple items to make it highly readable.

You are given the following information:
- `Question`: the natural language question from the user
- `Graph Schema`: contains the schema of the graph database
- `Context`: The response from the graph database as context. The context has nodes and edges. Use the relationships.
Information:
Question: {question}
Graph Schema: {graph_schema}
Context: {context}

Helpful Answer:
    """

    graph_prompt = PromptTemplate(
        template=SPANNERGRAPH_QA_TEMPLATE,
        input_variables=["question", "graph_schema", "context"],
    )

    llm_local = ChatVertexAI(model="gemini-2.0-flash", temperature=0)

    if _cached_graph_chain is None:
        _cached_graph_chain = graph_prompt | llm_local | StrOutputParser()
        print("✅ Spanner Graph chain initialized.")

    # ---------------------------
    # Retrieve graph node context
    # ---------------------------
    print("🔍 Retrieving graph node context ...")
    context_docs = _cached_graph_retriever.invoke(question)
    context_text = format_docs(context_docs)
    preview = context_text[:500] + ("..." if len(context_text) > 500 else "")
    print(f"📄 Retrieved context (preview):\\n{textwrap.fill(preview, width=100)}\\n")

    # Run the graph chain
    print("🤖 Generating answer ...")
    answer_raw = _cached_graph_chain.invoke(
        {
            "question": question,
            "graph_schema": _cached_graph_schema,
            "context": context_text,
        }
    )

    # Format / wrap the answer
    answer = wrap_answer(answer_raw)
    print(answer)

    return answer


# ------------------------------------------------------------
# VECTOR RAG CHAIN
# ------------------------------------------------------------
def build_rag_chain():
    """Builds and caches a text-based RAG chain (standard retrieval)."""
    global _cached_rag_chain

    if _cached_rag_chain is None:
        print(f"🔄 Initializing Spanner Vector connection for project: {PROJECT_ID}...")
        spanner.Client(project=PROJECT_ID)

        vector_store = SpannerVectorStore(
            instance_id=INSTANCE,
            database_id=DATABASE,
            table_name=TABLE_NAME,
            embedding_service=embeddings,
        )

        vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        conv_prompt = PromptTemplate(
            template="""
            You are a friendly digital shopping assistant.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know.

            Question: {question}
            Context: {context}
            Answer:
            """,
            input_variables=["context", "question"],
        )

        _cached_rag_chain = (
            {"context": vector_retriever, "question": RunnablePassthrough()}
            | conv_prompt
            | llm
            | StrOutputParser()
        )
        print("✅ Spanner Vector chain initialized.")

    return _cached_rag_chain
