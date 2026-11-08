from typing import Any, Dict, List


def calculate_bioavailability_index(
    ingredients: List[Dict[str, Any]],
    total_iron_mg: float,
    total_vit_c_mg: float,
    rule_version: str = "icmr_v2020.1",
) -> Dict[str, Any]:
    """Computes total non-heme iron and an absorbability-adjusted iron index.

    Formula considerations (Hallberg et al. / ICMR guidelines):
    - Base absorption of vegetarian non-heme iron in typical Indian diets is estimated at 5% - 8%.
    - Ascorbic acid (Vitamin C) acts as a potent reducing agent and absorption enhancer:
      * Vit C : Iron ratio >= 2:1 -> ~1.4x enhancement factor
      * Vit C : Iron ratio >= 4:1 -> ~1.8x enhancement factor
      * Vit C : Iron ratio >= 6:1 -> ~2.2x enhancement factor
    - Presence of high phytate/polyphenol grains applies an inhibitor factor (0.75x)
      which is mitigated in the presence of adequate ascorbic acid.
    """
    if total_iron_mg <= 0:
        return {
            "total_iron_mg": 0.0,
            "adjusted_iron_index": 0.0,
            "enhancement_factor": 1.0,
            "rule_version": rule_version,
            "label": f"Estimated bioavailability index (Rule {rule_version})",
        }

    # Compute Vitamin C to Iron ratio
    vit_c_iron_ratio = total_vit_c_mg / total_iron_mg if total_iron_mg > 0 else 0.0

    enhancement_factor = 1.0
    if vit_c_iron_ratio >= 6.0:
        enhancement_factor = 2.2
    elif vit_c_iron_ratio >= 4.0:
        enhancement_factor = 1.8
    elif vit_c_iron_ratio >= 2.0:
        enhancement_factor = 1.4
    elif vit_c_iron_ratio >= 1.0:
        enhancement_factor = 1.15

    # Check phytate flag among ingredients
    has_phytate = any(ing.get("nutrients", {}).get("phytate_flag", False) for ing in ingredients)
    if has_phytate:
        # If ascorbic acid is high (> 20mg), phytate inhibition is substantially overcome
        inhibitor_factor = 0.90 if total_vit_c_mg >= 20.0 else 0.75
    else:
        inhibitor_factor = 1.0

    net_modifier = round(enhancement_factor * inhibitor_factor, 2)
    # Baseline non-heme bioavailable fraction in Indian vegetarian diet: ~6.0%
    baseline_bioavailable_mg = total_iron_mg * 0.06
    adjusted_iron_index = round(baseline_bioavailable_mg * net_modifier, 2)

    return {
        "total_iron_mg": round(total_iron_mg, 2),
        "total_vit_c_mg": round(total_vit_c_mg, 2),
        "vit_c_iron_ratio": round(vit_c_iron_ratio, 2),
        "enhancement_factor": enhancement_factor,
        "inhibitor_factor": inhibitor_factor,
        "net_bioavailability_multiplier": net_modifier,
        "adjusted_iron_index": adjusted_iron_index,
        "rule_version": rule_version,
        "label": f"Absorbability-adjusted iron index: estimated (Rule {rule_version})",
    }

