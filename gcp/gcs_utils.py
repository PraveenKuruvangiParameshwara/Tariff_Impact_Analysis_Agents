"""Helpers to interact with Google Cloud Storage."""
import os
from google.cloud import storage

def upload_file(local_path, bucket_name, destination_name=None):
    if not os.path.exists(local_path):
        raise FileNotFoundError(local_path)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    if not destination_name:
        destination_name = os.path.basename(local_path)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(local_path)
    return f'gs://{bucket_name}/{destination_name}'
