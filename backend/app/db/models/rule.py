from sqlalchemy import Column, Date, DateTime, Enum, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class NutrientReferenceValue(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "nutrient_reference_values"

    nutrient_code = Column(String(32), nullable=False, index=True)
    life_stage = Column(String(64), nullable=False, index=True)  # girl_10_12, girl_13_15, girl_16_18, woman_19_35, woman_36_49, pregnancy, lactation
    value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(32), nullable=False)
    source_document = Column(String(255), default="ICMR-NIN RDA 2020", nullable=False)
    source_page = Column(String(64), nullable=True)
    version = Column(String(32), default="v2020.1", nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    reviewed_by = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum("draft", "expert_approved", name="nutrient_ref_status_enum"), default="draft", nullable=False)


class AssessmentRuleSet(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "assessment_rule_sets"

    version = Column(String(32), unique=True, nullable=False, index=True)
    rules = Column(JSONB, nullable=False)
    status = Column(Enum("draft", "expert_approved", "retired", name="rule_set_status_enum"), default="draft", nullable=False)
    approved_by = Column(String(255), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

