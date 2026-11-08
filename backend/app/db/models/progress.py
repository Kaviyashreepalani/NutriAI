from datetime import date
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class ConsumptionPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "consumption_plans"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="RESTRICT"), nullable=False)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("order_items.id", ondelete="SET NULL"), nullable=True)
    total_servings = Column(Integer, default=14, nullable=False)
    daily_target_servings = Column(Integer, default=1, nullable=False)
    start_date = Column(Date, default=date.today, nullable=False)
    status = Column(String(32), default="active", nullable=False)  # active, completed, paused

    user = relationship("User", back_populates="consumption_plans")
    formulation = relationship("ProductFormulation")
    logs = relationship("ConsumptionLog", back_populates="plan", cascade="all, delete-orphan")


class ConsumptionLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "consumption_logs"
    __table_args__ = (
        UniqueConstraint("plan_id", "logged_on", name="uq_plan_logged_on"),
    )

    plan_id = Column(UUID(as_uuid=True), ForeignKey("consumption_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    logged_on = Column(Date, default=date.today, nullable=False, index=True)
    servings_consumed = Column(Integer, default=1, nullable=False)
    notes = Column(Text, nullable=True)

    plan = relationship("ConsumptionPlan", back_populates="logs")


class ProgressRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "progress_records"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_date = Column(Date, default=date.today, nullable=False)
    adherence_pct = Column(Numeric(5, 2), nullable=False)
    total_servings_consumed = Column(Integer, default=0, nullable=False)
    metrics_snapshot = Column(JSONB, default=dict, nullable=False)


class Reminder(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reminders"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reminder_time = Column(String(8), default="09:00", nullable=False)  # HH:MM
    is_enabled = Column(Boolean, default=True, nullable=False)
    channel = Column(String(32), default="in_app", nullable=False)  # in_app, email

