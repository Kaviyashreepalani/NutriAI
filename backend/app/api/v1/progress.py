import uuid
from datetime import date, datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import check_resource_ownership, get_current_user
from app.core.errors import BadRequestException, NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.progress import (
    ConsumptionPlanResponse,
    DailyLogCreateRequest,
    LabComparisonPoint,
    LabComparisonResponse,
    PlanCreateRequest,
    ProgressOverviewResponse,
    ReminderUpdate,
)

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/plans", response_model=ConsumptionPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_consumption_plan(
    payload: PlanCreateRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = models.ConsumptionPlan(
        user_id=current_user.id,
        formulation_id=payload.formulation_id,
        order_item_id=payload.order_item_id,
        total_servings=payload.total_servings,
        daily_target_servings=payload.daily_target_servings,
        start_date=payload.start_date,
        status="active",
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)

    # Product category name
    cat_stmt = (
        select(models.ProductCategory.name)
        .join(models.ProductFormulation, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.ProductFormulation.id == payload.formulation_id)
    )
    cat_name = (await db.execute(cat_stmt)).scalar_one_or_none() or {"en": "Prototype Formulation"}

    proj_days = int(payload.total_servings / payload.daily_target_servings)
    end_date = payload.start_date + timedelta(days=proj_days)

    return ConsumptionPlanResponse(
        id=plan.id,
        formulation_id=plan.formulation_id,
        product_name=cat_name.get("en", "Prototype Formulation"),
        total_servings=plan.total_servings,
        consumed_servings=0,
        remaining_servings=plan.total_servings,
        completion_pct=0.0,
        daily_target=plan.daily_target_servings,
        start_date=plan.start_date,
        projected_end_date=end_date,
        status=plan.status,
    )


@router.post("/plans/{id}/logs", status_code=status.HTTP_201_CREATED)
async def log_daily_consumption(
    id: uuid.UUID,
    payload: DailyLogCreateRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.ConsumptionPlan).where(models.ConsumptionPlan.id == id)
    res = await db.execute(stmt)
    plan = res.scalar_one_or_none()
    if not plan:
        raise NotFoundException("Consumption Plan", id)

    check_resource_ownership(plan.user_id, current_user)

    # Check unique constraint (plan_id + logged_on)
    existing_stmt = select(models.ConsumptionLog).where(
        models.ConsumptionLog.plan_id == plan.id,
        models.ConsumptionLog.logged_on == payload.logged_on,
    )
    existing_log = (await db.execute(existing_stmt)).scalar_one_or_none()

    if existing_log:
        existing_log.servings_consumed += payload.servings_consumed
        if payload.notes:
            existing_log.notes = payload.notes
    else:
        new_log = models.ConsumptionLog(
            plan_id=plan.id,
            user_id=current_user.id,
            logged_on=payload.logged_on,
            servings_consumed=payload.servings_consumed,
            notes=payload.notes,
        )
        db.add(new_log)

    await db.commit()
    return {"success": True, "message": "Consumption recorded successfully."}


@router.get("/overview", response_model=ProgressOverviewResponse)
async def get_progress_overview(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Active plan
    plan_stmt = (
        select(models.ConsumptionPlan)
        .where(models.ConsumptionPlan.user_id == current_user.id, models.ConsumptionPlan.status == "active")
        .order_by(desc(models.ConsumptionPlan.created_at))
        .limit(1)
    )
    plan = (await db.execute(plan_stmt)).scalar_one_or_none()

    plan_resp = None
    if plan:
        # Sum logs
        consumed_stmt = select(func.sum(models.ConsumptionLog.servings_consumed)).where(models.ConsumptionLog.plan_id == plan.id)
        consumed = (await db.execute(consumed_stmt)).scalar() or 0
        remaining = max(0, plan.total_servings - consumed)
        pct = round(min(100.0, (consumed / plan.total_servings) * 100.0), 1)

        cat_stmt = (
            select(models.ProductCategory.name)
            .join(models.ProductFormulation, models.ProductFormulation.category_id == models.ProductCategory.id)
            .where(models.ProductFormulation.id == plan.formulation_id)
        )
        cat_name = (await db.execute(cat_stmt)).scalar_one_or_none() or {"en": "Prototype Product"}

        proj_days = int(plan.total_servings / (plan.daily_target_servings or 1))
        end_date = plan.start_date + timedelta(days=proj_days)

        plan_resp = ConsumptionPlanResponse(
            id=plan.id,
            formulation_id=plan.formulation_id,
            product_name=cat_name.get("en", "Prototype Formulation"),
            total_servings=plan.total_servings,
            consumed_servings=consumed,
            remaining_servings=remaining,
            completion_pct=pct,
            daily_target=plan.daily_target_servings,
            start_date=plan.start_date,
            projected_end_date=end_date,
            status=plan.status,
        )

    # Weekly adherence (last 7 days logs vs 7 * target)
    seven_days_ago = date.today() - timedelta(days=7)
    recent_logs_stmt = (
        select(models.ConsumptionLog)
        .where(models.ConsumptionLog.user_id == current_user.id, models.ConsumptionLog.logged_on >= seven_days_ago)
        .order_by(desc(models.ConsumptionLog.logged_on))
    )
    recent_logs = (await db.execute(recent_logs_stmt)).scalars().all()
    servings_last_7 = sum(l.servings_consumed for l in recent_logs)
    target_last_7 = (plan.daily_target_servings * 7) if plan else 7
    weekly_adherence = round(min(100.0, (servings_last_7 / target_last_7) * 100.0), 1)

    # All time logs count
    total_logs_stmt = select(func.sum(models.ConsumptionLog.servings_consumed)).where(models.ConsumptionLog.user_id == current_user.id)
    total_servings = (await db.execute(total_logs_stmt)).scalar() or 0

    return ProgressOverviewResponse(
        active_plan=plan_resp,
        weekly_adherence_pct=weekly_adherence,
        total_servings_logged=total_servings,
        recent_logs=[
            {"date": str(l.logged_on), "servings": l.servings_consumed, "notes": l.notes}
            for l in recent_logs[:10]
        ],
        lab_trend_available=True,
    )


@router.get("/lab-comparison", response_model=LabComparisonResponse)
async def get_lab_comparison(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Returns chronological series of confirmed laboratory values for Hb and Ferritin trends."""
    # Find confirmed reports for user
    rep_stmt = (
        select(models.UploadedReport)
        .where(models.UploadedReport.user_id == current_user.id, models.UploadedReport.ocr_status == "confirmed", models.UploadedReport.deleted_at.is_(None))
        .order_by(models.UploadedReport.report_date)
    )
    reports = (await db.execute(rep_stmt)).scalars().all()

    series = []
    for rep in reports:
        dt = rep.report_date or rep.created_at.date()
        # Find HB
        hb_stmt = (
            select(models.ExtractedLabResult.canonical_value, models.ExtractedLabResult.value_numeric)
            .join(models.LabParameter, models.ExtractedLabResult.parameter_id == models.LabParameter.id)
            .where(models.ExtractedLabResult.report_id == rep.id, models.LabParameter.code == "HB")
        )
        hb_res = (await db.execute(hb_stmt)).first()
        hb_val = float(hb_res[0] or hb_res[1]) if hb_res else None

        # Find Ferritin
        ferr_stmt = (
            select(models.ExtractedLabResult.canonical_value, models.ExtractedLabResult.value_numeric)
            .join(models.LabParameter, models.ExtractedLabResult.parameter_id == models.LabParameter.id)
            .where(models.ExtractedLabResult.report_id == rep.id, models.LabParameter.code == "FERRITIN")
        )
        ferr_res = (await db.execute(ferr_stmt)).first()
        ferr_val = float(ferr_res[0] or ferr_res[1]) if ferr_res else None

        if hb_val is not None or ferr_val is not None:
            series.append(LabComparisonPoint(
                date=dt,
                hb_val=hb_val,
                ferritin_val=ferr_val,
                unit="g/dL",
            ))

    return LabComparisonResponse(
        series=series,
        parameters=["HB", "FERRITIN"],
    )


@router.post("/reminders")
@router.patch("/reminders")
async def set_reminder(
    payload: ReminderUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Reminder).where(models.Reminder.user_id == current_user.id)
    reminder = (await db.execute(stmt)).scalar_one_or_none()

    if not reminder:
        reminder = models.Reminder(user_id=current_user.id)
        db.add(reminder)

    reminder.reminder_time = payload.reminder_time
    reminder.is_enabled = payload.is_enabled
    reminder.channel = payload.channel
    await db.commit()

    return {"success": True, "message": "Daily reminder preferences updated."}

