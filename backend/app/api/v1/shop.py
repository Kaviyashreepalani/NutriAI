import uuid
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import NotFoundException
from app.db.session import get_db
import app.db.models as models

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("/products")
async def list_shop_products(db: AsyncSession = Depends(get_db)):
    """Catalog of prototype products formulated for anaemia prevention."""
    stmt = (
        select(models.ProductFormulation, models.ProductCategory)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .limit(20)
    )
    res = await db.execute(stmt)
    items = res.all()

    catalog = []
    for formulation, cat in items:
        catalog.append({
            "id": str(formulation.id),
            "formulation_code": formulation.formulation_code,
            "name": cat.name,
            "category_slug": cat.slug,
            "description": cat.description,
            "serving_size_g": float(formulation.serving_size_g),
            "cost_per_serving_inr": float(formulation.cost_per_serving_inr),
            "cost_per_pack_inr": float(formulation.cost_per_pack_inr),
            "pack_size_servings": formulation.pack_size_servings,
            "nutrient_summary": formulation.nutrient_results_per_serving,
            "is_prototype": True,
            "prototype_badge": "Prototype product – demo checkout",
        })

    # If no formulation generated yet, present category prototypes
    if not catalog:
        cat_stmt = select(models.ProductCategory)
        cats = (await db.execute(cat_stmt)).scalars().all()
        for cat in cats:
            catalog.append({
                "id": str(cat.id),
                "formulation_code": f"CONCEPT-{cat.slug.upper()}",
                "name": cat.name,
                "category_slug": cat.slug,
                "description": cat.description,
                "serving_size_g": float(cat.format_template.get("serving_size_g", 35.0)),
                "cost_per_serving_inr": 25.0,
                "cost_per_pack_inr": 350.0,
                "pack_size_servings": 14,
                "nutrient_summary": {"iron": 4.5, "vit_c": 25.0, "protein": 6.0},
                "is_prototype": True,
                "prototype_badge": "Prototype product – demo checkout",
            })

    return catalog


@router.get("/products/{id}")
async def get_shop_product(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(models.ProductFormulation, models.ProductCategory)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.ProductFormulation.id == id)
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise NotFoundException("Product", id)

    formulation, cat = row
    return {
        "id": str(formulation.id),
        "formulation_code": formulation.formulation_code,
        "name": cat.name,
        "category_slug": cat.slug,
        "description": cat.description,
        "serving_size_g": float(formulation.serving_size_g),
        "cost_per_serving_inr": float(formulation.cost_per_serving_inr),
        "cost_per_pack_inr": float(formulation.cost_per_pack_inr),
        "pack_size_servings": formulation.pack_size_servings,
        "nutrient_results_per_serving": formulation.nutrient_results_per_serving,
        "preparation_instructions": formulation.preparation_instructions,
        "storage_instructions": formulation.storage_instructions,
        "is_prototype": True,
        "prototype_badge": "Prototype product – demo checkout",
    }

