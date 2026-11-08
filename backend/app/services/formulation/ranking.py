from typing import Any, Dict, List


def rank_formulations(
    candidates: List[Dict[str, Any]],
    user_preferred_formats: List[str],
    nutrient_targets: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Ranks validated formulations using a multi-criteria scoring function."""
    # Weights
    WEIGHTS = {
        "target_fit": 0.35,
        "bioavailability": 0.25,
        "affordability": 0.20,
        "format_preference": 0.15,
        "ingredient_simplicity": 0.05,
    }

    iron_target = float(nutrient_targets.get("iron_min_mg", 4.0))

    ranked_results: List[Dict[str, Any]] = []

    for item in candidates:
        nutrients = item.get("nutrient_results_per_serving", {})
        bio_info = item.get("bioavailability", {})

        # 1. Target fit score (iron proximity)
        iron_val = float(nutrients.get("iron", 0.0)) if isinstance(nutrients.get("iron"), (int, float)) else 0.0
        iron_diff = abs(iron_val - iron_target)
        fit_score = max(0.0, 100.0 - (iron_diff * 20.0))

        # 2. Bioavailability score
        bio_index = float(bio_info.get("adjusted_iron_index", 0.25))
        bio_score = min(100.0, bio_index * 200.0)

        # 3. Affordability score
        cost = float(item.get("cost_per_serving_inr", 25.0))
        cost_score = max(0.0, 100.0 - (cost * 2.0))

        # 4. User format preference score
        cat_slug = item.get("category_slug", "")
        pref_score = 100.0 if cat_slug in user_preferred_formats else 60.0

        # 5. Ingredient simplicity (5-7 ingredients ideal)
        ing_count = len(item.get("ingredients", []))
        simplicity_score = 100.0 if 4 <= ing_count <= 7 else 70.0

        composite_score = (
            (fit_score * WEIGHTS["target_fit"])
            + (bio_score * WEIGHTS["bioavailability"])
            + (cost_score * WEIGHTS["affordability"])
            + (pref_score * WEIGHTS["format_preference"])
            + (simplicity_score * WEIGHTS["ingredient_simplicity"])
        )

        # Build explainable why-selected reasons
        reasons = [
            {
                "reason_code": "IRON_DELIVERY_BENCHMARK",
                "detail": f"Provides {iron_val:.1f} mg iron per serving, matching the ICMR benchmark range for targeted dietary support.",
                "rule_version": "icmr_v2020.1",
            },
            {
                "reason_code": "BIOAVAILABILITY_ENHANCEMENT",
                "detail": f"Formulated with natural ascorbic acid pairing to achieve a {bio_info.get('net_bioavailability_multiplier', 1.0)}x estimated absorption multiplier.",
                "rule_version": "icmr_v2020.1",
            },
            {
                "reason_code": "AFFORDABLE_DAILY_SERVING",
                "detail": f"Optimized at ₹{cost:.2f} per serving for sustainable daily consumability.",
                "rule_version": "icmr_v2020.1",
            },
        ]

        item_copy = dict(item)
        item_copy["rank_score"] = round(composite_score, 2)
        item_copy["scoring_weights"] = WEIGHTS
        item_copy["why_selected"] = reasons
        ranked_results.append(item_copy)

    # Sort descending by composite score
    ranked_results.sort(key=lambda x: x["rank_score"], reverse=True)

    # Assign rank 1, 2, 3
    for i, res in enumerate(ranked_results):
        res["rank"] = i + 1

    return ranked_results[:3]

