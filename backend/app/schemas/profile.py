import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=32)
    address_line: Optional[str] = None
    city: Optional[str] = Field(default=None, max_length=128)
    state: Optional[str] = Field(default=None, max_length=128)
    pin_code: Optional[str] = Field(default=None, pattern=r"^[1-9][0-9]{5}$")


class MeasurementCreate(BaseModel):
    measured_on: date = Field(default_factory=date.today)
    height_cm: float = Field(ge=30.0, le=250.0)
    weight_kg: float = Field(ge=10.0, le=250.0)
    source: str = Field(default="user_entry")


class MeasurementResponse(BaseModel):
    id: uuid.UUID
    measured_on: date
    height_cm: float
    weight_kg: float
    bmi: float
    source: str
    created_at: datetime


class DietaryPreferenceUpdate(BaseModel):
    diet_type: str = Field(pattern="^(vegetarian|eggetarian|non_vegetarian|vegan|jain|other)$")
    disliked_foods: List[str] = Field(default_factory=list)
    favourite_foods: List[str] = Field(default_factory=list)
    meals_per_day: int = Field(default=3, ge=1, le=8)
    eating_pattern_notes: Optional[str] = None
    budget_per_serving_inr: float = Field(default=25.0, ge=5.0, le=500.0)
    preferred_format_ids: List[str] = Field(default_factory=list)


class AllergyItem(BaseModel):
    allergen_code: str = Field(max_length=64)
    kind: str = Field(default="allergy", pattern="^(allergy|intolerance|restriction)$")
    severity: str = Field(default="moderate")
    is_active: bool = True


class AllergiesUpdate(BaseModel):
    allergies: List[AllergyItem]


class HealthInfoUpdate(BaseModel):
    known_deficiencies: List[str] = Field(default_factory=list)
    pregnancy_status: str = Field(default="not_pregnant")
    diagnoses: Optional[str] = None
    menstrual_info: Optional[Dict[str, Any]] = None
    supplements: Optional[List[Dict[str, Any]]] = None
    medications: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class FullProfileResponse(BaseModel):
    user_id: uuid.UUID
    email: str
    preferred_language: str
    date_of_birth: date
    age: int
    full_name: Optional[str] = None
    sex: str = "female"
    phone: Optional[str] = None
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None
    profile_completion_pct: int = 0
    latest_measurement: Optional[MeasurementResponse] = None
    dietary_preferences: Optional[Dict[str, Any]] = None
    allergies: List[Dict[str, Any]] = Field(default_factory=list)
    health_info: Optional[Dict[str, Any]] = None

