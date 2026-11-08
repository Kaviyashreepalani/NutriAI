import socket
from urllib.parse import urlparse
from typing import AsyncGenerator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Base class for SQLAlchemy models
Base = declarative_base()

# Prepare URLs for async and sync engines
raw_url = settings.DATABASE_URL
if raw_url.startswith("postgresql://"):
    async_db_url = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    sync_db_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("postgresql+asyncpg://"):
    async_db_url = raw_url
    sync_db_url = raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("sqlite"):
    async_db_url = "sqlite+aiosqlite:///./test.db" if not raw_url.startswith("sqlite+aiosqlite") else raw_url
    sync_db_url = "sqlite:///./test.db"
else:
    async_db_url = raw_url
    sync_db_url = raw_url

def is_db_reachable(timeout: float = 2.5) -> bool:
    """Fast non-blocking socket probe to verify if the configured database host is listening."""
    try:
        parsed = urlparse(raw_url.replace("postgresql+asyncpg://", "http://").replace("postgresql://", "http://"))
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

# Async Engine for FastAPI Request Lifecycle
async_engine = create_async_engine(
    async_db_url,
    echo=False,
    future=True,
    pool_pre_ping=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Synchronous Engine for Seed Scripts and Migrations
sync_engine = create_engine(
    sync_db_url,
    echo=False,
    future=True,
    pool_pre_ping=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[Optional[AsyncSession], None]:
    """Dependency that yields an async database session, or None if database is offline or unauthenticated."""
    if not is_db_reachable():
        yield None
        return

    can_connect = False
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            can_connect = True
    except Exception:
        can_connect = False

    if not can_connect:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
