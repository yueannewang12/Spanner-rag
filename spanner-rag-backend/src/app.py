# app.py
import textwrap
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from rag_pipeline import build_graph_chain, build_rag_chain

app = FastAPI()

# ---------- CORS: Allow both frontend domains ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://graph-rag-bf64d.web.app",
        "https://graphrag.gcp.tomtomkaka.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],     # POST, GET, OPTIONS...
    allow_headers=["*"],     # Cloud Run requires this
)

@app.get("/health")
def health():
    return {"status": "ok"}


# ======================================================
# GRAPH RAG
#   - build_graph_chain(question) returns a STRING, not a chain
# ======================================================
@app.post("/predict_graph")
async def predict_graph(request: Request):
    body = await request.json()

    # Support both { "question": "..." } and { "query": "..." }
    instances = body.get("instances")
    if instances:
        question = instances[0].get("question") or instances[0].get("query")
    else:
        question = body.get("question") or body.get("query")

    try:
        # Graph chain builder ALREADY runs and returns an answer string
        answer = build_graph_chain(question)

        if not answer:
            answer = "No Graph RAG answer was generated."

        return {"answer": textwrap.fill(str(answer), width=80)}
    except Exception as e:
        return {"error": f"Graph RAG error: {str(e)}"}


# ======================================================
# TRADITIONAL RAG
#   - build_rag_chain() returns a Runnable (chain)
# ======================================================
@app.post("/predict_rag")
async def predict_rag(request: Request):
    body = await request.json()

    instances = body.get("instances")
    if instances:
        question = instances[0].get("question") or instances[0].get("query")
    else:
        question = body.get("question") or body.get("query")

    rag_chain = build_rag_chain()

    try:
        result = rag_chain.invoke(question)

        # May be dict or string depending on chain
        if isinstance(result, dict) and "answer" in result:
            answer = result["answer"]
        else:
            answer = result

        if not answer:
            answer = "No Traditional RAG answer was generated."

        return {"answer": textwrap.fill(str(answer), width=80)}
    except Exception as e:
        return {"error": f"RAG error: {str(e)}"}


# ======================================================
# Unified endpoint (optional)
# ======================================================
@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    instances = body.get("instances", [{}])

    mode = instances[0].get("mode") or body.get("mode", "rag")

    if mode == "graph":
        return await predict_graph(request)
    else:
        return await predict_rag(request)


# ======================================================
# Alias endpoints for your React frontend
# /query/rag       /query/graph
# ======================================================
@app.post("/query/rag")
async def query_rag(request: Request):
    return await predict_rag(request)

@app.post("/query/graph")
async def query_graph(request: Request):
    return await predict_graph(request)
