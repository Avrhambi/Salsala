import re

from server.utils.logger import get_logger

_logger = get_logger(__name__)

_CREDIT_CARD_PATTERN = re.compile(
    r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"
)
_PHONE_PATTERN = re.compile(r"\b0\d{1,2}[\s\-]?\d{3}[\s\-]?\d{4}\b")
_CASHIER_ID_PATTERN = re.compile(r"קופאי[:\s]*\d+", re.UNICODE)
_REDACTION_PLACEHOLDER = "[REDACTED]"


def redact_pii_from_text(text: str) -> str:
    """
    Remove credit card numbers, Israeli phone numbers, and cashier IDs
    from OCR-extracted text before it is persisted to the cloud.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string.")

    try:
        redacted = _CREDIT_CARD_PATTERN.sub(_REDACTION_PLACEHOLDER, text)
        redacted = _PHONE_PATTERN.sub(_REDACTION_PLACEHOLDER, redacted)
        redacted = _CASHIER_ID_PATTERN.sub(_REDACTION_PLACEHOLDER, redacted)
        _logger.debug("PII redaction completed.")
        return redacted
    except Exception as exc:
        _logger.error("PII redaction failed: %s", exc)
        raise
