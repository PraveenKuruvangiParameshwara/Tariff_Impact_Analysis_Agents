# knowledge_graph/scripts/kg_builder.py
from utils.neo4j_connector import Neo4jConnection
from google.cloud import storage
import os
import pandas as pd
from dotenv import load_dotenv

def ingest_data_from_gcs(bucket_name, file_path, db_conn):
    """
    Reads a CSV file from GCS, processes it, and loads it into Neo4j.
    
    Args:
        bucket_name (str): The name of the GCS bucket.
        file_path (str): The path to the CSV file within the bucket.
        db_conn (Neo4jConnection): The Neo4j database connection object.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    
    # Download and process the CSV file using pandas
    try:
        df = pd.read_csv(f'gs://{bucket_name}/{file_path}')
        print(f"Read {len(df)} rows from {file_path}")
    except Exception as e:
        print(f"Error reading from GCS: {e}")
        return

    # Ingest data into Neo4j
    with db_conn.driver.session() as session:
        for _, row in df.iterrows():
            # Example Cypher query to create nodes and relationships
            cypher_query = """
            MERGE (p:Product {id: $product_id, name: $product_name})
            MERGE (c:Country {name: $country_name})
            MERGE (t:TariffPolicy {rate: $tariff_rate, effective_date: date($effective_date)})
            MERGE (c)-[:APPLIES_TARIFF]->(t)
            MERGE (t)-[:AFFECTS]->(p)
            """
            session.run(cypher_query, parameters={
                "product_id": row['product_id'],
                "product_name": row['product_name'],
                "country_name": row['country'],
                "tariff_rate": float(row['tariff_rate']),
                "effective_date": str(row['effective_date'])
            })
    print("Data successfully ingested into the knowledge graph.")
