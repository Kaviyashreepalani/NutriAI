from datetime import timedelta
from app.core.config import settings
from app.services.storage.base import StorageProvider


class FirebaseStorageProvider(StorageProvider):
    def __init__(self):
        self._initialized = False

    def _ensure_init(self):
        if not self._initialized:
            import firebase_admin
            from firebase_admin import storage
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            self._bucket = storage.bucket(settings.FIREBASE_STORAGE_BUCKET)
            self._initialized = True

    async def put(self, storage_key: str, data: bytes, content_type: str) -> str:
        self._ensure_init()
        blob = self._bucket.blob(storage_key)
        blob.upload_from_string(data, content_type=content_type)
        return storage_key

    async def get_signed_url(self, storage_key: str, expires_in_seconds: int = 3600) -> str:
        self._ensure_init()
        blob = self._bucket.blob(storage_key)
        return blob.generate_signed_url(expiration=timedelta(seconds=expires_in_seconds))

    async def delete(self, storage_key: str) -> bool:
        self._ensure_init()
        blob = self._bucket.blob(storage_key)
        blob.delete()
        return True

