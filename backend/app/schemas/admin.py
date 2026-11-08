import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class IngredientCreateUpdate(BaseModel):
    name: str
    local_names: Dict[str, str] = Field(default_factory=dict)
    category: str
    diet_class: str = "vegan"
    allergens: List[str] = Field(default_factory=list)
    cost_per_kg_inr: float
    availability: str = "high"
    min_inclusion_pct: float = 0.0
    max_inclusion_pct: float = 100.0
    data_status: str = "draft"
    nutrients: Dict[str, float] = Field(default_factory=dict)


class StatisticVerifyRequest(BaseModel):
    value: float
    citation: Optional[str] = None
    status: str = Field(default="verified", pattern="^(verified|pending)$")


class OrderStatusUpdateRequest(BaseModel):
    status: str = Field(pattern="^(pending|confirmed|processing|shipped|delivered|cancelled)$")
    note: Optional[str] = None

