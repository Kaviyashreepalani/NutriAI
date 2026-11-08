from abc import ABC, abstractmethod


class StorageProvider(ABC):
    @abstractmethod
    async def put(self, storage_key: str, data: bytes, content_type: str) -> str:
        """Stores object bytes at storage_key and returns the canonical key or URL."""
        pass

    @abstractmethod
    async def get_signed_url(self, storage_key: str, expires_in_seconds: int = 3600) -> str:
        """Generates a short-lived secure download URL."""
        pass

    @abstractmethod
    async def delete(self, storage_key: str) -> bool:
        """Deletes the stored object."""
        pass

