import json
from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.services.auth.base import AuthProvider, AuthUser


class FirebaseAuthProvider(AuthProvider):
    def __init__(self):
        self._initialized = False

    def _ensure_init(self):
        if not self._initialized:
            try:
                import firebase_admin
                from firebase_admin import credentials

                if not firebase_admin._apps:
                    if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
                        cred_dict = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
                        cred = credentials.Certificate(cred_dict)
                        firebase_admin.initialize_app(cred)
                    elif settings.FIREBASE_SERVICE_ACCOUNT_PATH:
                        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
                        firebase_admin.initialize_app(cred)
                    else:
                        firebase_admin.initialize_app()
                self._initialized = True
            except Exception as e:
                pass

    async def verify_token(self, token: str) -> AuthUser:
        self._ensure_init()
        try:
            import firebase_admin.auth
            decoded = firebase_admin.auth.verify_id_token(token)
            return AuthUser(
                uid=decoded["uid"],
                email=decoded.get("email", ""),
                email_verified=decoded.get("email_verified", False),
                provider="firebase",
            )
        except Exception as e:
            raise UnauthorizedException(f"Firebase token validation failed: {str(e)}")

