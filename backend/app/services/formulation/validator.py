from typing import Any, Dict, List, Tuple


class FormulationValidator:
    """Independently verifies candidate formulation against hard dietary and safety constraints."""

    SUPPORTED_NUTRIENTS = [
        "energy",
        "protein",
        "iron",
        "folate",
        "b12",
        "vit_c",
        "calcium",
        "fat",
        "added_sugar",
        "sodium",
        "fibre",
    ]

    @classmethod
    def validate_and_recompute(
        cls,
        ingredients: List[Dict[str, Any]],
        serving_size_g: float,
        user_diet_type: str,
        user_allergens: List[str],
        nutrient_targets: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any], List[str]]:
        errors: List[str] = []
        user_allergen_set = {a.strip().lower() for a in user_allergens if a}

        # 1. Re-check Serving Size sum
        total_grams = sum(float(ing.get("grams_per_serving", 0.0)) for ing in ingredients)
        if abs(total_grams - serving_size_g) > 1.0:
            errors.append(f"Serving size mismatch: expected {serving_size_g}g, computed {total_grams:.2f}g.")

        # 2. Independent Allergen Re-Check (Hard Safety Guard)
        for ing in ingredients:
            ing_allergens = [a.strip().lower() for a in ing.get("allergens", []) if a]
            overlap = user_allergen_set.intersection(ing_allergens)
            if overlap:
                errors.append(f"ALLERGEN VIOLATION: Ingredient '{ing.get('name')}' contains allergen(s) {list(overlap)}.")

        # 3. Independent Recomputation of Nutrients
        nutrient_totals: Dict[str, Any] = {}
        for nut in cls.SUPPORTED_NUTRIENTS:
            total_nut = 0.0
            has_data = False
            for ing in ingredients:
                nut_dict = ing.get("nutrients", {})
                if nut in nut_dict and nut_dict[nut] is not None:
                    has_data = True
                    g = float(ing.get("grams_per_serving", 0.0))
                    val_100g = float(nut_dict[nut])
                    total_nut += (val_100g * g) / 100.0

            if has_data:
                nutrient_totals[nut] = round(total_nut, 2)
            else:
                nutrient_totals[nut] = "not in database"

        # 4. Check HFSS Caps
        sugar_val = nutrient_totals.get("added_sugar")
        if isinstance(sugar_val, (int, float)):
            sugar_cap = float(nutrient_targets.get("added_sugar_max_g", 6.0))
            if sugar_val > sugar_cap + 0.5:
                errors.append(f"HFSS Violation: Added sugar {sugar_val}g exceeds cap of {sugar_cap}g.")

        fat_val = nutrient_totals.get("fat")
        if isinstance(fat_val, (int, float)):
            fat_cap = float(nutrient_targets.get("saturated_fat_max_g", 4.0))
            if fat_val > fat_cap + 0.5:
                errors.append(f"HFSS Violation: Saturated fat {fat_val}g exceeds cap of {fat_cap}g.")

        # 5. Recompute Cost per serving
        cost_per_serving = 0.0
        for ing in ingredients:
            cost_per_kg = float(ing.get("cost_per_kg_inr", 100.0))
            g = float(ing.get("grams_per_serving", 0.0))
            cost_per_serving += (cost_per_kg * g) / 1000.0
        cost_per_serving = round(cost_per_serving, 2)

        is_valid = len(errors) == 0
        computed_summary = {
            "serving_size_g": serving_size_g,
            "total_grams": round(total_grams, 2),
            "cost_per_serving_inr": cost_per_serving,
            "nutrient_results_per_serving": nutrient_totals,
        }

        return is_valid, computed_summary, errors

