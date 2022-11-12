import os
from google.cloud import storage
from sqlalchemy import true

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'

bucket_name = os.environ.get('GOOGLE_APPLICATION_BUCKET_NAME', None)
if bucket_name is None:
    bucket_name = 'grupo4-cloud-366900-archivos'

class GoogleStorage:
    def upload_to_bucket(self, blob_name, file_path):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return blob

    def val_file_to_bucket(self, blob_name):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(bucket_name)
        blob_list = [ blob.name for blob in blobs ]
        return blob_name in blob_list

    def download_file_from_bucket(self, blog_name, file_path):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blog_name)
        blob.download_to_filename(file_path)
        