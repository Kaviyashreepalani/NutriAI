import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FormulationGenerateRequest(BaseModel):
    assessment_id: Optional[uuid.UUID] = None
    report_id: Optional[uuid.UUID] = None
    preferred_format_slugs: Optional[List[str]] = None
    max_budget_per_serving: Optional[float] = None


class FormulationIngredientItem(BaseModel):
    ingredient_id: Optional[uuid.UUID] = None
    name: str
    local_names: Dict[str, str] = Field(default_factory=dict)
    grams_per_serving: float
    pct_of_mix: float
    purpose: str
    rationale_code: Optional[str] = None


class WhySelectedReason(BaseModel):
    reason_code: str
    detail: str
    rule_version: str


class FormulationResponse(BaseModel):
    id: uuid.UUID
    formulation_code: str
    version: int
    category_slug: str
    category_name: Dict[str, str]
    serving_size_g: float
    cost_per_serving_inr: float
    cost_per_pack_inr: float
    pack_size_servings: int
    ingredients: List[FormulationIngredientItem] = Field(default_factory=list)
    nutrient_results_per_serving: Dict[str, Any] = Field(default_factory=dict)
    bioavailability: Dict[str, Any] = Field(default_factory=dict)
    why_selected: List[WhySelectedReason] = Field(default_factory=list)
    explanation_text: Dict[str, str] = Field(default_factory=dict)
    validation_status: str
    data_status_banner: str = "Demo nutrient data – not validated"
    preparation_instructions: Dict[str, str] = Field(default_factory=dict)
    storage_instructions: Dict[str, str] = Field(default_factory=dict)
    is_saved: bool = False
    rank: int = 1


class RecommendationDetailResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    formulation: FormulationResponse
    rank: int
    saved: bool
    generated_at: datetime


class CompareFormulationsResponse(BaseModel):
    formulations: List[FormulationResponse]

