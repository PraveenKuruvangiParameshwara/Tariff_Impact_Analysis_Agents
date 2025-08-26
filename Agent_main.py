# main.py
import os
from dotenv import load_dotenv
from knowledge_graph.scripts.kg_builder import ingest_data_from_gcs
from utils.neo4j_connector import Neo4jConnection
from multi_agent_system.pipelines.analysis_pipeline import project_crew

def main():
    """Main function to run the tariff impact analysis pipeline."""
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Neo4j connection
    neo4j_conn = Neo4jConnection(os.getenv("NEO4J_URI"), os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS"))

    # Step 1: Ingest data into the knowledge graph
    print("--- Starting data ingestion into the knowledge graph ---")
    try:
        # In a real-world scenario, you would have a trade_data.csv file in your GCS bucket
        ingest_data_from_gcs(
            bucket_name=os.getenv("GCS_BUCKET_NAME"),
            file_path="raw/trade_data.csv",
            db_conn=neo4j_conn
        )
    except Exception as e:
        print(f"Error during data ingestion: {e}")
        neo4j_conn.close()
        return

    # Step 2: Run the multi-agent analysis pipeline
    print("\n--- Starting multi-agent tariff impact analysis ---")
    try:
        analysis_result = project_crew.kickoff()
        print("\n--- Analysis completed successfully ---")
        print(analysis_result)
    except Exception as e:
        print(f"Error during agent analysis: {e}")
    finally:
        neo4j_conn.close()

if __name__ == "__main__":
    main()
