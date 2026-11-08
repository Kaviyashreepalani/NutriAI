import pytest
from datetime import date
from app.api.v1.auth import dev_login, login, register, forgot_password, create_or_get_session
from app.schemas.auth import DevLoginRequest, LoginRequest, RegisterRequest, ForgotPasswordRequest, SessionRequest


@pytest.mark.asyncio
async def test_dev_login_adolescent():
    req = DevLoginRequest(account_key="dev-user-adolescent")
    res = await dev_login(req, db=None)
    assert res.token is not None
    assert res.user.email == "adolescent.girl@example.org"
    assert res.user.age == 16
    assert res.user.requires_guardian_consent is True


@pytest.mark.asyncio
async def test_dev_login_adult():
    req = DevLoginRequest(account_key="dev-user-woman28")
    res = await dev_login(req, db=None)
    assert res.token is not None
    assert res.user.email == "woman28.vegan@example.org"
    assert res.user.requires_guardian_consent is False


@pytest.mark.asyncio
async def test_login_with_dev_email():
    req = LoginRequest(email="adolescent.girl@example.org", password="anypassword")
    res = await login(req, db=None)
    assert res.token is not None
    assert res.user.email == "adolescent.girl@example.org"


@pytest.mark.asyncio
async def test_register_adult_user():
    req = RegisterRequest(
        full_name="KAVIYA SHREE PALANI",
        email="kaviyashreepj0911@gmail.com",
        password="password123",
        date_of_birth=date(2005, 11, 9),
        preferred_language="en",
    )
    res = await register(req, db=None)
    assert res.token is not None
    assert res.user.full_name == "KAVIYA SHREE PALANI"
    assert res.user.email == "kaviyashreepj0911@gmail.com"
    assert res.user.requires_guardian_consent is False

    # Check session
    s_req = SessionRequest(token=res.token)
    session = await create_or_get_session(s_req, db=None)
    assert session.email == "kaviyashreepj0911@gmail.com"


@pytest.mark.asyncio
async def test_forgot_password():
    req = ForgotPasswordRequest(email="kaviyashreepj0911@gmail.com")
    res = await forgot_password(req)
    assert res["success"] is True
