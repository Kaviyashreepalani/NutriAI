from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel


class AuthUser(BaseModel):
    uid: str
    email: str
    email_verified: bool = False
    provider: str


class AuthProvider(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> AuthUser:
        """Verifies an authentication token and returns the normalized AuthUser."""
        pass

