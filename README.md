# Spanner Graph RAG vs. Traditional RAG Showcase

Welcome to the **Spanner Graph RAG Comparison** repository! This project serves as a functional, side-by-side demonstration of the structural and conceptual differences between Traditional Vector RAG (Retrieval-Augmented Generation) and Graph RAG using **Google Cloud Spanner**.

## Architecture Overview
This repository contains two main components:
1. **`firebase-frontend`**: A React application that dynamically loads and displays a side-by-side comparison of Traditional RAG vs. Graph RAG query results perfectly synchronized using asynchronous APIs.
2. **`spanner-rag-backend`**: A Python FastAPI backend running on Cloud Run, utilizing Vertex AI `text-embedding-004` and `gemini-2.0-flash` models parsed natively via the `langchain-google-spanner` framework.

## Setup & Implementation Guide
For a deep dive into the underlying mechanics of Graph RAG vs Traditional RAG, and for a step-by-step walkthrough on how to recreate this architecture yourself (including setting up Spanner configurations and deploying to Cloud Run/Firebase), please see the full walkthrough document!

👉 [Spanner Graph RAG Implementation & Architecture Walkthrough](./spanner_graph_rag_walkthrough.md)

### Deployment Commands Quick Reference
To deploy the backend to Cloud Run, execute the following from the `spanner-rag-backend/` directory:
```bash
gcloud run deploy <YOUR_CLOUD_RUN_SERVICE_NAME> --source . --region <YOUR_GCP_REGION>
```

To run your React frontend locally, run perfectly concurrent LLM queries from the `firebase-frontend/` directory:
```bash
npm install
npm start
```
