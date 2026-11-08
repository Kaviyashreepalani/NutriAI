import httpx
from app.core.config import settings
from app.services.storage.base import StorageProvider


class SupabaseStorageProvider(StorageProvider):
    def __init__(self):
        self.base_url = settings.SUPABASE_URL.rstrip("/")
        self.bucket = settings.SUPABASE_STORAGE_BUCKET_REPORTS
        self.service_key = settings.SUPABASE_SERVICE_ROLE_KEY

    async def put(self, storage_key: str, data: bytes, content_type: str) -> str:
        url = f"{self.base_url}/storage/v1/object/{self.bucket}/{storage_key}"
        headers = {
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": content_type,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=data, headers=headers)
            if resp.status_code not in (200, 201):
                # Try PUT update
                resp = await client.put(url, content=data, headers=headers)
        return storage_key

    async def get_signed_url(self, storage_key: str, expires_in_seconds: int = 3600) -> str:
        url = f"{self.base_url}/storage/v1/object/sign/{self.bucket}/{storage_key}"
        headers = {
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={"expiresIn": expires_in_seconds}, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                signed_path = data.get("signedURL", "")
                return f"{self.base_url}/storage/v1{signed_path}"
        return f"/api/v1/storage/download/{storage_key}"

    async def delete(self, storage_key: str) -> bool:
        url = f"{self.base_url}/storage/v1/object/{self.bucket}/{storage_key}"
        headers = {"Authorization": f"Bearer {self.service_key}"}
        async with httpx.AsyncClient() as client:
            resp = await client.delete(url, headers=headers)
            return resp.status_code in (200, 204)

