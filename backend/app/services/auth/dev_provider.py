import jwt
from datetime import date, datetime, timedelta, timezone
from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.services.auth.base import AuthProvider, AuthUser

# Pre-defined developer test accounts
DEV_ACCOUNTS = {
    "dev-user-adolescent": {
        "uid": "dev-user-adolescent-uid",
        "email": "adolescent.girl@example.org",
        "email_verified": True,
        "role": "user",
        "label": "16-year-old vegetarian with peanut allergy",
        "full_name": "Ananya Sen (Adolescent Demo)",
        "dob": date(2008, 5, 12),
        "diet": "vegetarian",
        "requires_guardian_consent": True,
        "guardian_consent_granted": True,
    },
    "dev-user-woman28": {
        "uid": "dev-user-woman28-uid",
        "email": "woman28.vegan@example.org",
        "email_verified": True,
        "role": "user",
        "label": "28-year-old vegan woman",
        "full_name": "Kavita Nair (Pregnant Demo)",
        "dob": date(1996, 8, 20),
        "diet": "vegan",
        "requires_guardian_consent": False,
        "guardian_consent_granted": False,
    },
    "dev-user-woman42": {
        "uid": "dev-user-woman42-uid",
        "email": "woman42.eggetarian@example.org",
        "email_verified": True,
        "role": "user",
        "label": "42-year-old eggetarian woman",
        "full_name": "Dr. Sunita Rao",
        "dob": date(1984, 11, 2),
        "diet": "eggetarian",
        "requires_guardian_consent": False,
        "guardian_consent_granted": False,
    },
    "dev-admin": {
        "uid": "dev-admin-uid",
        "email": "admin@nutriai.example.org",
        "email_verified": True,
        "role": "admin",
        "label": "Platform Administrator",
        "full_name": "Admin User",
        "dob": date(1990, 1, 1),
        "diet": "vegetarian",
        "requires_guardian_consent": False,
        "guardian_consent_granted": False,
    },
    "dev-nutritionist": {
        "uid": "dev-nutritionist-uid",
        "email": "nutritionist@nutriai.example.org",
        "email_verified": True,
        "role": "nutritionist",
        "label": "Certified Nutritionist & Reviewer",
        "full_name": "Dr. Aruna Swaminathan (Nutritionist)",
        "dob": date(1988, 3, 15),
        "diet": "vegetarian",
        "requires_guardian_consent": False,
        "guardian_consent_granted": False,
    },
}


class DevLocalAuthProvider(AuthProvider):
    def __init__(self):
        if settings.APP_ENV == "production":
            raise RuntimeError(
                "CRITICAL SECURITY FAILURE: DevLocalAuthProvider is strictly forbidden in production mode!"
            )

    def create_dev_token(self, account_key: str) -> str:
        if account_key not in DEV_ACCOUNTS:
            raise ValueError(f"Unknown dev account: {account_key}")
        acc = DEV_ACCOUNTS[account_key]
        payload = {
            "sub": acc["uid"],
            "email": acc["email"],
            "email_verified": acc["email_verified"],
            "role": acc["role"],
            "account_key": account_key,
            "iss": "nutriai-dev-auth",
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def create_custom_token(self, uid: str, email: str, role: str = "user") -> str:
        payload = {
            "sub": uid,
            "email": email,
            "email_verified": True,
            "role": role,
            "iss": "nutriai-dev-auth",
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    async def verify_token(self, token: str) -> AuthUser:
        if settings.APP_ENV == "production":
            raise RuntimeError("Dev auth attempted under production environment!")

        # Allow passing account key directly in dev mode for testing convenience
        if token in DEV_ACCOUNTS:
            acc = DEV_ACCOUNTS[token]
            return AuthUser(
                uid=acc["uid"],
                email=acc["email"],
                email_verified=acc["email_verified"],
                provider="dev",
            )

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            return AuthUser(
                uid=str(payload["sub"]),
                email=str(payload.get("email", "")),
                email_verified=payload.get("email_verified", True),
                provider="dev",
            )
        except jwt.PyJWTError as e:
            raise UnauthorizedException(f"Invalid dev authorization token: {str(e)}")
