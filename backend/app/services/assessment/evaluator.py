from datetime import date
from typing import Any, Dict, List, Optional, Tuple
from app.core.config import settings


def determine_life_stage(dob: date) -> Tuple[Optional[str], float]:
    """Computes exact age in years and derives target life-stage band.

    Bands:
    - girl_10_12 (10 - 12.9)
    - girl_13_15 (13 - 15.9)
    - girl_16_18 (16 - 18.9)
    - woman_19_35 (19 - 35.9)
    - woman_36_49 (36 - 49.9)
    """
    today = date.today()
    age = (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )

    if age < 10 or age > 49:
        return None, float(age)

    if 10 <= age <= 12:
        return "girl_10_12", float(age)
    elif 13 <= age <= 15:
        return "girl_13_15", float(age)
    elif 16 <= age <= 18:
        return "girl_16_18", float(age)
    elif 19 <= age <= 35:
        return "woman_19_35", float(age)
    else:
        return "woman_36_49", float(age)


# Default fallback clinical evaluation rules if DB rules are empty or loading
DEFAULT_SAFETY_RULES = {
    "version": "icmr_v2020.1",
    "hb_cutoffs_non_pregnant": {
        "severe": 7.0,
        "moderate": 10.0,
        "mild": 12.0,
    },
    "hb_cutoffs_pregnant": {
        "severe": 7.0,
        "moderate": 10.0,
        "mild": 11.0,
    },
    "ferritin_cutoff_depleted": 15.0,
    "ferritin_cutoff_elevated": 150.0,
    "mcv_cutoff_microcytic": 80.0,
    "b12_cutoff_low": 200.0,
    "folate_cutoff_low": 4.0,
}


def evaluate_clinical_safety(
    age: float,
    life_stage: Optional[str],
    lab_results: Dict[str, float],
    pregnancy_status: str = "not_pregnant",
    known_conditions: Optional[List[str]] = None,
    rule_set: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Deterministic evaluation of laboratory parameters and demographic context."""
    rules = rule_set or DEFAULT_SAFETY_RULES
    findings: List[Dict[str, Any]] = []
    safety_messages: List[Dict[str, Any]] = []
    overall_safety_status = "ok"

    # 1. Out of age scope gate
    if life_stage is None or age < 10 or age > 49:
        return {
            "safety_status": "blocked",
            "age": age,
            "life_stage": life_stage or "out_of_scope",
            "findings": [{
                "rule_id": "AGE_SCOPE_GATE",
                "message_key": "safety.age_out_of_scope",
                "detail": f"NutriAI formulation models are validated exclusively for adolescent girls and women aged 10-49 (current age: {age}).",
            }],
            "safety_messages": [{
                "severity": "critical",
                "message_key": "safety.age_out_of_scope",
            }],
            "nutrient_targets": {},
        }

    is_pregnant = "pregnant" in (pregnancy_status or "").lower() and "not" not in (pregnancy_status or "").lower()
    is_lactating = "lactat" in (pregnancy_status or "").lower()

    # Pregnancy / Lactation Advisory
    if is_pregnant or is_lactating:
        findings.append({
            "rule_id": "PREGNANCY_LACTATION_FLAG",
            "message_key": "safety.pregnancy_consult_required",
            "detail": "Pregnancy/lactation requires personalized medical supervision by an obstetrician. Food products serve strictly as supplementary nutritional intake.",
        })
        safety_messages.append({
            "severity": "caution",
            "message_key": "safety.pregnancy_consult_required",
        })
        if overall_safety_status == "ok":
            overall_safety_status = "caution"

    # 2. Haemoglobin Evaluation
    hb_val = lab_results.get("HB")
    hb_cutoffs = (
        rules.get("hb_cutoffs_pregnant", DEFAULT_SAFETY_RULES["hb_cutoffs_pregnant"])
        if is_pregnant
        else rules.get("hb_cutoffs_non_pregnant", DEFAULT_SAFETY_RULES["hb_cutoffs_non_pregnant"])
    )

    is_severe_hb = False
    is_moderate_hb = False
    is_mild_hb = False

    if hb_val is not None:
        if hb_val < hb_cutoffs["severe"]:
            is_severe_hb = True
            overall_safety_status = "blocked"
            findings.append({
                "rule_id": "HB_SEVERE_GATE",
                "parameter": "HB",
                "observed_value": hb_val,
                "message_key": "safety.hb_severe_warning",
                "detail": f"Haemoglobin value of {hb_val} g/dL is significantly outside the laboratory reference range. Immediate medical evaluation by a physician is necessary before consuming any specialized dietary product.",
            })
            safety_messages.append({
                "severity": "critical",
                "message_key": "safety.hb_severe_critical",
            })
        elif hb_val < hb_cutoffs["moderate"]:
            is_moderate_hb = True
            findings.append({
                "rule_id": "HB_MODERATE_REFERRAL",
                "parameter": "HB",
                "observed_value": hb_val,
                "message_key": "safety.hb_moderate_warning",
                "detail": f"Haemoglobin value of {hb_val} g/dL reflects a pattern outside reference ranges that a doctor may want to review.",
            })
            safety_messages.append({
                "severity": "refer_to_doctor",
                "message_key": "safety.hb_moderate_warning",
            })
            if overall_safety_status in ("ok", "caution"):
                overall_safety_status = (
                    "refer_to_doctor"
                    if settings.ALLOW_GENERATION_WITH_REFERRAL
                    else "blocked"
                )
        elif hb_val < hb_cutoffs["mild"]:
            is_mild_hb = True
            findings.append({
                "rule_id": "HB_MILD_ADVISORY",
                "parameter": "HB",
                "observed_value": hb_val,
                "message_key": "safety.hb_mild_advisory",
                "detail": f"Haemoglobin value of {hb_val} g/dL is slightly below typical reference thresholds. Targeted dietary iron and vitamin C support may help meet daily nutrient needs.",
            })
            if overall_safety_status == "ok":
                overall_safety_status = "caution"

    # 3. Ferritin & Non-Iron Anaemia Safeguard
    ferritin_val = lab_results.get("FERRITIN")
    mcv_val = lab_results.get("MCV")
    non_iron_pattern = False

    if ferritin_val is not None:
        if ferritin_val < rules.get("ferritin_cutoff_depleted", 15.0):
            findings.append({
                "rule_id": "FERRITIN_DEPLETED",
                "parameter": "FERRITIN",
                "observed_value": ferritin_val,
                "message_key": "safety.ferritin_depleted",
                "detail": f"Serum ferritin of {ferritin_val} ng/mL indicates depleted iron stores.",
            })
        elif ferritin_val > rules.get("ferritin_cutoff_elevated", 150.0):
            # Normal or elevated ferritin with low Hb / low MCV
            if (hb_val is not None and hb_val < hb_cutoffs["mild"]) or (mcv_val is not None and mcv_val < rules.get("mcv_cutoff_microcytic", 80.0)):
                non_iron_pattern = True
                findings.append({
                    "rule_id": "NON_IRON_ANAEMIA_SAFEGUARD",
                    "parameter": "FERRITIN_MCV_COMBINED",
                    "observed_value": f"Ferritin={ferritin_val}, MCV={mcv_val}",
                    "message_key": "safety.non_iron_anaemia_pattern",
                    "detail": "Observed pattern shows reduced red cell indices alongside normal/elevated ferritin stores. This suggests possible non-iron related factors (e.g. haemoglobinopathy trait or inflammation). Excessive iron supplementation is not advised without medical investigation.",
                })
                safety_messages.append({
                    "severity": "refer_to_doctor",
                    "message_key": "safety.non_iron_anaemia_pattern",
                })
                if overall_safety_status in ("ok", "caution"):
                    overall_safety_status = "refer_to_doctor"

    # 4. Vitamin B12 and Folate Check
    b12_val = lab_results.get("B12")
    if b12_val is not None and b12_val < rules.get("b12_cutoff_low", 200.0):
        findings.append({
            "rule_id": "B12_LOW_ADVISORY",
            "parameter": "B12",
            "observed_value": b12_val,
            "message_key": "safety.b12_low_advisory",
            "detail": f"Vitamin B12 level of {b12_val} pg/mL is below reference threshold. Folate and B12 support are emphasized.",
        })
        if overall_safety_status == "ok":
            overall_safety_status = "caution"

    folate_val = lab_results.get("FOLATE")
    if folate_val is not None and folate_val < rules.get("folate_cutoff_low", 4.0):
        findings.append({
            "rule_id": "FOLATE_LOW_ADVISORY",
            "parameter": "FOLATE",
            "observed_value": folate_val,
            "message_key": "safety.folate_low_advisory",
            "detail": f"Folate level of {folate_val} ng/mL is below reference threshold.",
        })
        if overall_safety_status == "ok":
            overall_safety_status = "caution"

    # 5. Calculate Deterministic Nutrient Targets per Serving
    # Iron delivery benchmark: 4 - 5 mg per serving
    iron_min = settings.DEFAULT_IRON_TARGET_MIN_MG
    iron_max = settings.DEFAULT_IRON_TARGET_MAX_MG

    if non_iron_pattern:
        # Dampen iron target when non-iron pattern detected
        iron_min = 2.0
        iron_max = 3.5

    # Ascorbic acid minimum: at least 20mg to enhance non-heme iron absorption
    # Folate: 75 - 120 mcg
    # Protein: 4 - 8 g
    # Energy: 120 - 180 kcal
    # HFSS Caps: Added sugar < 6.0 g, Saturated Fat < 3.0 g, Sodium < 100 mg
    nutrient_targets = {
        "iron_min_mg": iron_min,
        "iron_max_mg": iron_max,
        "vit_c_min_mg": 25.0,
        "folate_min_ug": 80.0,
        "b12_min_ug": 0.6 if (b12_val and b12_val < 200.0) else 0.4,
        "protein_min_g": 5.0,
        "energy_min_kcal": 130.0,
        "energy_max_kcal": 190.0,
        "added_sugar_max_g": 5.0,      # HFSS cap
        "saturated_fat_max_g": 3.0,    # HFSS cap
        "sodium_max_mg": 100.0,        # HFSS cap
        "calcium_min_mg": 60.0,
    }

    return {
        "safety_status": overall_safety_status,
        "age": age,
        "life_stage": life_stage,
        "findings": findings,
        "safety_messages": safety_messages,
        "nutrient_targets": nutrient_targets,
    }

