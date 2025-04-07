import boto3
from botocore.client import Config
from typing import Optional, BinaryIO

class S3Client:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
        )

    def get_file_size(self, filename: str) -> Optional[int]:
        response = self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
        return response["ContentLength"]

    def stream_file(self, filename: str, start: int = 0, end: Optional[int] = None) -> Optional[BinaryIO]:
        range_header = f"bytes={start}-{end}" if end is not None else f"bytes={start}-"
        response = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=filename,
            Range=range_header
        )
        return response["Body"]
