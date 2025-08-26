"""Orchestration pipeline:
- Read CSV
- Build KG (TTL)
- Compute tariff impact
- Optionally push to Neo4j and GCS
- Trigger agent messages
"""
import os, pandas as pd
from kg.build_kg import build_kg_from_csv
from agents.agent_core import Agent, AgentManager
from dotenv import load_dotenv
from gcp.gcs_utils import upload_file

load_dotenv()

DATA_CSV = os.getenv('DATA_CSV', os.path.join(os.path.dirname(__file__),'..','data','sample_tariffs_small.csv'))
KG_OUT = os.path.join(os.path.dirname(__file__),'..','kg','tariff_kg.ttl')

def compute_tariff_impact(df):
    df = df.copy()
    df['tariff_delta_pct'] = df['tariff_after'] - df['tariff_before']
    df['estimated_additional_cost_usd'] = df['import_value_usd'] * (df['tariff_delta_pct'] / 100.0)
    return df

def main():
    print('Starting pipeline...')
    df = pd.read_csv(DATA_CSV)
    kg_path = build_kg_from_csv(DATA_CSV, output_path=KG_OUT)
    print('KG wrote to', kg_path)
    impact_df = compute_tariff_impact(df)
    print(impact_df.head())

    # Agent orchestration demo
    manager = AgentManager()
    da = Agent('DataAgent'); ra = Agent('ReasoningAgent')
    manager.register(da); manager.register(ra)
    summary = impact_df.groupby('product_code')['estimated_additional_cost_usd'].sum().reset_index().to_dict('records')
    da.inbox.put({'to':'ReasoningAgent','from':'DataAgent','message':{'type':'tariff_summary','payload':summary}})
    manager.route_all()

    # Upload KG to GCS if configured
    bucket = os.getenv('GCP_BUCKET')
    if bucket and os.path.exists(kg_path):
        print('Uploading KG to GCS...')
        upload_file(kg_path, bucket, destination_name='kg/tariff_kg.ttl')
    print('Pipeline completed.')

if __name__ == '__main__':
    main()
