from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class Consent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "consents"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_type = Column(Enum("self", "guardian", name="consent_subject_type_enum"), default="self", nullable=False)
    guardian_name = Column(String(255), nullable=True)
    guardian_relation = Column(String(64), nullable=True)
    guardian_contact = Column(String(64), nullable=True)
    purpose = Column(
        Enum("data_processing", "health_data", "report_ocr", "chatbot", name="consent_purpose_enum"),
        nullable=False,
    )
    granted = Column(Boolean, default=True, nullable=False)
    policy_version = Column(String(32), default="v1.0", nullable=False)
    granted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="consents")

