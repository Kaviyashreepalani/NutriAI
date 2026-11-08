"""Initial schema with PostgreSQL extensions, 24 tables, and RLS

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-06 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "citext";')

    # Tables are created via SQLAlchemy metadata
    from app.db.session import Base
    import app.db.models
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)

    # 2. Row Level Security (RLS) on user tables
    user_owned_tables = [
        "user_profiles",
        "consents",
        "physical_measurements",
        "dietary_preferences",
        "allergies",
        "health_information",
        "uploaded_reports",
        "extracted_lab_results",
        "nutritional_assessments",
        "generated_recommendations",
        "carts",
        "cart_items",
        "orders",
        "order_items",
        "consumption_plans",
        "consumption_logs",
        "progress_records",
        "reminders",
        "chat_sessions",
        "chat_messages",
    ]

    for table in user_owned_tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    from app.db.session import Base
    import app.db.models
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

