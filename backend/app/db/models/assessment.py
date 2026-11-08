from sqlalchemy import Column, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class NutritionalAssessment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "nutritional_assessments"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    report_id = Column(UUID(as_uuid=True), ForeignKey("uploaded_reports.id", ondelete="SET NULL"), nullable=True, index=True)
    measurement_id = Column(UUID(as_uuid=True), ForeignKey("physical_measurements.id", ondelete="SET NULL"), nullable=True)
    diet_pref_id = Column(UUID(as_uuid=True), ForeignKey("dietary_preferences.id", ondelete="SET NULL"), nullable=True)
    rule_set_id = Column(UUID(as_uuid=True), ForeignKey("assessment_rule_sets.id", ondelete="RESTRICT"), nullable=False)
    reference_set_version = Column(String(32), default="v2020.1", nullable=False)
    age_years_at_assessment = Column(Numeric(4, 1), nullable=False)
    life_stage = Column(String(64), nullable=False)
    
    findings = Column(JSONB, default=list, nullable=False)
    nutrient_targets = Column(JSONB, default=dict, nullable=False)
    safety_status = Column(
        Enum("ok", "caution", "refer_to_doctor", "blocked", name="assessment_safety_status_enum"),
        default="ok",
        nullable=False,
        index=True,
    )
    safety_messages = Column(JSONB, default=list, nullable=False)

    user = relationship("User", back_populates="assessments")
    report = relationship("UploadedReport", back_populates="assessments")
    recommendations = relationship("GeneratedRecommendation", back_populates="assessment", cascade="all, delete-orphan")

