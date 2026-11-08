from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin


class LabParameter(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lab_parameters"

    code = Column(String(32), unique=True, nullable=False, index=True)
    display_name = Column(JSONB, nullable=False)  # {"en": "Haemoglobin", "ta": "ஹீமோகுளோபின்", "hi": "हीमोग्लोबिन", ...}
    canonical_unit = Column(String(32), nullable=False)
    allowed_units = Column(JSONB, nullable=False)  # {"g/dL": 1.0, "g/L": 0.1}
    plausible_min = Column(Numeric(10, 2), nullable=False)
    plausible_max = Column(Numeric(10, 2), nullable=False)
    aliases = Column(ARRAY(String), default=list, nullable=False)

    extracted_results = relationship("ExtractedLabResult", back_populates="parameter")


class ExtractedLabResult(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "extracted_lab_results"

    report_id = Column(UUID(as_uuid=True), ForeignKey("uploaded_reports.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parameter_id = Column(UUID(as_uuid=True), ForeignKey("lab_parameters.id", ondelete="SET NULL"), nullable=True, index=True)
    
    raw_name = Column(String(255), nullable=False)
    raw_value = Column(String(128), nullable=False)
    value_numeric = Column(Numeric(10, 2), nullable=True)
    unit = Column(String(64), nullable=True)
    canonical_value = Column(Numeric(10, 2), nullable=True)
    ref_low = Column(Numeric(10, 2), nullable=True)
    ref_high = Column(Numeric(10, 2), nullable=True)
    flag = Column(String(32), default="NORMAL", nullable=False)  # LOW, NORMAL, HIGH, CRITICAL_LOW, CRITICAL_HIGH, UNKNOWN
    ocr_confidence = Column(Numeric(5, 4), default=1.0, nullable=False)
    needs_review = Column(Boolean, default=False, nullable=False, index=True)
    user_corrected = Column(Boolean, default=False, nullable=False)
    original_ocr_value = Column(Text, nullable=True)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)

    report = relationship("UploadedReport", back_populates="extracted_results")
    parameter = relationship("LabParameter", back_populates="extracted_results")

