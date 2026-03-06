from typing import List, Tuple

from server.services.pii_redactor import redact_pii_from_text
from server.utils.logger import get_logger

_logger = get_logger(__name__)

_MAX_CONFIDENCE = 1.0
_EMPTY_LINE_THRESHOLD = 0


def extract_items_from_receipt_text(
    raw_ocr_text: str,
) -> Tuple[List[dict], float]:
    """
    Parse OCR output into item-price pairs and an overall confidence score.
    PII is redacted before any further processing.
    Returns a tuple of (parsed_items, confidence_score).
    """
    if not raw_ocr_text or not raw_ocr_text.strip():
        raise ValueError("raw_ocr_text must not be empty.")

    try:
        clean_text = redact_pii_from_text(raw_ocr_text)
        line_items = _parse_line_items(clean_text)
        confidence = _estimate_confidence(line_items, clean_text)
        _logger.debug(
            "OCR extraction: %d items parsed, confidence=%.2f.",
            len(line_items),
            confidence,
        )
        return line_items, confidence
    except Exception as exc:
        _logger.error("OCR extraction failed: %s", exc)
        raise


def _parse_line_items(text: str) -> List[dict]:
    """
    Split OCR text into individual line items.
    Placeholder — replace with a Hebrew NER/regex receipt parser.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return [{"raw_line": line} for line in lines]


def _estimate_confidence(line_items: List[dict], text: str) -> float:
    """
    Estimate OCR confidence as the ratio of parseable lines to total lines.
    Placeholder — replace with model-based scoring.
    """
    total_lines = len([l for l in text.splitlines() if l.strip()])
    if total_lines == _EMPTY_LINE_THRESHOLD:
        return 0.0
    return min(len(line_items) / total_lines, _MAX_CONFIDENCE)
