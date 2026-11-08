from typing import Dict, List, Optional, Tuple
from rapidfuzz import fuzz, process

# Standard canonical parameters and their known laboratory aliases
PARAMETER_DEFINITIONS: Dict[str, Dict] = {
    "HB": {
        "canonical_unit": "g/dL",
        "allowed_units": {"g/dL": 1.0, "g/L": 0.1, "gm/dL": 1.0, "gm%": 1.0, "g%": 1.0},
        "plausible_min": 3.0,
        "plausible_max": 25.0,
        "aliases": [
            "haemoglobin",
            "hemoglobin",
            "hb",
            "hgb",
            "total hemoglobin",
            "blood haemoglobin",
        ],
    },
    "FERRITIN": {
        "canonical_unit": "ng/mL",
        "allowed_units": {"ng/mL": 1.0, "ug/L": 1.0, "µg/L": 1.0, "mcg/L": 1.0, "pmol/L": 0.449},
        "plausible_min": 1.0,
        "plausible_max": 2000.0,
        "aliases": [
            "serum ferritin",
            "ferritin",
            "s. ferritin",
            "ferritin serum",
        ],
    },
    "SERUM_IRON": {
        "canonical_unit": "ug/dL",
        "allowed_units": {"ug/dL": 1.0, "µg/dL": 1.0, "mcg/dL": 1.0, "umol/L": 5.58},
        "plausible_min": 5.0,
        "plausible_max": 500.0,
        "aliases": [
            "serum iron",
            "iron",
            "s. iron",
            "total iron",
        ],
    },
    "TIBC": {
        "canonical_unit": "ug/dL",
        "allowed_units": {"ug/dL": 1.0, "µg/dL": 1.0, "mcg/dL": 1.0, "umol/L": 5.58},
        "plausible_min": 100.0,
        "plausible_max": 800.0,
        "aliases": [
            "total iron binding capacity",
            "tibc",
            "total iron-binding capacity",
        ],
    },
    "TSAT": {
        "canonical_unit": "%",
        "allowed_units": {"%": 1.0, "percent": 1.0},
        "plausible_min": 1.0,
        "plausible_max": 100.0,
        "aliases": [
            "transferrin saturation",
            "tsat",
            "iron saturation",
            "% transferrin saturation",
        ],
    },
    "MCV": {
        "canonical_unit": "fL",
        "allowed_units": {"fL": 1.0, "fl": 1.0, "cu.um": 1.0},
        "plausible_min": 40.0,
        "plausible_max": 150.0,
        "aliases": [
            "mean corpuscular volume",
            "mcv",
        ],
    },
    "MCH": {
        "canonical_unit": "pg",
        "allowed_units": {"pg": 1.0},
        "plausible_min": 10.0,
        "plausible_max": 60.0,
        "aliases": [
            "mean corpuscular hemoglobin",
            "mean corpuscular haemoglobin",
            "mch",
        ],
    },
    "MCHC": {
        "canonical_unit": "g/dL",
        "allowed_units": {"g/dL": 1.0, "g/L": 0.1, "%": 1.0},
        "plausible_min": 20.0,
        "plausible_max": 45.0,
        "aliases": [
            "mean corpuscular hemoglobin concentration",
            "mean corpuscular haemoglobin concentration",
            "mchc",
        ],
    },
    "RDW": {
        "canonical_unit": "%",
        "allowed_units": {"%": 1.0, "percent": 1.0},
        "plausible_min": 8.0,
        "plausible_max": 35.0,
        "aliases": [
            "red cell distribution width",
            "rdw",
            "rdw-cv",
        ],
    },
    "B12": {
        "canonical_unit": "pg/mL",
        "allowed_units": {"pg/mL": 1.0, "pmol/L": 1.355, "ng/L": 1.0},
        "plausible_min": 20.0,
        "plausible_max": 3000.0,
        "aliases": [
            "vitamin b12",
            "cyanocobalamin",
            "b12",
            "serum vitamin b12",
            "vit b12",
        ],
    },
    "FOLATE": {
        "canonical_unit": "ng/mL",
        "allowed_units": {"ng/mL": 1.0, "nmol/L": 0.441, "ug/L": 1.0},
        "plausible_min": 0.5,
        "plausible_max": 50.0,
        "aliases": [
            "folate",
            "serum folate",
            "folic acid",
            "vitamin b9",
        ],
    },
    "VITD": {
        "canonical_unit": "ng/mL",
        "allowed_units": {"ng/mL": 1.0, "nmol/L": 0.400},
        "plausible_min": 2.0,
        "plausible_max": 200.0,
        "aliases": [
            "vitamin d",
            "25-hydroxy vitamin d",
            "vit d3",
            "25-oh vitamin d",
        ],
    },
}


def match_parameter_alias(test_name: str, threshold: float = 80.0) -> Tuple[Optional[str], float]:
    """Matches a raw test name against standardized laboratory parameters using rapidfuzz."""
    clean_name = test_name.strip().lower()

    # Direct substring/exact fast-path
    for param_code, meta in PARAMETER_DEFINITIONS.items():
        if clean_name in meta["aliases"] or any(alias == clean_name for alias in meta["aliases"]):
            return param_code, 1.0

    # Fuzzy match across all aliases
    best_match_code = None
    best_score = 0.0

    for param_code, meta in PARAMETER_DEFINITIONS.items():
        match_result = process.extractOne(
            clean_name,
            meta["aliases"],
            scorer=fuzz.token_sort_ratio,
        )
        if match_result:
            _, score, _ = match_result
            if score > best_score and score >= threshold:
                best_score = score
                best_match_code = param_code

    if best_match_code:
        return best_match_code, round(best_score / 100.0, 4)
    return None, 0.0


def convert_unit(param_code: str, value: float, raw_unit: Optional[str]) -> Tuple[Optional[float], bool]:
    """Converts a value to its canonical unit using verified factor multipliers.

    Returns:
        (canonical_value, is_known_unit)
    """
    if param_code not in PARAMETER_DEFINITIONS or not raw_unit:
        return None, False

    clean_unit = raw_unit.strip()
    allowed = PARAMETER_DEFINITIONS[param_code]["allowed_units"]

    # Match unit case-insensitively
    factor = None
    for k, v in allowed.items():
        if k.lower() == clean_unit.lower():
            factor = v
            break

    if factor is not None:
        return round(value * factor, 2), True
    return None, False


def is_value_plausible(param_code: str, canonical_value: float) -> bool:
    """Checks whether a canonical value falls within the plausible biological minimum and maximum."""
    if param_code not in PARAMETER_DEFINITIONS:
        return True
    meta = PARAMETER_DEFINITIONS[param_code]
    return meta["plausible_min"] <= canonical_value <= meta["plausible_max"]

