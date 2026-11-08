import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AssessmentCreateRequest(BaseModel):
    report_id: Optional[uuid.UUID] = None
    measurement_id: Optional[uuid.UUID] = None
    diet_pref_id: Optional[uuid.UUID] = None


class FindingItem(BaseModel):
    rule_id: str
    parameter: Optional[str] = None
    observed_value: Optional[Any] = None
    message_key: str
    detail: str


class SafetyMessage(BaseModel):
    severity: str  # critical, refer_to_doctor, caution, advisory
    message_key: str


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    report_id: Optional[uuid.UUID] = None
    age: float
    life_stage: str
    safety_status: str  # ok, caution, refer_to_doctor, blocked
    safe_to_formulate: bool = True
    red_flags: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    rda_targets: Dict[str, Any] = Field(default_factory=dict)
    anaemia_risk: str = "mild"
    findings: List[FindingItem] = Field(default_factory=list)
    safety_messages: List[SafetyMessage] = Field(default_factory=list)
    nutrient_targets: Dict[str, Any] = Field(default_factory=dict)
    rule_version: str = "icmr_v2020.1"
    created_at: datetime

