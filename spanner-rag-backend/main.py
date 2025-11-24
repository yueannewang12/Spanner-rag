from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag_pipeline import build_rag_chain, build_graph_chain
import logging


# ------------------------------------------------------------
# Initialize FastAPI app
# ------------------------------------------------------------
app = FastAPI()

# ------------------------------------------------------------
# Enable CORS (allow your Firebase frontend)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://graph-rag-bf64d.web.app",  # ✅ your live Firebase site
        "http://localhost:3000"             # ✅ optional: local React testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging (Cloud Run friendly)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------
# Request model
# ------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str


# ------------------------------------------------------------
# Health check endpoint
# ------------------------------------------------------------
@app.get("/")
def health_check():
    """Simple endpoint for Cloud Run health checks."""
    return {"status": "ok"}


# ------------------------------------------------------------
# Standard RAG endpoint (Spanner Vector RAG)
# ------------------------------------------------------------
@app.post("/query/rag")
async def query_rag(req: QueryRequest):
    """
    Runs the standard vector-based RAG chain.
    Uses Spanner vector retrieval and Vertex AI for response generation.
    """
    logger.info(f"[RAG] Received query: {req.query}")

    try:
        chain = build_rag_chain()
        response = chain.invoke(req.query)
        logger.info(f"[RAG] Response: {response}")
        return {"type": "rag", "answer": response}

    except Exception as e:
        logger.exception(f"[RAG] Error processing query: {e}")
        return {"error": str(e)}


# ------------------------------------------------------------
# Graph RAG endpoint (Spanner Graph)
# ------------------------------------------------------------
@app.post("/query/graph")
async def query_graph(req: QueryRequest):
    """
    Runs the graph-based RAG chain.
    Combines Spanner Graph schema + node context + Vertex AI.
    """
    logger.info(f"[GRAPH] Received query: {req.query}")

    try:
        # build_graph_chain already executes and returns the answer string
        response = build_graph_chain(req.query)
        logger.info(f"[GRAPH] Response: {response}")
        return {"type": "graph", "answer": response}

    except Exception as e:
        logger.exception(f"[GRAPH] Error processing query: {e}")
        return {"error": str(e)}
