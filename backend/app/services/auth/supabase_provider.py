import jwt
from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.services.auth.base import AuthProvider, AuthUser


class SupabaseAuthProvider(AuthProvider):
    def __init__(self, jwt_secret: str = ""):
        self.jwt_secret = jwt_secret or settings.SUPABASE_JWT_SECRET

    async def verify_token(self, token: str) -> AuthUser:
        try:
            # Decode Supabase JWT token using HS256 secret or JWKS
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            uid = payload.get("sub")
            email = payload.get("email", "")
            app_metadata = payload.get("app_metadata", {})
            user_metadata = payload.get("user_metadata", {})
            email_verified = bool(
                payload.get("email_confirmed_at")
                or app_metadata.get("email_verified")
                or user_metadata.get("email_verified")
            )

            if not uid:
                raise UnauthorizedException("Invalid token payload: missing sub.")

            return AuthUser(
                uid=str(uid),
                email=str(email),
                email_verified=email_verified,
                provider="supabase",
            )
        except jwt.PyJWTError as e:
            raise UnauthorizedException(f"Supabase token validation failed: {str(e)}")

