from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class GeneratedRecommendation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "generated_recommendations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("nutritional_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    formulation_id = Column(UUID(as_uuid=True), ForeignKey("product_formulations.id", ondelete="CASCADE"), nullable=False, index=True)
    rank = Column(Integer, default=1, nullable=False)
    why_selected = Column(JSONB, default=list, nullable=False)  # Array of {reason_code, detail, source_row_ids, rule_version}
    explanation_text = Column(JSONB, default=dict, nullable=False)  # {en, ta, hi, te, ml}
    saved = Column(Boolean, default=False, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="recommendations")
    assessment = relationship("NutritionalAssessment", back_populates="recommendations")
    formulation = relationship("ProductFormulation", back_populates="recommendations")

