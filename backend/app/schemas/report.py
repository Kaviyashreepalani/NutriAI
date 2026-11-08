import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ExtractedResultResponse(BaseModel):
    id: uuid.UUID
    parameter_code: Optional[str] = None
    parameter_name: Optional[str] = None
    raw_name: str
    raw_value: str
    value_numeric: Optional[float] = None
    unit: Optional[str] = None
    canonical_value: Optional[float] = None
    ref_low: Optional[float] = None
    ref_high: Optional[float] = None
    flag: str
    ocr_confidence: float
    needs_review: bool
    user_corrected: bool
    original_ocr_value: Optional[str] = None


class ExtractedResultCorrection(BaseModel):
    id: uuid.UUID
    value_numeric: float
    unit: Optional[str] = None
    parameter_code: Optional[str] = None


class BatchCorrectionsRequest(BaseModel):
    corrections: List[ExtractedResultCorrection]
    report_date: Optional[Union[date, str]] = None
    lab_name: Optional[str] = None


class ReportSummaryResponse(BaseModel):
    id: uuid.UUID
    report_id: Optional[uuid.UUID] = None
    original_filename: str
    mime_type: str
    size_bytes: int
    report_date: Optional[Union[date, str]] = None
    lab_name: Optional[str] = None
    ocr_status: str
    uploaded_at: datetime
    results_count: int = 0
    needs_review_count: int = 0

    def model_post_init(self, __context):
        if self.report_id is None:
            self.report_id = self.id


class ReportDetailResponse(ReportSummaryResponse):
    results: List[ExtractedResultResponse] = Field(default_factory=list)
    extracted_results: List[ExtractedResultResponse] = Field(default_factory=list)

    def model_post_init(self, __context):
        super().model_post_init(__context)
        if not self.extracted_results and self.results:
            self.extracted_results = self.results

