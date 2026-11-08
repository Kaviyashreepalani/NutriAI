from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class Allergy(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "allergies"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    allergen_code = Column(String(64), nullable=False, index=True)
    kind = Column(Enum("allergy", "intolerance", "restriction", name="allergy_kind_enum"), default="allergy", nullable=False)
    severity = Column(String(32), default="moderate", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    recorded_on = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="allergies")

