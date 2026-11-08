import io
import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import check_resource_ownership, get_current_user
from app.core.errors import BadRequestException, NotFoundException
from app.db.session import get_db
import app.db.models as models
from app.schemas.formulation import (
    CompareFormulationsResponse,
    FormulationResponse,
    RecommendationDetailResponse,
)
from app.services.pdf.report_generator import generate_nutritional_pdf_report

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{id}", response_model=RecommendationDetailResponse)
async def get_recommendation_detail(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(models.GeneratedRecommendation)
        .where(models.GeneratedRecommendation.id == id)
    )
    res = await db.execute(stmt)
    rec = res.scalar_one_or_none()
    if not rec:
        raise NotFoundException("Recommendation", id)

    check_resource_ownership(rec.user_id, current_user)

    # Fetch formulation
    form_stmt = (
        select(models.ProductFormulation, models.ProductCategory)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.ProductFormulation.id == rec.formulation_id)
    )
    form_res = await db.execute(form_stmt)
    form_tuple = form_res.first()
    if not form_tuple:
        raise NotFoundException("Formulation", rec.formulation_id)

    formulation, category = form_tuple

    # Fetch ingredients
    ing_stmt = (
        select(models.FormulationIngredient, models.Ingredient)
        .join(models.Ingredient, models.FormulationIngredient.ingredient_id == models.Ingredient.id)
        .where(models.FormulationIngredient.formulation_id == formulation.id)
    )
    ing_rows = (await db.execute(ing_stmt)).all()

    ingredient_items = [
        {
            "ingredient_id": ing.id,
            "name": ing.name,
            "local_names": ing.local_names,
            "grams_per_serving": float(fi.grams_per_serving),
            "pct_of_mix": float(fi.pct_of_mix),
            "purpose": fi.purpose,
            "rationale_code": fi.rationale_code,
        }
        for fi, ing in ing_rows
    ]

    form_resp = FormulationResponse(
        id=formulation.id,
        formulation_code=formulation.formulation_code,
        version=formulation.version,
        category_slug=category.slug,
        category_name=category.name,
        serving_size_g=float(formulation.serving_size_g),
        cost_per_serving_inr=float(formulation.cost_per_serving_inr),
        cost_per_pack_inr=float(formulation.cost_per_pack_inr),
        pack_size_servings=formulation.pack_size_servings,
        ingredients=ingredient_items,
        nutrient_results_per_serving=formulation.nutrient_results_per_serving,
        bioavailability={},
        why_selected=rec.why_selected,
        explanation_text=rec.explanation_text,
        validation_status=formulation.validation_status,
        data_status_banner="Demo nutrient data – not validated",
        preparation_instructions=formulation.preparation_instructions,
        storage_instructions=formulation.storage_instructions,
        is_saved=rec.saved,
        rank=rec.rank,
    )

    return RecommendationDetailResponse(
        id=rec.id,
        assessment_id=rec.assessment_id,
        formulation=form_resp,
        rank=rec.rank,
        saved=rec.saved,
        generated_at=rec.generated_at,
    )


@router.post("/{id}/save")
async def save_recommendation(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.GeneratedRecommendation).where(models.GeneratedRecommendation.id == id)
    res = await db.execute(stmt)
    rec = res.scalar_one_or_none()
    if not rec:
        raise NotFoundException("Recommendation", id)

    check_resource_ownership(rec.user_id, current_user)
    rec.saved = True
    await db.commit()
    return {"success": True, "message": "Formulation saved to your favorites."}


@router.get("/compare", response_model=CompareFormulationsResponse)
async def compare_formulations(
    ids: str = Query(..., description="Comma-separated formulation IDs (max 3)"),
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    raw_ids = [s.strip() for s in ids.split(",") if s.strip()]
    if not raw_ids or len(raw_ids) > 3:
        raise BadRequestException("INVALID_ID_COUNT", "Please provide between 1 and 3 formulation IDs for comparison.")

    formulations_list: List[FormulationResponse] = []
    for f_id in raw_ids:
        try:
            uid = uuid.UUID(f_id)
        except ValueError:
            continue

        form_stmt = (
            select(models.ProductFormulation, models.ProductCategory)
            .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
            .where(models.ProductFormulation.id == uid)
        )
        res = await db.execute(form_stmt)
        row = res.first()
        if row:
            formulation, category = row
            # Ingredients
            ing_stmt = (
                select(models.FormulationIngredient, models.Ingredient)
                .join(models.Ingredient, models.FormulationIngredient.ingredient_id == models.Ingredient.id)
                .where(models.FormulationIngredient.formulation_id == formulation.id)
            )
            ing_rows = (await db.execute(ing_stmt)).all()
            ing_items = [
                {
                    "name": ing.name,
                    "grams_per_serving": float(fi.grams_per_serving),
                    "pct_of_mix": float(fi.pct_of_mix),
                    "purpose": fi.purpose,
                }
                for fi, ing in ing_rows
            ]

            formulations_list.append(
                FormulationResponse(
                    id=formulation.id,
                    formulation_code=formulation.formulation_code,
                    version=formulation.version,
                    category_slug=category.slug,
                    category_name=category.name,
                    serving_size_g=float(formulation.serving_size_g),
                    cost_per_serving_inr=float(formulation.cost_per_serving_inr),
                    cost_per_pack_inr=float(formulation.cost_per_pack_inr),
                    pack_size_servings=formulation.pack_size_servings,
                    ingredients=ing_items,
                    nutrient_results_per_serving=formulation.nutrient_results_per_serving,
                    bioavailability={},
                    why_selected=[],
                    explanation_text={},
                    validation_status=formulation.validation_status,
                    data_status_banner="Demo nutrient data – not validated",
                    preparation_instructions=formulation.preparation_instructions,
                    storage_instructions=formulation.storage_instructions,
                    is_saved=False,
                    rank=1,
                )
            )

    return CompareFormulationsResponse(formulations=formulations_list)


@router.get("/{id}/report.pdf")
async def download_pdf_report(
    id: uuid.UUID,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generates and streams an auditable PDF nutritional report."""
    rec_stmt = select(models.GeneratedRecommendation).where(models.GeneratedRecommendation.id == id)
    rec = (await db.execute(rec_stmt)).scalar_one_or_none()
    if not rec:
        raise NotFoundException("Recommendation", id)

    check_resource_ownership(rec.user_id, current_user)

    form_stmt = (
        select(models.ProductFormulation, models.ProductCategory)
        .join(models.ProductCategory, models.ProductFormulation.category_id == models.ProductCategory.id)
        .where(models.ProductFormulation.id == rec.formulation_id)
    )
    formulation, category = (await db.execute(form_stmt)).first()

    ing_stmt = (
        select(models.FormulationIngredient, models.Ingredient)
        .join(models.Ingredient, models.FormulationIngredient.ingredient_id == models.Ingredient.id)
        .where(models.FormulationIngredient.formulation_id == formulation.id)
    )
    ing_rows = (await db.execute(ing_stmt)).all()

    pdf_data = {
        "name": category.name.get("en", "NutriAI Food Prototype"),
        "category": category.slug.replace("_", " ").title(),
        "serving_size_g": float(formulation.serving_size_g),
        "cost_per_serving_inr": float(formulation.cost_per_serving_inr),
        "validation_status": formulation.validation_status,
        "ingredients": [
            {
                "name": ing.name,
                "grams_per_serving": float(fi.grams_per_serving),
                "pct_of_mix": float(fi.pct_of_mix),
                "purpose": fi.purpose,
            }
            for fi, ing in ing_rows
        ],
        "nutrient_results_per_serving": formulation.nutrient_results_per_serving,
    }

    pdf_bytes = generate_nutritional_pdf_report(pdf_data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=NutriAI_Specification_{formulation.formulation_code}.pdf"
        },
    )

