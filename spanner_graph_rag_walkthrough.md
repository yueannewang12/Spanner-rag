# Spanner Graph RAG vs. Traditional RAG Showcase

## Overview
This repository serves as a functional, side-by-side demonstration of the structural and conceptual differences between **Traditional Vector RAG** (Retrieval-Augmented Generation) and **Graph RAG**. 

It specifically leverages **Google Cloud Spanner** to showcase how traversing a relational graph yields significantly different, often superior structural context for Large Language Models (LLMs) compared to indiscriminately querying massive unstructured text paragraphs over standard vector databases.

### Core Technologies Used
* **Database**: Google Cloud Spanner (Graph & Vector representations)
* **Embeddings**: Vertex AI `text-embedding-004`
* **LLM**: Vertex AI `gemini-2.0-pro` / `gemini-2.0-flash`
* **Backend**: Python FastAPI deployed on Cloud Run
* **Frontend**: React deployed on Firebase Hosting

## How the Architecture Works 

### 1. Traditional RAG (The "Unstructured Text" Approach)
* **Mechanic**: The system uses a `SpannerVectorStore` to perform mathematical similarity searches across standard text blob columns.
* **Outcome**: It acts like a brochure. The system searches for keywords (e.g., "cost-effective SSD") and retrieves explicit paragraphs containing those exact attributes. It's fantastic at generating massive marketing copy but hallucinates frequently when comparing disconnected models or prices.

### 2. Graph RAG (The "Structured Entity" Approach)
* **Mechanic**: The system uses the `SpannerGraphVectorContextRetriever` in a **Hybrid Array**. 
    1. First, it performs a Vector Search to mathematically locate the **Top 3** (`top_k=3`) entry-point nodes (Products) in the Spanner graph.
    2. Then, it statically traverses **1 graph hop** (`expand_by_hops=1`) outward to retrieve connected "Edges" up to a maximum graph limit of 50 objects (`k=50`).
* **Outcome**: It acts like an intelligent e-commerce recommendation engine. Rather than fetching marketing fluff, it organically maps physical connections (Accessories, Upgrades, Feature Bundles) mapping perfectly to the target drone or camera.

---

## Step-by-Step Implementation Guide

Follow this guide to recreate the Cloud Run + React App Architecture from scratch.

### Step 1: Google Cloud Environment Preparation
1. Create a Google Cloud Project (e.g., `<YOUR_GCP_PROJECT_ID>`).
2. Enable the **Cloud Spanner API**, **Cloud Run API**, and **Vertex AI API**.
3. Create a Spanner Instance and populate your database (`<YOUR_SPANNER_DATABASE_NAME>`) with two distinct schemas:
   * A standard table mapped with embedding columns for text querying.
   * A formal Graph Schema mapping Nodes (Products, Features, Categories) connected organically via Edges (`BELONGS_TO`, `ACCESSORY_OF`).

### Step 2: Construct the Python / FastAPI Backend
The backend utilizes Python `LangChain` to construct two distinct pipelines acting autonomously. 

1. **Initialize the Environment**: `pip install fastapi uvicorn langchain-google-spanner langchain-google-vertexai`.
2. **Traditional Pipeline**: Initialize `SpannerVectorStore` routing natively into Gemini.
3. **Graph Context Engine (`rag_pipeline.py`)**: 
   * Configure `SpannerGraphVectorContextRetriever`. Set `top_k=3` (starting nodes) and `expand_by_hops=1`.
   * **Crucial Step**: Increase the subgraph constraint to `k=50` to safeguard against truncating necessary relationship edges.
   * *Performance Tip*: Cache this Retriever in server memory so it doesn't repeatedly drop and establish Spanner configuration connections.
4. **Define the Server Endpoints (`main.py`)**:
   * Wrap LangChain `.invoke()` executions explicitly inside `asyncio.to_thread()` blocks. Because FastAPI is an async loop, running raw LangChain queries natively will artificially block incoming concurrent network requests!
   * Optionally integrate an `demo_cache_graph` dictionary to locally memorize strings for instant 0.05ms "stage-demo" latency simulations.
5. **Deploy**:
   ```bash
   gcloud run deploy <YOUR_CLOUD_RUN_SERVICE_NAME> --source . --region <YOUR_GCP_REGION> --quiet
   ```

### Step 3: Construct the React / Firebase Frontend
The UI uses `Promise.all` networking to query the backend endpoints concurrently.

1. Generate a React scaffolding tree and define the layout (`App.js`).
2. Use asynchronous fetch operations routed strictly via `Promise.all([fetchRag(), fetchGraph()])`. This ensures network lag acts universally, presenting both LLM blocks simultaneously to the user.
3. Catch frontend endpoint errors globally, but allow the endpoints to catch them individually internally so one failing backend doesn't overwrite a successful graph interface.
4. Open the `firebase.json` deployment tree and configure default cross-origin domain (CORS) security strings inside `main.py` explicitly whitelisting your frontend URL (`<YOUR_FRONTEND_URL>`).
5. Point the `API_BASE` directly to your provided Cloud Run `.run.app` service URL.
6. Deploy your static bundle.

---

**Demo Strategy**
If you are giving a live presentation and fear the 5–10 second LLM processing latency, deploy the local dictionary cache in `main.py` with an async delay parameter. Warm up the container by clicking through the questions 10 minutes prior to the talk. The cache guarantees flawless sub-second results simulating live generative AI via artificial `asyncio.sleep()` buffers.
