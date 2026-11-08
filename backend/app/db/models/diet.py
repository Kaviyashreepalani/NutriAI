from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class DietaryPreference(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "dietary_preferences"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    diet_type = Column(
        Enum("vegetarian", "eggetarian", "non_vegetarian", "vegan", "jain", "other", name="diet_type_enum"),
        default="vegetarian",
        nullable=False,
    )
    disliked_foods = Column(ARRAY(String), default=list, nullable=False)
    favourite_foods = Column(ARRAY(String), default=list, nullable=False)
    meals_per_day = Column(Integer, default=3, nullable=False)
    eating_pattern_notes = Column(Text, nullable=True)
    budget_per_serving_inr = Column(Numeric(6, 2), default=25.0, nullable=False)
    preferred_format_ids = Column(ARRAY(String), default=list, nullable=False)
    effective_from = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="dietary_preferences")

