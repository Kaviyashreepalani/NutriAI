from datetime import date
import pytest
from app.services.assessment.evaluator import determine_life_stage, evaluate_clinical_safety


def test_age_boundary_evaluation():
    # 8-year-old child -> out of scope
    dob_child = date(2018, 1, 1)
    stage, age = determine_life_stage(dob_child)
    assert stage is None
    res = evaluate_clinical_safety(age, stage, {})
    assert res["safety_status"] == "blocked"

    # 16-year-old adolescent -> girl_16_18
    dob_teen = date(2010, 5, 1)
    stage, age = determine_life_stage(dob_teen)
    assert stage == "girl_16_18"


def test_haemoglobin_severity_bands():
    # Normal Hb >= 12.0
    res = evaluate_clinical_safety(25.0, "woman_19_35", {"HB": 12.8})
    assert res["safety_status"] == "ok"

    # Mild Hb (10.0 - 11.9)
    res = evaluate_clinical_safety(25.0, "woman_19_35", {"HB": 10.5})
    assert res["safety_status"] == "caution"

    # Moderate Hb (7.0 - 9.9)
    res = evaluate_clinical_safety(25.0, "woman_19_35", {"HB": 8.5})
    assert res["safety_status"] == "refer_to_doctor"

    # Severe Hb (< 7.0) -> BLOCKED
    res = evaluate_clinical_safety(25.0, "woman_19_35", {"HB": 6.2})
    assert res["safety_status"] == "blocked"


def test_non_iron_anaemia_safeguard():
    # Low MCV (68) with elevated ferritin (180) -> differential alert, iron target dampened
    res = evaluate_clinical_safety(28.0, "woman_19_35", {"HB": 10.2, "MCV": 68.0, "FERRITIN": 180.0})
    assert res["safety_status"] == "refer_to_doctor"
    non_iron_finding = [f for f in res["findings"] if f["rule_id"] == "NON_IRON_ANAEMIA_SAFEGUARD"]
    assert len(non_iron_finding) == 1
    # Check iron target is dampened
    assert res["nutrient_targets"]["iron_max_mg"] <= 3.5


def test_pregnancy_flag():
    res = evaluate_clinical_safety(26.0, "woman_19_35", {"HB": 11.5}, pregnancy_status="pregnant_trimester_2")
    preg_finding = [f for f in res["findings"] if f["rule_id"] == "PREGNANCY_LACTATION_FLAG"]
    assert len(preg_finding) == 1

