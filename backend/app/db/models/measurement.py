from sqlalchemy import Column, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class PhysicalMeasurement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "physical_measurements"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    measured_on = Column(Date, nullable=False)
    height_cm = Column(Numeric(5, 2), nullable=False)  # 30 - 250
    weight_kg = Column(Numeric(5, 2), nullable=False)  # 10 - 250
    bmi = Column(Numeric(4, 2), nullable=False)        # Computed (weight / (height_m^2))
    source = Column(String(64), default="user_entry", nullable=False)

    user = relationship("User", back_populates="measurements")

