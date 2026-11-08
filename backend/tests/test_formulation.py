import pytest
from app.services.formulation.candidates import filter_candidate_ingredients
from app.services.formulation.optimizer import FormulationOptimizer
from app.services.formulation.validator import FormulationValidator
from app.seed.data.ingredients import INGREDIENTS_SEED


def test_hard_allergen_exclusion():
    # User is vegetarian with peanut and sesame allergy
    user_allergens = ["peanut", "sesame"]
    user_diet = "vegetarian"

    category_template = {
        "serving_size_g": 35.0,
        "allowed_ingredient_categories": ["cereal_millet", "pulse_legume", "oilseed_nut", "sweetener_spice"],
    }

    candidates = filter_candidate_ingredients(
        all_ingredients=INGREDIENTS_SEED,
        user_diet_type=user_diet,
        user_allergens=user_allergens,
        category_template=category_template,
    )

    for ing in candidates:
        for a in ing.get("allergens", []):
            assert a not in user_allergens, f"Allergen {a} leaked into candidates!"


def test_linear_programming_and_validator():
    category_template = {
        "serving_size_g": 35.0,
        "binder_min_pct": 10.0,
        "allowed_ingredient_categories": ["cereal_millet", "pulse_legume", "oilseed_nut", "sweetener_spice", "fruit_veggie"],
    }
    nutrient_targets = {
        "iron_min_mg": 4.0,
        "iron_max_mg": 5.0,
        "vit_c_min_mg": 20.0,
        "added_sugar_max_g": 5.0,
        "saturated_fat_max_g": 3.0,
        "sodium_max_mg": 100.0,
    }

    candidates = filter_candidate_ingredients(
        all_ingredients=INGREDIENTS_SEED,
        user_diet_type="vegan",
        user_allergens=[],
        category_template=category_template,
    )

    optimizer = FormulationOptimizer(category_template, nutrient_targets)
    res = optimizer.solve(candidates)
    assert res is not None
    assert "ingredients" in res

    # Independent Validator
    is_valid, summary, errors = FormulationValidator.validate_and_recompute(
        ingredients=res["ingredients"],
        serving_size_g=35.0,
        user_diet_type="vegan",
        user_allergens=[],
        nutrient_targets=nutrient_targets,
    )

    assert is_valid is True, f"Validation failed with errors: {errors}"
    assert abs(summary["total_grams"] - 35.0) <= 0.5
    assert summary["cost_per_serving_inr"] > 0.0

