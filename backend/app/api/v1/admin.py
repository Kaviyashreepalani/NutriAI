import uuid
from datetime import date, datetime, timezone
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, log_audit_event, require_role
from app.core.errors import NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.admin import (
    IngredientCreateUpdate,
    OrderStatusUpdateRequest,
    StatisticVerifyRequest,
)

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role(["admin", "nutritionist"]))])


# 1. Ingredients Management
@router.get("/ingredients")
async def list_admin_ingredients(db: AsyncSession = Depends(get_db)):
    stmt = select(models.Ingredient).order_by(models.Ingredient.name)
    ings = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(i.id),
            "name": i.name,
            "category": i.category,
            "diet_class": i.diet_class,
            "allergens": i.allergens,
            "cost_per_kg_inr": float(i.cost_per_kg_inr),
            "data_status": i.data_status,
        }
        for i in ings
    ]


@router.post("/ingredients", status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    payload: IngredientCreateUpdate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ing = models.Ingredient(
        name=payload.name,
        local_names=payload.local_names,
        category=payload.category,
        diet_class=payload.diet_class,
        allergens=payload.allergens,
        cost_per_kg_inr=payload.cost_per_kg_inr,
        cost_as_of=date.today(),
        availability=payload.availability,
        min_inclusion_pct=payload.min_inclusion_pct,
        max_inclusion_pct=payload.max_inclusion_pct,
        data_status=payload.data_status,
    )
    db.add(ing)
    await db.flush()

    for nut_code, amount in payload.nutrients.items():
        nut = models.IngredientNutrient(
            ingredient_id=ing.id,
            nutrient_code=nut_code,
            amount_per_100g=amount,
            unit="mg",
            source="ICMR_NIN" if payload.data_status == "verified" else "PLACEHOLDER_DEMO",
            verified_by=current_user.email if payload.data_status == "verified" else None,
            verified_at=datetime.now(timezone.utc) if payload.data_status == "verified" else None,
        )
        db.add(nut)

    await db.commit()
    return {"success": True, "id": str(ing.id), "message": "Ingredient registered."}


# 2. Statistics Verification
@router.get("/statistics")
async def list_admin_statistics(db: AsyncSession = Depends(get_db)):
    stmt = select(models.Statistic)
    stats = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(s.id),
            "metric_name": s.metric_name,
            "value": float(s.value) if s.value is not None else None,
            "unit": s.unit,
            "population_group": s.population_group,
            "survey_name": s.survey_name,
            "survey_year": s.survey_year,
            "status": s.status,
        }
        for s in stats
    ]


@router.patch("/statistics/{id}")
async def verify_and_publish_statistic(
    id: uuid.UUID,
    payload: StatisticVerifyRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Statistic).where(models.Statistic.id == id)
    stat = (await db.execute(stmt)).scalar_one_or_none()
    if not stat:
        raise NotFoundException("Statistic", id)

    stat.value = payload.value
    stat.status = payload.status

    if payload.citation:
        ref = models.ReferenceCatalog(citation=payload.citation, year=2024)
        db.add(ref)
        await db.flush()
        stat.reference_id = ref.id

    await db.commit()

    await log_audit_event(
        db,
        current_user.id,
        action="statistic_verified",
        resource_type="statistics",
        resource_id=str(stat.id),
        details={"metric": stat.metric_name, "value": payload.value},
    )

    return {"success": True, "message": "Statistic verified and published to public homepage."}


# 3. Order Lifecycle Advancement
@router.patch("/orders/{id}/status")
async def advance_order_status(
    id: uuid.UUID,
    payload: OrderStatusUpdateRequest,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.Order).where(models.Order.id == id)
    order = (await db.execute(stmt)).scalar_one_or_none()
    if not order:
        raise NotFoundException("Order", id)

    order.status = payload.status
    event = models.OrderStatusEvent(
        order_id=order.id,
        status=payload.status,
        note=payload.note or f"Order advanced to {payload.status} by admin {current_user.email}.",
    )
    db.add(event)
    await db.commit()

    return {"success": True, "message": f"Order status updated to {payload.status}."}


# 4. Audit Trail
@router.get("/audit-logs")
async def list_audit_logs(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.AuditLog).order_by(desc(models.AuditLog.created_at)).limit(limit)
    logs = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(l.id),
            "user_id": str(l.user_id) if l.user_id else None,
            "action": l.action,
            "resource_type": l.resource_type,
            "resource_id": l.resource_id,
            "details": l.details,
            "ip_address": l.ip_address,
            "created_at": l.created_at,
        }
        for l in logs
    ]

