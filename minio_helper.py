import json, os
from minio import Minio
from minio.error import S3Error

class MinioHelper:
    def __init__(self, client):
        self.client = client

    @classmethod
    def from_config(cls, config_path='minio_config.json'):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'MinIO config not found: {config_path}')
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        endpoint = cfg.get('endpoint')
        access = cfg.get('access_key')
        secret = cfg.get('secret_key')
        secure = cfg.get('secure', False)
        client = Minio(endpoint, access_key=access, secret_key=secret, secure=secure)
        # simple validation
        try:
            client.list_buckets()
        except Exception as e:
            raise RuntimeError(f'Failed to connect to MinIO: {e}')
        return cls(client)

    def download(self, bucket, object_name, local_path):
        try:
            if not self.client.bucket_exists(bucket):
                raise RuntimeError(f'Bucket does not exist: {bucket}')
            self.client.fget_object(bucket, object_name, local_path)
            print(f'[MinIO] ✅ Downloaded {object_name} to {local_path}')
        except S3Error as e:
            raise RuntimeError(f'[MinIO] Error downloading object: {e}')

    def upload(self, bucket, local_path, object_name):
        try:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
            self.client.fput_object(bucket, object_name, local_path)
            print(f'[MinIO] ✅ Uploaded {local_path} to {bucket}/{object_name}')
        except S3Error as e:
            raise RuntimeError(f'[MinIO] Error uploading object: {e}')
