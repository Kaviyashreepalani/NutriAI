import pytest
from app.services.llm.number_guard import NumberGuard


def test_number_guard_accepts_valid_json_numbers():
    context_json = {
        "iron_mg": 4.5,
        "vit_c_mg": 25.0,
        "cost_inr": 22.50,
        "serving_size_g": 35,
    }

    # Answer only includes numbers from context JSON
    valid_answer = (
        "This product is optimized with 4.5 mg of iron per 35 g serving, "
        "paired with 25 mg of vitamin C at a cost of 22.50."
    )
    is_valid, hallucinations = NumberGuard.audit_llm_response(valid_answer, context_json)
    assert is_valid is True
    assert len(hallucinations) == 0


def test_number_guard_rejects_hallucinated_numbers():
    context_json = {
        "iron_mg": 4.5,
        "cost_inr": 22.50,
    }

    # Answer includes hallucinated dosage or nutrient amount (e.g., 99.9, 1500)
    hallucinated_answer = (
        "Take this bar containing 99.9 mg iron to increase your levels by 1500 percent."
    )
    is_valid, hallucinations = NumberGuard.audit_llm_response(hallucinated_answer, context_json)
    assert is_valid is False
    assert "99.9" in hallucinations or "1500" in hallucinations

