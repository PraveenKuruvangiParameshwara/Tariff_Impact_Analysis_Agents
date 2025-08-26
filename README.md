# Tariff Impact Analysis — GenAI + Agentic AI (GCP-ready)

This is a comprehensive starter project scaffold to build a tariff impact analysis solution focused on India.
It integrates Knowledge Graphs (RDF/OWL), SPARQL, Neo4j, multi-agent orchestration stubs (LangGraph/AutoGen/CrewAI style),
agent memory stubs (vector DB), MCP runtime server, and Google Cloud SDK integrations (GCS, BigQuery, Pub/Sub, Vertex AI notes).

**Created:** 2025-08-09

## What's included
- `data/` — sample datasets (small and medium) to start experiments.
- `kg/` — RDF/OWL KG builder and SPARQL query examples.
- `neo4j/` — loader to upsert KG summaries to Neo4j.
- `agents/` — agent runtime stubs, A2A messaging simulation, memory vector DB stub.
- `mcp/` — MCP-style Flask server ready for containerization.
- `pipeline/` — orchestration pipeline (ingest -> KG -> index -> agents -> analysis).
- `gcp/` — utilities for GCS, BigQuery, Pub/Sub and deployment helpers.
- `webui/` — Streamlit app to explore KG and impact results.
- `deploy/` — Dockerfile, cloudbuild.yaml, and Cloud Run notes.
- `.env.example` — environment variables template.
- `requirements.txt` — baseline python packages.

## Quick local demo
1. Create venv and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill values (Neo4j, GCP credentials).
3. Run pipeline:
   ```bash
   python -m pipeline.main
   python pipeline/main.py
   ```
4. Run the MCP server (for agent runtime):
   ```bash
   python mcp/server.py
   ```
5. Start Streamlit web UI:
   ```bash
   streamlit run webui/app.py
   ```

## Notes
- Several modules contain stubs and `TODO` markers where production connectors (LangGraph, AutoGen, CrewAI, Pinecone, Vertex Matching) should be wired in.
- This repo is intended as a fully-documented starting point for productionization on GCP.
