"""
test_spanner.py
Manual test script for both RAG and Graph RAG pipelines.

Usage:
    python -m src.test_spanner
"""

import traceback
from rag_pipeline import build_rag_chain, build_graph_chain


def test_rag_and_graph():
    """Run both RAG and Graph RAG tests using the same question."""
    # Define one shared question for both tests
    question = "I am looking for a beginner drone. Please give me some recommendations."

    print("🚀 Running RAG and Graph chain tests with the same question...\n")
    print(f"📝 Question: {question}\n")

    # --- Test RAG chain ---
    try:
        print("🧠 === Testing build_rag_chain() ===")
        chain = build_rag_chain()
        response_rag = chain.invoke(question)
        print("\n✅ RAG Chain Response:\n")
        print(response_rag)
    except Exception as e:
        print("\n❌ RAG Chain test failed!")
        traceback.print_exc()

    # --- Test Graph chain ---
    try:
        print("\n🔗 === Testing build_graph_chain() ===")
        response_graph = build_graph_chain(question)
        print("\n✅ Graph Chain Response:\n")
        print(response_graph)
    except Exception as e:
        print("\n❌ Graph Chain test failed!")
        traceback.print_exc()

    print("\n🎯 All tests completed.\n")


if __name__ == "__main__":
    test_rag_and_graph()
