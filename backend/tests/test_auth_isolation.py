import uuid
import pytest
from app.api.deps import check_resource_ownership
from app.core.config import settings
from app.core.errors import ForbiddenException
from app.db.models.user import User
from app.services.auth.dev_provider import DevLocalAuthProvider


def test_dev_auth_refuses_production():
    # If APP_ENV is production, DevLocalAuthProvider must raise an error
    original_env = settings.APP_ENV
    try:
        settings.APP_ENV = "production"
        with pytest.raises(RuntimeError) as exc_info:
            DevLocalAuthProvider()
        assert "forbidden in production mode" in str(exc_info.value)
    finally:
        settings.APP_ENV = original_env


def test_resource_ownership_check():
    user_a = User(id=uuid.uuid4(), role="user")
    user_b_id = uuid.uuid4()

    # User A attempting to access User B's resource should raise ForbiddenException
    with pytest.raises(ForbiddenException):
        check_resource_ownership(user_b_id, user_a)

    # User A accessing their own resource should pass
    check_resource_ownership(user_a.id, user_a)

