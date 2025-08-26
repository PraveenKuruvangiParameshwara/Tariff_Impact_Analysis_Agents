"""Helpers for BigQuery ingestion and queries."""
from google.cloud import bigquery
import pandas as pd

def upload_dataframe(df, dataset_table, project=None):
    client = bigquery.Client(project=project)
    job = client.load_table_from_dataframe(df, dataset_table)
    job.result()
    return job.result()
