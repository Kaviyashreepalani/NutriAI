import os
import boto3
from botocore.config import Config
from app.core.config import settings
from app.services.storage.base import StorageProvider


class S3StorageProvider(StorageProvider):
    def __init__(self):
        self.bucket = settings.S3_BUCKET_NAME
        self.endpoint_url = settings.S3_ENDPOINT_URL
        self.client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version="s3v4"),
        )
        # Ensure local fallback dir exists if local testing without running MinIO
        self._local_fallback_dir = os.path.join(os.getcwd(), "storage", "reports")
        os.makedirs(self._local_fallback_dir, exist_ok=True)

    async def put(self, storage_key: str, data: bytes, content_type: str) -> str:
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=storage_key,
                Body=data,
                ContentType=content_type,
            )
            return storage_key
        except Exception:
            # Fallback to local storage path for offline dev
            safe_filename = storage_key.replace("/", "_")
            file_path = os.path.join(self._local_fallback_dir, safe_filename)
            with open(file_path, "wb") as f:
                f.write(data)
            return storage_key

    async def get_signed_url(self, storage_key: str, expires_in_seconds: int = 3600) -> str:
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": storage_key},
                ExpiresIn=expires_in_seconds,
            )
            return url
        except Exception:
            return f"/api/v1/storage/download/{storage_key}"

    async def delete(self, storage_key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket, Key=storage_key)
            return True
        except Exception:
            safe_filename = storage_key.replace("/", "_")
            file_path = os.path.join(self._local_fallback_dir, safe_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            return True

