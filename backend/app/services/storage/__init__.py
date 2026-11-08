from app.core.config import settings
from app.services.storage.base import StorageProvider
from app.services.storage.s3_provider import S3StorageProvider
from app.services.storage.supabase_provider import SupabaseStorageProvider
from app.services.storage.firebase_provider import FirebaseStorageProvider


def get_storage_provider() -> StorageProvider:
    if settings.STORAGE_PROVIDER == "supabase":
        return SupabaseStorageProvider()
    elif settings.STORAGE_PROVIDER == "firebase":
        return FirebaseStorageProvider()
    else:
        return S3StorageProvider()


__all__ = ["StorageProvider", "get_storage_provider"]

