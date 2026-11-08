import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, log_audit_event
from app.db.session import get_db
import app.db.models as models
from app.schemas.profile import (
    AllergiesUpdate,
    DietaryPreferenceUpdate,
    FullProfileResponse,
    HealthInfoUpdate,
    MeasurementCreate,
    MeasurementResponse,
    UserProfileUpdate,
)

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=FullProfileResponse)
async def get_profile(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    profile_stmt = select(models.UserProfile).where(models.UserProfile.user_id == current_user.id)
    profile_res = await db.execute(profile_stmt)
    profile = profile_res.scalar_one_or_none()

    # Latest measurement
    meas_stmt = select(models.PhysicalMeasurement).where(models.PhysicalMeasurement.user_id == current_user.id).order_by(desc(models.PhysicalMeasurement.measured_on)).limit(1)
    meas_res = await db.execute(meas_stmt)
    latest_meas = meas_res.scalar_one_or_none()

    # Dietary preferences
    diet_stmt = select(models.DietaryPreference).where(models.DietaryPreference.user_id == current_user.id).order_by(desc(models.DietaryPreference.effective_from)).limit(1)
    diet_res = await db.execute(diet_stmt)
    latest_diet = diet_res.scalar_one_or_none()

    # Allergies
    allergy_stmt = select(models.Allergy).where(models.Allergy.user_id == current_user.id, models.Allergy.is_active == True)
    allergy_res = await db.execute(allergy_stmt)
    allergies = allergy_res.scalars().all()

    # Health info
    health_stmt = select(models.HealthInformation).where(models.HealthInformation.user_id == current_user.id)
    health_res = await db.execute(health_stmt)
    health = health_res.scalar_one_or_none()

    return FullProfileResponse(
        user_id=current_user.id,
        email=current_user.email,
        preferred_language=current_user.preferred_language,
        date_of_birth=current_user.date_of_birth,
        age=current_user.age,
        full_name=profile.full_name if profile else None,
        sex=profile.sex if profile else "female",
        phone=profile.phone if profile else None,
        address_line=profile.address_line if profile else None,
        city=profile.city if profile else None,
        state=profile.state if profile else None,
        pin_code=profile.pin_code if profile else None,
        profile_completion_pct=profile.profile_completion_pct if profile else 30,
        latest_measurement=MeasurementResponse(
            id=latest_meas.id,
            measured_on=latest_meas.measured_on,
            height_cm=float(latest_meas.height_cm),
            weight_kg=float(latest_meas.weight_kg),
            bmi=float(latest_meas.bmi),
            source=latest_meas.source,
            created_at=latest_meas.created_at,
        ) if latest_meas else None,
        dietary_preferences={
            "diet_type": latest_diet.diet_type,
            "disliked_foods": latest_diet.disliked_foods,
            "favourite_foods": latest_diet.favourite_foods,
            "meals_per_day": latest_diet.meals_per_day,
            "budget_per_serving_inr": float(latest_diet.budget_per_serving_inr),
            "preferred_format_ids": latest_diet.preferred_format_ids,
        } if latest_diet else None,
        allergies=[
            {
                "allergen_code": a.allergen_code,
                "kind": a.kind,
                "severity": a.severity,
                "is_active": a.is_active,
            }
            for a in allergies
        ],
        health_info={
            "known_deficiencies": health.known_deficiencies,
            "pregnancy_status": health.pregnancy_status,
            "diagnoses": health.diagnoses,
            "menstrual_info": health.menstrual_info,
            "supplements": health.supplements,
            "medications": health.medications,
            "notes": health.notes,
        } if health else None,
    )


@router.patch("")
async def update_profile(
    payload: UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.UserProfile).where(models.UserProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalar_one_or_none()
    if not profile:
        profile = models.UserProfile(user_id=current_user.id, full_name=payload.full_name or "User")
        db.add(profile)

    if payload.full_name is not None:
        profile.full_name = payload.full_name
    if payload.phone is not None:
        profile.phone = payload.phone
    if payload.address_line is not None:
        profile.address_line = payload.address_line
    if payload.city is not None:
        profile.city = payload.city
    if payload.state is not None:
        profile.state = payload.state
    if payload.pin_code is not None:
        profile.pin_code = payload.pin_code

    profile.profile_completion_pct = min(100, profile.profile_completion_pct + 15)
    await db.commit()
    return {"success": True, "message": "Profile updated successfully."}


@router.get("/measurements", response_model=List[MeasurementResponse])
async def list_measurements(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.PhysicalMeasurement).where(models.PhysicalMeasurement.user_id == current_user.id).order_by(desc(models.PhysicalMeasurement.measured_on))
    res = await db.execute(stmt)
    records = res.scalars().all()
    return [
        MeasurementResponse(
            id=r.id,
            measured_on=r.measured_on,
            height_cm=float(r.height_cm),
            weight_kg=float(r.weight_kg),
            bmi=float(r.bmi),
            source=r.source,
            created_at=r.created_at,
        )
        for r in records
    ]


@router.post("/measurements", response_model=MeasurementResponse)
async def add_measurement(
    payload: MeasurementCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    h_m = payload.height_cm / 100.0
    bmi = round(payload.weight_kg / (h_m * h_m), 1)

    meas = models.PhysicalMeasurement(
        user_id=current_user.id,
        measured_on=payload.measured_on,
        height_cm=payload.height_cm,
        weight_kg=payload.weight_kg,
        bmi=bmi,
        source=payload.source,
    )
    db.add(meas)
    await db.commit()
    await db.refresh(meas)

    return MeasurementResponse(
        id=meas.id,
        measured_on=meas.measured_on,
        height_cm=float(meas.height_cm),
        weight_kg=float(meas.weight_kg),
        bmi=float(meas.bmi),
        source=meas.source,
        created_at=meas.created_at,
    )


@router.put("/diet")
async def update_dietary_preferences(
    payload: DietaryPreferenceUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    diet = models.DietaryPreference(
        user_id=current_user.id,
        diet_type=payload.diet_type,
        disliked_foods=payload.disliked_foods,
        favourite_foods=payload.favourite_foods,
        meals_per_day=payload.meals_per_day,
        eating_pattern_notes=payload.eating_pattern_notes,
        budget_per_serving_inr=payload.budget_per_serving_inr,
        preferred_format_ids=payload.preferred_format_ids,
        effective_from=datetime.now(timezone.utc),
    )
    db.add(diet)
    await db.commit()
    return {"success": True, "message": "Dietary preferences updated."}


@router.put("/allergies")
async def update_allergies(
    payload: AllergiesUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Deactivate prior allergies
    stmt = select(models.Allergy).where(models.Allergy.user_id == current_user.id)
    res = await db.execute(stmt)
    for old_a in res.scalars().all():
        old_a.is_active = False

    # Insert new active allergies
    for item in payload.allergies:
        allergy = models.Allergy(
            user_id=current_user.id,
            allergen_code=item.allergen_code,
            kind=item.kind,
            severity=item.severity,
            is_active=item.is_active,
        )
        db.add(allergy)

    await db.commit()
    return {"success": True, "message": "Allergens and restrictions saved."}


@router.put("/health")
async def update_health_information(
    payload: HealthInfoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.HealthInformation).where(models.HealthInformation.user_id == current_user.id)
    res = await db.execute(stmt)
    health = res.scalar_one_or_none()

    if not health:
        health = models.HealthInformation(user_id=current_user.id)
        db.add(health)

    health.known_deficiencies = payload.known_deficiencies
    health.pregnancy_status = payload.pregnancy_status
    if payload.diagnoses is not None:
        health.diagnoses = payload.diagnoses
    if payload.menstrual_info is not None:
        health.menstrual_info = payload.menstrual_info
    if payload.supplements is not None:
        health.supplements = payload.supplements
    if payload.medications is not None:
        health.medications = payload.medications
    if payload.notes is not None:
        health.notes = payload.notes

    await db.commit()
    return {"success": True, "message": "Health information securely updated."}

