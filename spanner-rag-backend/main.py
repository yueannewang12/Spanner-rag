# main.py
import textwrap
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from rag_pipeline import run_graph_chain, build_rag_chain

# Global in-memory cache for blazing fast demos
demo_cache_graph = {}
demo_cache_rag = {}

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
    allow_headers=["*"],     # Cloud Run adds custom headers
)

@app.get("/health")
def health():
    return {"status": "ok"}


# ======================================================
# GRAPH RAG  (run_graph_chain(question) → returns string)
# ======================================================
@app.post("/predict_graph")
async def predict_graph(request: Request):
    body = await request.json()

    instances = body.get("instances")
    if instances:
        question = instances[0].get("question") or instances[0].get("query")
    else:
        question = body.get("question") or body.get("query")

    try:
        # 1. Check if we already answered this exact question
        if question in demo_cache_graph:
            print(f"⚡ [CACHE HIT] Returning fake 4s graph answer for: {question}")
            await asyncio.sleep(4)  # Artificial 4-second demo delay
            return {"answer": textwrap.fill(str(demo_cache_graph[question]), width=80)}

        # 2. Graph builder already runs and returns a string
        # Run synchronously blocking code in a background thread
        answer = await asyncio.to_thread(run_graph_chain, question)

        if not answer:
            answer = "No Graph RAG answer was generated."

        # 3. Save to cache for the literal zero-latency next request
        demo_cache_graph[question] = answer

        return {"answer": textwrap.fill(str(answer), width=80)}
    except Exception as e:
        return {"error": f"Graph RAG error: {str(e)}"}


# ======================================================
# TRADITIONAL RAG (build_rag_chain() → returns Runnable)
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
        # 1. Check if we already answered this exact question
        if question in demo_cache_rag:
            print(f"⚡ [CACHE HIT] Returning fake 4s traditional answer for: {question}")
            await asyncio.sleep(4)  # Artificial 4-second demo delay
            return {"answer": textwrap.fill(str(demo_cache_rag[question]), width=80)}

        # 2. Run synchronously blocking code in a background thread
        result = await asyncio.to_thread(rag_chain.invoke, question)

        # Some chains return dicts, some strings
        if isinstance(result, dict) and "answer" in result:
            answer = result["answer"]
        else:
            answer = result

        if not answer:
            answer = "No Traditional RAG answer was generated."

        # 3. Save to cache for next time
        demo_cache_rag[question] = answer

        return {"answer": textwrap.fill(str(answer), width=80)}
    except Exception as e:
        return {"error": f"RAG error: {str(e)}"}


# ======================================================
# Unified /predict endpoint (optional, for Vertex AI)
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
# ======================================================
@app.post("/query/rag")
async def query_rag(request: Request):
    return await predict_rag(request)

@app.post("/query/graph")
async def query_graph(request: Request):
    return await predict_graph(request)
