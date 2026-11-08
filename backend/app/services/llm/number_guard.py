import re
from typing import Any, Dict, List, Set, Tuple, Union


def extract_numbers_from_json(obj: Any) -> Set[str]:
    """Recursively extracts all numeric values and numeric substrings from a JSON dictionary or list."""
    numbers: Set[str] = set()

    if isinstance(obj, dict):
        for v in obj.values():
            numbers.update(extract_numbers_from_json(v))
    elif isinstance(obj, list):
        for item in obj:
            numbers.update(extract_numbers_from_json(item))
    elif isinstance(obj, (int, float)):
        # Add exact representations
        numbers.add(str(obj))
        # Add rounded integer representation if float
        if isinstance(obj, float):
            numbers.add(str(int(round(obj))))
            numbers.add(f"{obj:.1f}")
            numbers.add(f"{obj:.2f}")
    elif isinstance(obj, str):
        # Extract embedded numbers from text string
        matches = re.findall(r"\b\d+(?:\.\d+)?\b", obj)
        for m in matches:
            numbers.add(m)
            try:
                val = float(m)
                numbers.add(str(int(round(val))))
                numbers.add(f"{val:.1f}")
                numbers.add(f"{val:.2f}")
            except ValueError:
                pass

    return numbers


def extract_numbers_from_text(text: str) -> List[str]:
    """Extracts all isolated numbers from LLM generated response text."""
    # Find all digits or decimals, excluding common dates/years (e.g. 2026) or percentages if desired
    tokens = re.findall(r"\b\d+(?:\.\d+)?\b", text)
    # Whitelist harmless formatting numbers (like bullet point numbers 1, 2, 3)
    whitelisted = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "2026", "2020"}
    return [t for t in tokens if t not in whitelisted]


class NumberGuard:
    """Deterministic validator that inspects LLM answers to prevent hallucinated numbers."""

    @classmethod
    def audit_llm_response(cls, response_text: str, source_json: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Compares numbers present in LLM response against numbers present in the authorized input JSON.

        Returns:
            (is_valid, list_of_hallucinated_numbers)
        """
        allowed_numbers = extract_numbers_from_json(source_json)
        response_numbers = extract_numbers_from_text(response_text)

        unauthorized_numbers = []
        for num in response_numbers:
            # Check if num or float equivalent is in allowed_numbers
            is_allowed = False
            if num in allowed_numbers:
                is_allowed = True
            else:
                try:
                    num_f = float(num)
                    for allowed in allowed_numbers:
                        try:
                            if abs(float(allowed) - num_f) < 0.05:
                                is_allowed = True
                                break
                        except ValueError:
                            pass
                except ValueError:
                    pass

            if not is_allowed:
                unauthorized_numbers.append(num)

        is_valid = len(unauthorized_numbers) == 0
        return is_valid, unauthorized_numbers

