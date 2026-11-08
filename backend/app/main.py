from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.errors import AppException, format_error_response
from app.db.session import sync_engine, Base, is_db_reachable
import app.db.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Enforce strict configuration validation
    settings.validate_runtime_configuration()

    # 2. Check if DB is reachable before attempting schema creation and seed
    if is_db_reachable(timeout=0.1):
        try:
            Base.metadata.create_all(bind=sync_engine)
        except Exception as e:
            print(f"Database schema auto-creation notice: {e}")

        # 3. Optional auto-seed in dev mode
        if settings.APP_ENV == "development":
            try:
                from app.seed.load import load_seed_data
                load_seed_data()
            except Exception as e:
                print(f"Auto-seed completed or skipped: {e}")
    else:
        print("Database offline; running in resilient dev mode with fallback.")

    yield


app = FastAPI(
    title="NutriAI – AI-Optimized Nutrient-Dense Food Products for Anaemia Prevention",
    description=(
        "Research and clinical food formulation platform for adolescent girls and women of reproductive age. "
        "Deterministic code calculates all numbers. The LLM only explains."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# Centralized Exception Handlers enforcing { "error": { "code", "message", "details" } }
@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(exc.code, exc.message, exc.details),
    )


@app.exception_handler(Exception)
async def handle_unhandled_exception(request: Request, exc: Exception):
    if settings.DEBUG:
        print(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            "INTERNAL_SERVER_ERROR",
            "An unexpected error occurred. Please contact system support.",
            {"detail": str(exc)} if settings.DEBUG else None,
        ),
    )


# Mount All API Routes
app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "app": "NutriAI",
        "status": "online",
        "docs": "/docs",
        "api_v1": "/api/v1",
        "medical_disclaimer": "NutriAI is a dietary formulation support platform. It does not diagnose, treat, or cure medical conditions.",
    }

