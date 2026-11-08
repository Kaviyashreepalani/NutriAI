from app.core.config import settings
from app.services.auth.base import AuthProvider, AuthUser
from app.services.auth.supabase_provider import SupabaseAuthProvider
from app.services.auth.firebase_provider import FirebaseAuthProvider
from app.services.auth.dev_provider import DevLocalAuthProvider, DEV_ACCOUNTS


def get_auth_provider() -> AuthProvider:
    if settings.AUTH_PROVIDER == "supabase":
        return SupabaseAuthProvider()
    elif settings.AUTH_PROVIDER == "firebase":
        return FirebaseAuthProvider()
    elif settings.AUTH_PROVIDER == "dev":
        if settings.APP_ENV == "production":
            raise RuntimeError("Fatal: DevLocalAuthProvider cannot be used in production.")
        return DevLocalAuthProvider()
    else:
        raise ValueError(f"Unsupported AUTH_PROVIDER: {settings.AUTH_PROVIDER}")


__all__ = ["AuthProvider", "AuthUser", "get_auth_provider", "DEV_ACCOUNTS"]

