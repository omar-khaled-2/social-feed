import boto3
from botocore.client import Config as BotoConfig
from app.config import Config

s3_client = boto3.client(
    's3',
    endpoint_url=Config.MINIO_ENDPOINT,
    aws_access_key_id=Config.MINIO_ACCESS_KEY,
    aws_secret_access_key=Config.MINIO_SECRET_KEY,
    config=BotoConfig(signature_version='s3v4'),
    region_name='us-east-1'  
)


