# app.py
import textwrap
from fastapi import FastAPI, Request
# Import the builders, but DO NOT call them here
from rag_pipeline import build_graph_chain, build_rag_chain

app = FastAPI()

# --- ❌ DO NOT initialize chains here. This causes crashes. ---
# graph_chain = build_graph_chain() 
# rag_chain = build_rag_chain()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict_graph")
async def predict_graph(request: Request):
    # ✅ Initialize INSIDE the function (Lazy Loading)
    graph_chain = build_graph_chain()
    
    body = await request.json()
    # Handle Vertex AI "instances" wrapper
    instances = body.get("instances")
    if instances:
        question = instances[0].get("question")
    else:
        question = body.get("question")

    try:
        answer = graph_chain.invoke({
            "question": question,
            "graph_schema": "Schema omitted for brevity",
            "context": "" 
        })
        return {"predictions": [textwrap.fill(answer, width=80)]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict_rag")
async def predict_rag(request: Request):
    # ✅ Initialize INSIDE the function
    rag_chain = build_rag_chain()

    body = await request.json()
    instances = body.get("instances")
    if instances:
        question = instances[0].get("question")
    else:
        question = body.get("question")

    try:
        answer = rag_chain.invoke(question)
        return {"predictions": [textwrap.fill(answer, width=80)]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict")
async def predict(request: Request):
    """
    Unified endpoint for Vertex AI.
    """
    body = await request.json()
    
    # Check for "mode" to route traffic
    instances = body.get("instances", [{}])
    mode = instances[0].get("mode") or body.get("mode", "rag")
    
    if mode == "graph":
        return await predict_graph(request)
    else:
        return await predict_rag(request)

