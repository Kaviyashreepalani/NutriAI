import os
import pytest
from app.services.ocr.normalizer import convert_unit, is_value_plausible, match_parameter_alias
from app.services.ocr.parser import (
    extract_metadata,
    extract_text_from_pdf,
    parse_lab_lines,
    sniff_mime_type,
    validate_file_upload,
)


def test_mime_sniffing():
    assert sniff_mime_type(b"%PDF-1.4 test") == "application/pdf"
    assert sniff_mime_type(b"\xff\xd8\xff\xe0 test") == "image/jpeg"
    assert sniff_mime_type(b"\x89PNG\r\n\x1a\n test") == "image/png"
    assert sniff_mime_type(b"plain text document") == "application/octet-stream"


def test_unit_conversion():
    # Haemoglobin g/L to g/dL (factor 0.1)
    val, ok = convert_unit("HB", 120.0, "g/L")
    assert ok is True
    assert val == 12.0

    # Ferritin ug/L to ng/mL (factor 1.0)
    val, ok = convert_unit("FERRITIN", 25.0, "ug/L")
    assert ok is True
    assert val == 25.0

    # Unknown unit
    val, ok = convert_unit("HB", 12.0, "unknown_unit")
    assert ok is False


def test_parameter_alias_matching():
    code, score = match_parameter_alias("Haemoglobin")
    assert code == "HB"
    assert score >= 0.90

    code, score = match_parameter_alias("S. Ferritin")
    assert code == "FERRITIN"
    assert score >= 0.85

    code, score = match_parameter_alias("MCV")
    assert code == "MCV"


def test_plausible_ranges():
    assert is_value_plausible("HB", 12.5) is True
    assert is_value_plausible("HB", 2.0) is False   # Biological floor
    assert is_value_plausible("HB", 35.0) is False  # Biological ceiling


def test_synthetic_adolescent_fixture():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "sample_report_adolescent.pdf")
    assert os.path.exists(fixture_path), "Adolescent fixture PDF must exist"

    with open(fixture_path, "rb") as f:
        pdf_bytes = f.read()

    full_text, lines = extract_text_from_pdf(pdf_bytes)
    assert len(lines) > 0
    assert "SYNTHETIC" in full_text and "SAMPLE" in full_text

    parsed = parse_lab_lines(lines)
    assert len(parsed) >= 2

    hb_rows = [r for r in parsed if r["parameter_code"] == "HB"]
    assert len(hb_rows) == 1
    assert hb_rows[0]["value_numeric"] == 10.8
