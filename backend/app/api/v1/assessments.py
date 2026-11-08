import uuid
from datetime import datetime, timezone
from typing import Dict, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import check_resource_ownership, get_current_user, log_audit_event
from app.core.config import settings
from app.core.errors import BadRequestException, NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.assessment import AssessmentCreateRequest, AssessmentResponse
from app.services.assessment.evaluator import (
    DEFAULT_SAFETY_RULES,
    determine_life_stage,
    evaluate_clinical_safety,
)
from app.api.v1.reports import DEV_REPORTS

router = APIRouter(prefix="/assessments", tags=["assessments"])

DEV_ASSESSMENTS: Dict[uuid.UUID, AssessmentResponse] = {}


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    payload: AssessmentCreateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Executes deterministic clinical safety gate and generates personalized nutrient targets."""
    # 1. Determine Life Stage from DOB
    life_stage, age_years = determine_life_stage(current_user.date_of_birth)

    rule_dict = DEFAULT_SAFETY_RULES
    rule_version = "icmr_v2020.1"
    rule_set_id = uuid.uuid4()

    if db is not None:
        try:
            rule_stmt = select(models.AssessmentRuleSet).order_by(desc(models.AssessmentRuleSet.created_at)).limit(1)
            rule_res = await db.execute(rule_stmt)
            rule_set_obj = rule_res.scalar_one_or_none()
            if rule_set_obj:
                rule_dict = rule_set_obj.rules
                rule_version = rule_set_obj.version
                rule_set_id = rule_set_obj.id
        except Exception:
            pass

    # 3. Collect Lab Results if report provided
    lab_results: Dict[str, float] = {}
    if payload.report_id:
        if payload.report_id in DEV_REPORTS:
            for item in DEV_REPORTS[payload.report_id]["results"]:
                if item.parameter_code:
                    val = item.canonical_value if item.canonical_value is not None else item.value_numeric
                    if val is not None:
                        lab_results[item.parameter_code] = float(val)
        elif db is not None:
            try:
                stmt = (
                    select(models.ExtractedLabResult, models.LabParameter.code)
                    .join(models.LabParameter, models.ExtractedLabResult.parameter_id == models.LabParameter.id)
                    .where(models.ExtractedLabResult.report_id == payload.report_id)
                )
                res = await db.execute(stmt)
                for r, code in res.all():
                    val = r.canonical_value or r.value_numeric
                    if val is not None and code:
                        lab_results[code] = float(val)
            except Exception:
                pass

    pregnancy_status = "not_pregnant"
    if db is not None:
        try:
            health_stmt = select(models.HealthInformation).where(models.HealthInformation.user_id == current_user.id)
            health_res = await db.execute(health_stmt)
            health = health_res.scalar_one_or_none()
            if health:
                pregnancy_status = health.pregnancy_status
        except Exception:
            pass

    # 5. Execute Deterministic Evaluation
    evaluation = evaluate_clinical_safety(
        age=age_years,
        life_stage=life_stage,
        lab_results=lab_results,
        pregnancy_status=pregnancy_status,
        rule_set=rule_dict,
    )

    safety_status = evaluation["safety_status"]
    safe_to_formulate = safety_status in ["ok", "caution"] or settings.ALLOW_GENERATION_WITH_REFERRAL

    red_flags = [f["detail"] for f in evaluation["findings"] if "CRITICAL" in f.get("rule_id", "")]
    warnings = [f["detail"] for f in evaluation["findings"] if "CRITICAL" not in f.get("rule_id", "")]
    anaemia_risk = "severe" if safety_status == "blocked" else ("moderate" if safety_status == "refer_to_doctor" else ("mild" if safety_status == "caution" else "low"))

    now = datetime.now(timezone.utc)
    assessment_id = uuid.uuid4()

    response = AssessmentResponse(
        id=assessment_id,
        user_id=current_user.id,
        report_id=payload.report_id,
        age=float(age_years),
        life_stage=life_stage or "adolescent_girl",
        safety_status=safety_status,
        safe_to_formulate=safe_to_formulate,
        red_flags=red_flags,
        warnings=warnings,
        rda_targets=evaluation["nutrient_targets"],
        anaemia_risk=anaemia_risk,
        findings=evaluation["findings"],
        safety_messages=evaluation["safety_messages"],
        nutrient_targets=evaluation["nutrient_targets"],
        rule_version=rule_version,
        created_at=now,
    )
    DEV_ASSESSMENTS[assessment_id] = response

    if db is not None:
        try:
            assessment = models.NutritionalAssessment(
                id=assessment_id,
                user_id=current_user.id,
                report_id=payload.report_id,
                measurement_id=payload.measurement_id,
                diet_pref_id=payload.diet_pref_id,
                rule_set_id=rule_set_id,
                reference_set_version=rule_version,
                age_years_at_assessment=age_years,
                life_stage=life_stage or "out_of_scope",
                findings=evaluation["findings"],
                nutrient_targets=evaluation["nutrient_targets"],
                safety_status=safety_status,
                safety_messages=evaluation["safety_messages"],
            )
            db.add(assessment)
            await db.commit()
        except Exception:
            pass

    return response


@router.get("/{id}", response_model=AssessmentResponse)
async def get_assessment(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: Optional[AsyncSession] = Depends(get_db),
):
    if id in DEV_ASSESSMENTS:
        return DEV_ASSESSMENTS[id]

    if db is None:
        raise NotFoundException("Nutritional Assessment", id)

    stmt = select(models.NutritionalAssessment).where(models.NutritionalAssessment.id == id)
    res = await db.execute(stmt)
    assessment = res.scalar_one_or_none()

    if not assessment:
        raise NotFoundException("Nutritional Assessment", id)

    check_resource_ownership(assessment.user_id, current_user)

    safe_to_formulate = assessment.safety_status in ["ok", "caution"] or settings.ALLOW_GENERATION_WITH_REFERRAL
    red_flags = [f["detail"] for f in assessment.findings if "CRITICAL" in f.get("rule_id", "")]
    warnings = [f["detail"] for f in assessment.findings if "CRITICAL" not in f.get("rule_id", "")]

    return AssessmentResponse(
        id=assessment.id,
        user_id=assessment.user_id,
        report_id=assessment.report_id,
        age=float(assessment.age_years_at_assessment),
        life_stage=assessment.life_stage,
        safety_status=assessment.safety_status,
        safe_to_formulate=safe_to_formulate,
        red_flags=red_flags,
        warnings=warnings,
        rda_targets=assessment.nutrient_targets,
        anaemia_risk="mild",
        findings=assessment.findings,
        safety_messages=assessment.safety_messages,
        nutrient_targets=assessment.nutrient_targets,
        rule_version=assessment.reference_set_version,
        created_at=assessment.created_at,
    )
