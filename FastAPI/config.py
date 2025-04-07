import os
from dotenv import load_dotenv

load_dotenv()

MINIO_CONFIG = {
    "endpoint": os.getenv("MINIO_ENDPOINT"),
    "access_key": os.getenv("MINIO_ACCESS_KEY"),
    "secret_key": os.getenv("MINIO_SECRET_KEY"),
    "bucket_name": os.getenv("MINIO_BUCKET_NAME"),
}