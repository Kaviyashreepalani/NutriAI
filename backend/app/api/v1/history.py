from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.db.session import get_db
import app.db.models as models

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/products")
async def get_products_history(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.GeneratedRecommendation, models.ProductFormulation, models.ProductCategory)
        .join(models.ProductFormulation, models.GeneratedRecommendation.formulation_id == models.ProductFormulation.id)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.GeneratedRecommendation.user_id == current_user.id)
        .order_by(desc(models.GeneratedRecommendation.generated_at))
    )
    res = await db.execute(stmt)
    rows = res.all()

    return [
        {
            "recommendation_id": str(rec.id),
            "formulation_id": str(form.id),
            "formulation_code": form.formulation_code,
            "category_name": cat.name,
            "category_slug": cat.slug,
            "serving_size_g": float(form.serving_size_g),
            "cost_per_serving_inr": float(form.cost_per_serving_inr),
            "nutrient_summary": form.nutrient_results_per_serving,
            "rank": rec.rank,
            "saved": rec.saved,
            "generated_at": rec.generated_at,
        }
        for rec, form, cat in rows
    ]


@router.get("/reports")
async def get_reports_history(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.UploadedReport)
        .where(models.UploadedReport.user_id == current_user.id, models.UploadedReport.deleted_at.is_(None))
        .order_by(desc(models.UploadedReport.created_at))
    )
    reports = (await db.execute(stmt)).scalars().all()

    items = []
    for r in reports:
        # Load extracted items
        res_stmt = (
            select(models.ExtractedLabResult, models.LabParameter.code)
            .outerjoin(models.LabParameter, models.ExtractedLabResult.parameter_id == models.LabParameter.id)
            .where(models.ExtractedLabResult.report_id == r.id)
        )
        res_items = (await db.execute(res_stmt)).all()

        items.append({
            "id": str(r.id),
            "original_filename": r.original_filename,
            "report_date": r.report_date,
            "lab_name": r.lab_name,
            "ocr_status": r.ocr_status,
            "uploaded_at": r.created_at,
            "results": [
                {
                    "parameter": p_code or elr.raw_name,
                    "value": float(elr.canonical_value or elr.value_numeric or 0),
                    "unit": elr.unit,
                    "flag": elr.flag,
                    "user_corrected": elr.user_corrected,
                }
                for elr, p_code in res_items
            ],
        })

    return items


@router.get("/orders")
async def get_orders_history(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.Order)
        .where(models.Order.user_id == current_user.id)
        .order_by(desc(models.Order.created_at))
    )
    orders = (await db.execute(stmt)).scalars().all()

    return [
        {
            "id": str(o.id),
            "order_number": o.order_number,
            "status": o.status,
            "total": float(o.total),
            "payment_mode": o.payment_mode,
            "created_at": o.created_at,
        }
        for o in orders
    ]


@router.get("/progress")
async def get_progress_history(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.ConsumptionLog, models.ConsumptionPlan)
        .join(models.ConsumptionPlan, models.ConsumptionLog.plan_id == models.ConsumptionPlan.id)
        .where(models.ConsumptionLog.user_id == current_user.id)
        .order_by(desc(models.ConsumptionLog.logged_on))
    )
    rows = (await db.execute(stmt)).all()

    return [
        {
            "id": str(log.id),
            "logged_on": log.logged_on,
            "servings_consumed": log.servings_consumed,
            "notes": log.notes,
            "plan_id": str(plan.id),
        }
        for log, plan in rows
    ]

