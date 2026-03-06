import re

from server.utils.logger import get_logger

_logger = get_logger(__name__)

_SCRIPT_TAG_PATTERN = re.compile(
    r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL
)
_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
_MAX_INPUT_LENGTH = 500


def sanitize_hebrew_text(text: str) -> str:
    """
    Strip script tags and HTML from user-supplied text to prevent XSS
    injection in collaborative list inputs. Enforces a maximum length.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, received {type(text).__name__}.")
    if len(text) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input exceeds the maximum allowed length of {_MAX_INPUT_LENGTH} characters."
        )

    try:
        sanitized = _SCRIPT_TAG_PATTERN.sub("", text)
        sanitized = _HTML_TAG_PATTERN.sub("", sanitized)
        return sanitized.strip()
    except Exception as exc:
        _logger.error("Failed to sanitize text input: %s", exc)
        raise
