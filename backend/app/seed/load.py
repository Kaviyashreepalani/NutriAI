"""Idempotent seed data loader for NutriAI.
Run with: python -m app.seed.load
"""
import uuid
from datetime import date, datetime, timezone
from sqlalchemy import select
from app.db.session import SyncSessionLocal, sync_engine, Base
import app.db.models as models

from app.seed.data.ingredients import INGREDIENTS_SEED
from app.seed.data.rules import RULE_SETS_SEED, PRODUCT_CATEGORIES_SEED
from app.seed.data.references import NUTRIENT_REFERENCES_SEED
from app.seed.data.statistics import STATISTICS_SEED
from app.seed.data.education import EDUCATION_MODULES_SEED
from app.services.ocr.normalizer import PARAMETER_DEFINITIONS


def load_seed_data():
    print("Beginning idempotent database seed...")
    # Ensure tables are created
    Base.metadata.create_all(bind=sync_engine)

    db = SyncSessionLocal()
    try:
        # 1. Seed Lab Parameters
        print("Seeding Lab Parameters...")
        for code, meta in PARAMETER_DEFINITIONS.items():
            existing = db.execute(select(models.LabParameter).where(models.LabParameter.code == code)).scalar_one_or_none()
            if not existing:
                param = models.LabParameter(
                    code=code,
                    display_name={
                        "en": code.replace("_", " ").title(),
                        "ta": code,
                        "hi": code,
                        "te": code,
                        "ml": code,
                    },
                    canonical_unit=meta["canonical_unit"],
                    allowed_units=meta["allowed_units"],
                    plausible_min=meta["plausible_min"],
                    plausible_max=meta["plausible_max"],
                    aliases=meta["aliases"],
                )
                db.add(param)
        db.commit()

        # 2. Seed Assessment Rule Sets
        print("Seeding Rule Sets...")
        for rset in RULE_SETS_SEED:
            existing = db.execute(select(models.AssessmentRuleSet).where(models.AssessmentRuleSet.version == rset["version"])).scalar_one_or_none()
            if not existing:
                db_rule = models.AssessmentRuleSet(
                    version=rset["version"],
                    rules=rset["rules"],
                    status=rset["status"],
                )
                db.add(db_rule)
        db.commit()

        # 3. Seed Product Categories
        print("Seeding Product Categories...")
        for cat in PRODUCT_CATEGORIES_SEED:
            existing = db.execute(select(models.ProductCategory).where(models.ProductCategory.slug == cat["slug"])).scalar_one_or_none()
            if not existing:
                db_cat = models.ProductCategory(
                    slug=cat["slug"],
                    name=cat["name"],
                    description=cat["description"],
                    format_template=cat["format_template"],
                )
                db.add(db_cat)
        db.commit()

        # 4. Seed Nutrient Reference Values (RDA)
        print("Seeding Nutrient Reference Values...")
        for ref in NUTRIENT_REFERENCES_SEED:
            existing = db.execute(
                select(models.NutrientReferenceValue).where(
                    models.NutrientReferenceValue.nutrient_code == ref["nutrient_code"],
                    models.NutrientReferenceValue.life_stage == ref["life_stage"],
                    models.NutrientReferenceValue.version == "v2020.1",
                )
            ).scalar_one_or_none()
            if not existing:
                db_ref = models.NutrientReferenceValue(
                    nutrient_code=ref["nutrient_code"],
                    life_stage=ref["life_stage"],
                    value=ref["value"],
                    unit=ref["unit"],
                    source_document="PLACEHOLDER_DEMO",
                    version="v2020.1",
                    effective_from=date(2020, 1, 1),
                    status="draft",
                )
                db.add(db_ref)
        db.commit()

        # 5. Seed Ingredients and Nutrients
        print("Seeding 40 Ingredients & Draft Nutrients...")
        for ing_data in INGREDIENTS_SEED:
            existing = db.execute(select(models.Ingredient).where(models.Ingredient.name == ing_data["name"])).scalar_one_or_none()
            if not existing:
                db_ing = models.Ingredient(
                    name=ing_data["name"],
                    local_names=ing_data["local_names"],
                    category=ing_data["category"],
                    diet_class=ing_data["diet_class"],
                    allergens=ing_data["allergens"],
                    cost_per_kg_inr=ing_data["cost_per_kg_inr"],
                    cost_as_of=date.today(),
                    availability=ing_data.get("availability", "high"),
                    processing_notes=ing_data.get("processing_notes", ""),
                    min_inclusion_pct=ing_data.get("min_inclusion_pct", 0.0),
                    max_inclusion_pct=ing_data.get("max_inclusion_pct", 100.0),
                    data_status="draft",
                    version=1,
                )
                db.add(db_ing)
                db.flush()

                # Add nutrients
                for nut_code, amount in ing_data["nutrients"].items():
                    db_nut = models.IngredientNutrient(
                        ingredient_id=db_ing.id,
                        nutrient_code=nut_code,
                        amount_per_100g=float(amount) if isinstance(amount, (int, float)) else (1.0 if amount else 0.0),
                        unit="mg" if nut_code in ("iron", "vit_c", "calcium", "sodium") else ("g" if nut_code in ("protein", "fat", "added_sugar", "fibre") else ("kcal" if nut_code == "energy" else "ug")),
                        source="PLACEHOLDER_DEMO",
                        source_ref="Draft Estimation",
                        is_heme_iron=False,
                    )
                    db.add(db_nut)
        db.commit()

        # 6. Seed Statistics
        print("Seeding Epidemiological Statistics...")
        for stat in STATISTICS_SEED:
            existing = db.execute(select(models.Statistic).where(models.Statistic.metric_name == stat["metric_name"])).scalar_one_or_none()
            if not existing:
                # Add reference if citation present
                ref_id = None
                if stat.get("citation"):
                    ref = models.ReferenceCatalog(citation=stat["citation"], year=2021)
                    db.add(ref)
                    db.flush()
                    ref_id = ref.id

                db_stat = models.Statistic(
                    metric_name=stat["metric_name"],
                    value=stat["value"],
                    unit=stat["unit"],
                    population_group=stat["population_group"],
                    survey_name=stat["survey_name"],
                    survey_year=stat["survey_year"],
                    definition=stat["definition"],
                    reference_id=ref_id,
                    status=stat["status"],
                )
                db.add(db_stat)
        db.commit()

        # 7. Seed Educational Content
        print("Seeding Educational Modules...")
        for edu in EDUCATION_MODULES_SEED:
            existing = db.execute(select(models.EducationalContent).where(models.EducationalContent.slug == edu["slug"])).scalar_one_or_none()
            if not existing:
                db_edu = models.EducationalContent(
                    slug=edu["slug"],
                    category=edu["category"],
                    title=edu["title"],
                    body=edu["body"],
                    status=edu["status"],
                    translation_review_status=edu["translation_review_status"],
                    references_list=edu["references_list"],
                )
                db.add(db_edu)
        db.commit()

        # 8. Seed Demo Users
        print("Seeding 3 Clinical Demo Users...")
        demo_users_data = [
            {
                "uid": "dev-user-adolescent-uid",
                "email": "adolescent.girl@example.org",
                "dob": date(2010, 5, 14),  # 16-year-old
                "full_name": "Ananya Sharma",
                "role": "user",
                "diet": "vegetarian",
                "allergens": ["peanut"],
                "height": 158.0,
                "weight": 46.0,
            },
            {
                "uid": "dev-user-woman28-uid",
                "email": "woman28.vegan@example.org",
                "dob": date(1998, 8, 20),  # 28-year-old
                "full_name": "Pooja Hegde",
                "role": "user",
                "diet": "vegan",
                "allergens": [],
                "height": 162.0,
                "weight": 54.0,
            },
            {
                "uid": "dev-user-woman42-uid",
                "email": "woman42.eggetarian@example.org",
                "dob": date(1984, 11, 2),  # 42-year-old
                "full_name": "Dr. Sunita Rao",
                "role": "user",
                "diet": "eggetarian",
                "allergens": [],
                "height": 155.0,
                "weight": 60.0,
            },
            {
                "uid": "dev-admin-uid",
                "email": "admin@nutriai.example.org",
                "dob": date(1990, 1, 1),
                "full_name": "Admin User",
                "role": "admin",
                "diet": "vegetarian",
                "allergens": [],
                "height": 165.0,
                "weight": 65.0,
            },
            {
                "uid": "dev-nutritionist-uid",
                "email": "nutritionist@nutriai.example.org",
                "dob": date(1988, 3, 15),
                "full_name": "Dr. Aruna Swaminathan (Nutritionist)",
                "role": "nutritionist",
                "diet": "vegetarian",
                "allergens": [],
                "height": 160.0,
                "weight": 58.0,
            },
        ]

        for u in demo_users_data:
            existing = db.execute(select(models.User).where(models.User.email == u["email"])).scalar_one_or_none()
            if not existing:
                user = models.User(
                    auth_uid=u["uid"],
                    auth_provider="dev",
                    email=u["email"],
                    email_verified=True,
                    role=u["role"],
                    preferred_language="en",
                    date_of_birth=u["dob"],
                    status="active",
                )
                db.add(user)
                db.flush()

                # Profile
                profile = models.UserProfile(
                    user_id=user.id,
                    full_name=u["full_name"],
                    sex="female",
                    city="Bengaluru",
                    state="Karnataka",
                    pin_code="560001",
                    profile_completion_pct=100,
                )
                db.add(profile)

                # Physical Measurement
                h_m = u["height"] / 100.0
                bmi = round(u["weight"] / (h_m * h_m), 1)
                meas = models.PhysicalMeasurement(
                    user_id=user.id,
                    measured_on=date.today(),
                    height_cm=u["height"],
                    weight_kg=u["weight"],
                    bmi=bmi,
                    source="clinical_demo",
                )
                db.add(meas)

                # Dietary Preference
                diet = models.DietaryPreference(
                    user_id=user.id,
                    diet_type=u["diet"],
                    disliked_foods=[],
                    favourite_foods=[],
                    meals_per_day=3,
                    budget_per_serving_inr=30.0,
                    preferred_format_ids=["bars", "laddoos"],
                )
                db.add(diet)

                # Allergies
                for allergen in u["allergens"]:
                    allergy = models.Allergy(
                        user_id=user.id,
                        allergen_code=allergen,
                        kind="allergy",
                        severity="severe",
                        is_active=True,
                    )
                    db.add(allergy)

                # Health Information
                health = models.HealthInformation(
                    user_id=user.id,
                    known_deficiencies=[],
                    pregnancy_status="not_pregnant",
                )
                db.add(health)

                # Cart
                cart = models.Cart(user_id=user.id)
                db.add(cart)

        db.commit()
        print("Idempotent seed completed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    load_seed_data()

