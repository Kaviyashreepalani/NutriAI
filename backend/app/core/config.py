import os
from typing import List

# Constrain OpenBLAS / OpenMP threading on Windows to prevent memory allocation faults
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    SECRET_KEY: str = Field(default="dev-secret-key-at-least-32-chars-long-for-testing")
    ENCRYPTION_KEY: str = Field(default="dGhpc2lzYTMyeWVhcmxvbmctc2VjcmV0LWtleS1mb3ItZGV2")

    DATA_PLATFORM: str = Field(default="supabase")
    AUTH_PROVIDER: str = Field(default="dev")
    STORAGE_PROVIDER: str = Field(default="s3")

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/nutriai"
    )
    DATABASE_DIRECT_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/nutriai"
    )

    # Supabase
    SUPABASE_URL: str = Field(default="")
    SUPABASE_ANON_KEY: str = Field(default="")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="")
    SUPABASE_JWT_SECRET: str = Field(default="")
    SUPABASE_STORAGE_BUCKET_REPORTS: str = Field(default="reports")
    SUPABASE_STORAGE_BUCKET_IMAGES: str = Field(default="product-images")

    # Firebase
    FIREBASE_PROJECT_ID: str = Field(default="")
    FIREBASE_SERVICE_ACCOUNT_PATH: str = Field(default="")
    FIREBASE_SERVICE_ACCOUNT_JSON: str = Field(default="")
    FIREBASE_STORAGE_BUCKET: str = Field(default="")

    # S3 / MinIO
    S3_ENDPOINT_URL: str = Field(default="http://localhost:9000")
    S3_ACCESS_KEY: str = Field(default="minioadmin")
    S3_SECRET_KEY: str = Field(default="minioadminpassword")
    S3_BUCKET_NAME: str = Field(default="nutriai-reports")
    S3_REGION: str = Field(default="us-east-1")

    # LLM
    LLM_PROVIDER: str = Field(default="mock")
    GEMINI_API_KEY: str = Field(default="")
    ANTHROPIC_API_KEY: str = Field(default="")

    # Speech
    SPEECH_PROVIDER: str = Field(default="mock")
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(default="")
    BHASHINI_API_KEY: str = Field(default="")
    BHASHINI_USER_ID: str = Field(default="")

    # OCR
    ENABLE_LLM_OCR_FALLBACK: bool = Field(default=False)
    OCR_CONFIDENCE_THRESHOLD: float = Field(default=0.75)

    # Safety
    ALLOW_GENERATION_WITH_REFERRAL: bool = Field(default=True)
    DEFAULT_IRON_TARGET_MIN_MG: float = Field(default=4.0)
    DEFAULT_IRON_TARGET_MAX_MG: float = Field(default=5.0)

    # CORS
    FRONTEND_URL: str = Field(default="http://localhost:5173")
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    )

    @property
    def parsed_allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    def validate_runtime_configuration(self) -> None:
        """Enforce strict startup configuration checks and safety rules."""
        if self.APP_ENV == "production":
            if self.AUTH_PROVIDER == "dev":
                raise ValueError(
                    "FATAL SECURITY VIOLATION: AUTH_PROVIDER cannot be 'dev' when APP_ENV=production. "
                    "Configure 'supabase' or 'firebase' auth for production deployment."
                )
            if "change-this" in self.SECRET_KEY or len(self.SECRET_KEY) < 32:
                raise ValueError("FATAL SECURITY VIOLATION: SECRET_KEY must be a strong key >= 32 chars in production.")

        if self.AUTH_PROVIDER == "supabase":
            if not self.SUPABASE_URL or not self.SUPABASE_JWT_SECRET:
                raise ValueError(
                    "CONFIGURATION ERROR: SUPABASE_URL and SUPABASE_JWT_SECRET are required when AUTH_PROVIDER='supabase'."
                )

        if self.AUTH_PROVIDER == "firebase":
            if not self.FIREBASE_PROJECT_ID:
                raise ValueError(
                    "CONFIGURATION ERROR: FIREBASE_PROJECT_ID is required when AUTH_PROVIDER='firebase'."
                )


settings = Settings()

