from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.errors import NotFoundException
from app.db.session import get_db
import app.db.models as models

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "NutriAI Backend",
        "environment": settings.APP_ENV,
        "platform": settings.DATA_PLATFORM,
        "auth_provider": settings.AUTH_PROVIDER,
        "storage_provider": settings.STORAGE_PROVIDER,
    }


@router.get("/public/statistics")
async def get_public_statistics(db: AsyncSession = Depends(get_db)):
    """Returns only VERIFIED statistics for the public homepage.

    Unverified items display as pending verification.
    """
    stmt = select(models.Statistic).where(models.Statistic.status == "verified")
    res = await db.execute(stmt)
    stats = res.scalars().all()

    items = []
    for s in stats:
        items.append({
            "id": str(s.id),
            "metric_name": s.metric_name,
            "value": float(s.value) if s.value is not None else None,
            "unit": s.unit,
            "population_group": s.population_group,
            "survey_name": s.survey_name,
            "survey_year": s.survey_year,
            "definition": s.definition,
            "status": s.status,
        })

    # Also check if any pending statistics exist
    pending_stmt = select(models.Statistic).where(models.Statistic.status == "pending")
    pending_res = await db.execute(pending_stmt)
    pending_count = len(pending_res.scalars().all())

    return {
        "verified_statistics": items,
        "pending_verification_count": pending_count,
        "disclaimer": "All displayed metrics are cited from published national surveys (NFHS-5, ICMR-NIN).",
    }


@router.get("/public/products/categories")
async def get_product_categories(db: AsyncSession = Depends(get_db)):
    stmt = select(models.ProductCategory)
    res = await db.execute(stmt)
    cats = res.scalars().all()
    return [
        {
            "id": str(c.id),
            "slug": c.slug,
            "name": c.name,
            "description": c.description,
            "format_template": c.format_template,
            "badge": "Prototype concept – not validated",
        }
        for c in cats
    ]


@router.post("/public/contact")
async def submit_contact_form(data: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    msg = models.ContactMessage(
        name=data.get("name", "Anonymous"),
        email=data.get("email", ""),
        subject=data.get("subject", "General Inquiry"),
        message=data.get("message", ""),
    )
    db.add(msg)
    await db.commit()
    return {"success": True, "message": "Inquiry recorded successfully. Our team will review it."}


@router.get("/education")
async def list_educational_modules(db: AsyncSession = Depends(get_db)):
    stmt = select(models.EducationalContent).where(models.EducationalContent.status == "published")
    res = await db.execute(stmt)
    modules = res.scalars().all()
    return [
        {
            "id": str(m.id),
            "slug": m.slug,
            "title": m.title,
            "category": m.category,
            "translation_review_status": m.translation_review_status,
        }
        for m in modules
    ]


@router.get("/education/{slug}")
async def get_educational_module(slug: str, db: AsyncSession = Depends(get_db)):
    stmt = select(models.EducationalContent).where(models.EducationalContent.slug == slug)
    res = await db.execute(stmt)
    module = res.scalar_one_or_none()
    if not module:
        raise NotFoundException("Educational Content", slug)

    return {
        "id": str(module.id),
        "slug": module.slug,
        "title": module.title,
        "category": module.category,
        "body": module.body,
        "status": module.status,
        "translation_review_status": module.translation_review_status,
        "references": module.references_list,
    }

