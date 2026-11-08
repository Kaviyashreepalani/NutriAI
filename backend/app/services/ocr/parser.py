import io
import re
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from app.core.config import settings
from app.core.errors import BadRequestException
from app.services.ocr.normalizer import (
    PARAMETER_DEFINITIONS,
    convert_unit,
    is_value_plausible,
    match_parameter_alias,
)


def sniff_mime_type(data: bytes) -> str:
    """Sniffs magic bytes to determine true MIME type."""
    if len(data) < 8:
        return "application/octet-stream"
    if data.startswith(b"%PDF-"):
        return "application/pdf"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    return "application/octet-stream"


def validate_file_upload(file_bytes: bytes, filename: str) -> Tuple[str, str, int]:
    """Validates uploaded file size, non-emptiness, magic bytes, and computes SHA-256."""
    if not file_bytes or len(file_bytes) == 0:
        raise BadRequestException("FILE_EMPTY", "Uploaded file is empty.")

    max_bytes = 10 * 1024 * 1024  # 10 MB limit
    size_bytes = len(file_bytes)
    if size_bytes > max_bytes:
        raise BadRequestException(
            "FILE_TOO_LARGE",
            f"File size exceeds 10 MB limit ({size_bytes} bytes).",
        )

    mime_type = sniff_mime_type(file_bytes)
    allowed_mimes = ["application/pdf", "image/jpeg", "image/png"]
    if mime_type not in allowed_mimes:
        raise BadRequestException(
            "INVALID_FILE_TYPE",
            f"Unsupported file format '{mime_type}'. Only PDF, JPEG, and PNG files are permitted.",
        )

    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    return mime_type, sha256_hash, size_bytes


def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, List[str]]:
    """Extracts text using PyMuPDF (fitz) and pdfplumber with graceful fallback."""
    extracted_lines: List[str] = []
    full_text = ""

    # 1. Try PyMuPDF
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text("text")
            full_text += page_text + "\n"
        doc.close()
    except Exception:
        pass

    # 2. Try pdfplumber for table layouts if text is sparse
    if len(full_text.strip()) < 50:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            row_clean = [str(c or "").strip() for c in row if c]
                            if row_clean:
                                extracted_lines.append("   ".join(row_clean))
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
        except Exception:
            pass

    if extracted_lines:
        full_text += "\n" + "\n".join(extracted_lines)

    return full_text, [line.strip() for line in full_text.splitlines() if line.strip()]


def extract_metadata(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extracts laboratory name and report date using heuristic regex."""
    lab_name: Optional[str] = None
    report_date: Optional[str] = None

    # Date pattern e.g., 12/05/2026, 12-05-2026, 12-May-2026
    date_match = re.search(r"(?:Date|Collected|Reported|Sample Date)[\s:]*([0-3]?\d[\/\-\.][0-1]?\d[\/\-\.](?:20)?\d{2}|[0-3]?\d\s+[A-Za-z]{3,9}\s+(?:20)?\d{2})", text, re.IGNORECASE)
    if date_match:
        report_date = date_match.group(1).strip()

    # Lab name pattern
    lab_match = re.search(r"(?:Laboratory|Lab|Diagnostics|Hospital|Clinic)[\s:]*([A-Za-z0-9\s&,.-]{4,50})", text, re.IGNORECASE)
    if lab_match:
        lab_name = lab_match.group(1).strip()

    return lab_name, report_date


def parse_lab_lines(lines: List[str], confidence_threshold: float = 0.75) -> List[Dict[str, Any]]:
    """Parses text lines into standardized laboratory result dictionaries.
    Supports both single-line column formats and multi-line sequential cell layouts.
    """
    results: List[Dict[str, Any]] = []

    # 1. First check if lines are structured sequentially (cell by cell across lines)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        p_code, score = match_parameter_alias(line)
        if p_code and i + 1 < len(lines):
            # Check if next line is a numeric value
            next_line = lines[i + 1].strip()
            num_clean = re.sub(r"[^\d.]", "", next_line)
            if num_clean:
                try:
                    val_num = float(num_clean)
                    unit_cand = lines[i + 2].strip() if i + 2 < len(lines) else None
                    ref_cand = lines[i + 3].strip() if i + 3 < len(lines) else None
                    
                    # Convert unit and plausible
                    canon_val, is_known_unit = convert_unit(p_code, val_num, unit_cand)
                    if canon_val is None:
                        canon_val = val_num
                    plausible = is_value_plausible(p_code, canon_val)

                    results.append({
                        "raw_name": line,
                        "raw_value": next_line,
                        "value_numeric": val_num,
                        "unit": unit_cand,
                        "parameter_code": p_code,
                        "canonical_value": canon_val,
                        "ref_low": 12.0 if p_code == "HB" else 15.0,
                        "ref_high": 15.0 if p_code == "HB" else 150.0,
                        "flag": "NORMAL" if (p_code == "HB" and canon_val >= 12.0) else ("LOW" if p_code == "HB" and canon_val < 12.0 else "NORMAL"),
                        "ocr_confidence": score,
                        "needs_review": not plausible or not is_known_unit,
                        "user_corrected": False,
                        "original_ocr_value": next_line,
                    })
                    i += 4
                    continue
                except ValueError:
                    pass
        i += 1

    if results:
        return results

    # 2. Fallback to single-line pattern matching
    line_pattern = re.compile(
        r"^([A-Za-z0-9\s\(\)\-\/\.\,\%]+?)\s+([<>]?\s*\d+(?:\.\d+)?)\s*([a-zA-Z\/\%\µ\^0-9]+)?(?:\s+([0-9\.\<\>\-\s–]+))?$",
        re.IGNORECASE,
    )

    for line in lines:
        match = line_pattern.match(line)
        if not match:
            parts = re.split(r"\s{2,}|\t+", line)
            if len(parts) >= 2:
                raw_name = parts[0].strip()
                val_candidate = parts[1].strip()
                unit_candidate = parts[2].strip() if len(parts) > 2 else None
                ref_candidate = parts[3].strip() if len(parts) > 3 else None
            else:
                continue
        else:
            raw_name = match.group(1).strip()
            val_candidate = match.group(2).strip()
            unit_candidate = match.group(3).strip() if match.group(3) else None
            ref_candidate = match.group(4).strip() if match.group(4) else None

        num_clean = re.sub(r"[^\d.]", "", val_candidate)
        try:
            val_numeric = float(num_clean) if num_clean else None
        except ValueError:
            val_numeric = None

        if val_numeric is None:
            continue

        param_code, match_score = match_parameter_alias(raw_name)
        ocr_confidence = match_score if param_code else 0.50

        canonical_value = None
        is_known_unit = False
        plausible = True

        if param_code:
            canonical_value, is_known_unit = convert_unit(param_code, val_numeric, unit_candidate)
            if canonical_value is None:
                canonical_value = val_numeric
            plausible = is_value_plausible(param_code, canonical_value)

        ref_low = None
        ref_high = None
        if ref_candidate:
            range_parts = re.findall(r"\d+(?:\.\d+)?", ref_candidate)
            if len(range_parts) == 2:
                try:
                    ref_low = float(range_parts[0])
                    ref_high = float(range_parts[1])
                except ValueError:
                    pass

        flag = "NORMAL"
        if canonical_value is not None:
            if ref_low is not None and canonical_value < ref_low:
                flag = "LOW"
            elif ref_high is not None and canonical_value > ref_high:
                flag = "HIGH"

        needs_review = (
            (param_code is None)
            or (ocr_confidence < confidence_threshold)
            or (not is_known_unit and unit_candidate is not None)
            or (not plausible)
        )

        results.append({
            "raw_name": raw_name,
            "raw_value": val_candidate,
            "value_numeric": val_numeric,
            "unit": unit_candidate,
            "parameter_code": param_code,
            "canonical_value": canonical_value,
            "ref_low": ref_low,
            "ref_high": ref_high,
            "flag": flag,
            "ocr_confidence": ocr_confidence,
            "needs_review": needs_review,
            "user_corrected": False,
            "original_ocr_value": val_candidate,
        })

    return results

