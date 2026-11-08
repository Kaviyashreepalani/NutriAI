from typing import Any, Dict, List, Set


def filter_candidate_ingredients(
    all_ingredients: List[Dict[str, Any]],
    user_diet_type: str,
    user_allergens: List[str],
    category_template: Dict[str, Any],
    max_budget_per_serving: float = 35.0,
) -> List[Dict[str, Any]]:
    """Hard filter candidate ingredients based on clinical allergens, diet class, and format compatibility."""
    user_allergen_set: Set[str] = {a.strip().lower() for a in user_allergens if a}
    allowed_categories: Set[str] = set(category_template.get("allowed_ingredient_categories", []))

    # Diet class hierarchy
    diet_hierarchy = {
        "vegan": {"vegan"},
        "vegetarian": {"vegan", "vegetarian"},
        "eggetarian": {"vegan", "vegetarian", "eggetarian"},
        "non_vegetarian": {"vegan", "vegetarian", "eggetarian", "non_vegetarian"},
        "jain": {"vegan", "vegetarian"},  # Excludes root vegetables via tags if present
    }
    allowed_diet_classes = diet_hierarchy.get(user_diet_type.lower(), {"vegan", "vegetarian"})

    candidates: List[Dict[str, Any]] = []

    for ing in all_ingredients:
        # 1. HARD ALLERGEN CONSTRAINT: Zero tolerance
        ing_allergens = [a.strip().lower() for a in ing.get("allergens", []) if a]
        if any(a in user_allergen_set for a in ing_allergens):
            continue  # Excluded at candidate generation layer

        # 2. Diet class filter
        ing_diet_class = ing.get("diet_class", "vegan").lower()
        if ing_diet_class not in allowed_diet_classes:
            continue

        # 3. Product format category compatibility
        ing_cat = ing.get("category", "")
        if allowed_categories and ing_cat not in allowed_categories:
            continue

        # 4. Availability
        if ing.get("availability") == "discontinued":
            continue

        candidates.append(ing)

    return candidates

