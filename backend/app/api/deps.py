import uuid
from datetime import date
from typing import AsyncGenerator, Callable, List, Optional
from fastapi import Depends, Header, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.errors import ForbiddenException, UnauthorizedException
from app.db.session import get_db
import app.db.models as models
from app.services.auth import AuthUser, get_auth_provider


async def get_current_auth_user(
    authorization: Optional[str] = Header(None),
) -> AuthUser:
    """Extracts and verifies the Bearer authentication token."""
    if not authorization:
        raise UnauthorizedException("Authorization header missing.")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthorizedException("Invalid authorization header format. Expected 'Bearer <token>'.")

    token = parts[1]
    provider = get_auth_provider()
    return await provider.verify_token(token)


async def get_current_user(
    auth_user: AuthUser = Depends(get_current_auth_user),
    db: Optional[AsyncSession] = Depends(get_db),
) -> models.User:
    """Resolves the internal User entity from auth_uid with automatic dev provisioning."""
    # Fast path if database is offline in local development mode
    if db is None:
        from app.services.auth.dev_provider import DEV_ACCOUNTS
        matching = next((v for v in DEV_ACCOUNTS.values() if v["uid"] == auth_user.uid), None)
        dob = matching.get("dob", date(1995, 1, 1)) if matching else date(1995, 1, 1)
        role = matching.get("role", "user") if matching else "user"
        return models.User(
            id=uuid.uuid5(uuid.NAMESPACE_DNS, auth_user.uid),
            auth_uid=auth_user.uid,
            auth_provider="dev",
            email=auth_user.email,
            email_verified=True,
            role=role,
            preferred_language="en",
            date_of_birth=dob,
            status="active",
        )

    try:
        stmt = select(models.User).where(models.User.auth_uid == auth_user.uid)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
    except Exception:
        user = None

    if not user:
        if auth_user.provider == "dev":
            from app.services.auth.dev_provider import DEV_ACCOUNTS
            matching = next((v for v in DEV_ACCOUNTS.values() if v["uid"] == auth_user.uid), None)
            dob = matching.get("dob", date(1995, 1, 1)) if matching else date(1995, 1, 1)
            role = matching.get("role", "user") if matching else "user"
            full_name = matching.get("full_name", "Demo User") if matching else "Demo User"
            try:
                user = models.User(
                    auth_uid=auth_user.uid,
                    auth_provider="dev",
                    email=auth_user.email,
                    email_verified=True,
                    role=role,
                    preferred_language="en",
                    date_of_birth=dob,
                    status="active",
                )
                db.add(user)
                await db.flush()

                profile = models.UserProfile(
                    user_id=user.id,
                    full_name=full_name,
                    profile_completion_pct=100,
                )
                db.add(profile)

                cart = models.Cart(user_id=user.id)
                db.add(cart)

                await db.commit()
                await db.refresh(user)
                return user
            except Exception:
                return models.User(
                    id=uuid.UUID("00000000-0000-0000-0000-" + auth_user.uid.replace("-", "")[:12].ljust(12, "0")),
                    auth_uid=auth_user.uid,
                    auth_provider="dev",
                    email=auth_user.email,
                    email_verified=True,
                    role=role,
                    preferred_language="en",
                    date_of_birth=dob,
                    status="active",
                )

        raise UnauthorizedException("User account not found. Please complete profile registration.")

    if user.status != "active":
        raise ForbiddenException("User account is inactive or suspended.")

    return user


def require_role(allowed_roles: List[str]) -> Callable:
    """Dependency factory enforcing role-based authorization."""
    async def role_checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(f"Action restricted to roles: {allowed_roles}")
        return current_user
    return role_checker


def check_resource_ownership(resource_owner_id: uuid.UUID, current_user: models.User) -> None:
    """Enforces strict multi-tenant ownership: User A cannot read or write User B's resources."""
    if current_user.role in ("admin", "nutritionist"):
        return
    if str(resource_owner_id) != str(current_user.id):
        raise ForbiddenException("Access denied: You do not own this resource.")


async def log_audit_event(
    db: Optional[AsyncSession],
    user_id: Optional[uuid.UUID],
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
) -> None:
    """Records security and clinical audit trails."""
    if db is None:
        return
    try:
        audit = models.AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
        )
        db.add(audit)
        await db.commit()
    except Exception:
        pass
