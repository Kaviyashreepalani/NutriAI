import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlanCreateRequest(BaseModel):
    order_item_id: Optional[uuid.UUID] = None
    formulation_id: uuid.UUID
    total_servings: int = Field(default=14, ge=1, le=120)
    daily_target_servings: int = Field(default=1, ge=1, le=5)
    start_date: date = Field(default_factory=date.today)


class DailyLogCreateRequest(BaseModel):
    logged_on: date = Field(default_factory=date.today)
    servings_consumed: int = Field(default=1, ge=1, le=10)
    notes: Optional[str] = None


class ConsumptionPlanResponse(BaseModel):
    id: uuid.UUID
    formulation_id: uuid.UUID
    product_name: str
    total_servings: int
    consumed_servings: int
    remaining_servings: int
    completion_pct: float
    daily_target: int
    start_date: date
    projected_end_date: date
    status: str


class ProgressOverviewResponse(BaseModel):
    active_plan: Optional[ConsumptionPlanResponse] = None
    weekly_adherence_pct: float
    total_servings_logged: int
    recent_logs: List[Dict[str, Any]] = Field(default_factory=list)
    lab_trend_available: bool = False
    disclaimer: str = (
        "Changes in laboratory parameters must not be attributed solely to NutriAI products "
        "and should be evaluated by a qualified healthcare professional."
    )


class LabComparisonPoint(BaseModel):
    date: date
    hb_val: Optional[float] = None
    ferritin_val: Optional[float] = None
    unit: str = "g/dL"


class LabComparisonResponse(BaseModel):
    series: List[LabComparisonPoint]
    parameters: List[str]


class ReminderUpdate(BaseModel):
    reminder_time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # HH:MM
    is_enabled: bool = True
    channel: str = Field(default="in_app", pattern="^(in_app|email)$")

