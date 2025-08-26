Expanded Project Folder Structure
---------------------------------
tariff_impact_analysis_full/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ Dockerfile
├─ cloudbuild.yaml
├─ data/
│  ├─ sample_tariffs_small.csv
│  └─ sample_tariffs_medium.csv
├─ pipeline/
│  └─ main.py
├─ kg/
│  ├─ build_kg.py
│  ├─ tariff_kg.ttl (generated)
│  └─ queries.sparql
├─ neo4j/
│  └─ neo4j_loader.py
├─ agents/
│  ├─ agent_core.py
│  ├─ memory_vector_stub.py
│  └─ langgraph_stub.py
├─ mcp/
│  └─ server.py
├─ gcp/
│  ├─ gcs_utils.py
│  ├─ bigquery_utils.py
│  └─ pubsub_utils.py
├─ webui/
│  └─ app.py
├─ deploy/
│  ├─ deploy_instructions.md
│  ├─ cloud_run_notes.md
│  └─ cloudbuild.yaml
└─ deploy.sh
