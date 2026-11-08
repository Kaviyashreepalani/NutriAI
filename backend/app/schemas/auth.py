import uuid
from datetime import date
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class SessionRequest(BaseModel):
    token: str = Field(description="Supabase / Firebase / Dev authentication token")


class UserSessionResponse(BaseModel):
    id: uuid.UUID
    auth_uid: str
    email: EmailStr
    email_verified: bool
    role: str
    preferred_language: str
    date_of_birth: date
    age: int
    full_name: Optional[str] = None
    profile_completion_pct: int = 0
    requires_guardian_consent: bool = False
    guardian_consent_granted: bool = False


class DevLoginRequest(BaseModel):
    account_key: str = Field(description="Pre-defined developer account key, e.g. dev-user-adolescent")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class GuardianConsentInfo(BaseModel):
    guardian_name: str = Field(min_length=2, max_length=255)
    guardian_relation: str = Field(min_length=2, max_length=64)
    guardian_contact: str = Field(min_length=6, max_length=64)
    guardian_consent: bool = True


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
    date_of_birth: date
    preferred_language: str = Field(default="en", pattern="^(en|ta|hi|te|ml)$")
    role: str = Field(default="user", pattern="^(user|nutritionist|admin)$")
    consent_data: bool = True
    consent_health: bool = True
    guardian: Optional[GuardianConsentInfo] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class AuthTokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    user: Optional[UserSessionResponse] = None


class RegisterProfileRequest(BaseModel):
    token: str
    full_name: str = Field(min_length=2, max_length=255)
    date_of_birth: date
    preferred_language: str = Field(default="en", pattern="^(en|ta|hi|te|ml)$")
    role: str = Field(default="user", pattern="^(user|nutritionist|admin)$")


class GuardianConsentRequest(BaseModel):
    guardian_name: str = Field(min_length=2, max_length=255)
    guardian_relation: str = Field(min_length=2, max_length=64)
    guardian_contact: str = Field(min_length=6, max_length=64)
    purpose: str = Field(default="data_processing")
    granted: bool = True
    policy_version: str = Field(default="v1.0")
