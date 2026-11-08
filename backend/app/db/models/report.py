from sqlalchemy import BigInteger, Column, Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.models.base_mixin import UUIDMixin, TimestampMixin, SoftDeleteMixin


class UploadedReport(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "uploaded_reports"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    storage_key = Column(String(512), nullable=False)
    original_filename = Column(String(255), nullable=False)
    mime_type = Column(String(64), nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    sha256 = Column(String(64), nullable=False, index=True)
    report_date = Column(Date, nullable=True)
    lab_name = Column(String(255), nullable=True)
    ocr_engine = Column(String(64), default="pymupdf_pdfplumber", nullable=False)
    ocr_status = Column(
        Enum("uploaded", "processing", "needs_review", "confirmed", "failed", name="ocr_status_enum"),
        default="uploaded",
        nullable=False,
        index=True,
    )
    raw_ocr = Column(JSONB, default=dict, nullable=False)

    user = relationship("User", back_populates="reports")
    extracted_results = relationship("ExtractedLabResult", back_populates="report", cascade="all, delete-orphan")
    assessments = relationship("NutritionalAssessment", back_populates="report")

