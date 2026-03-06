import logging
import os

_LOG_LEVEL_RAW = os.environ.get("LOG_LEVEL", "INFO").upper()
_LOG_LEVEL = getattr(logging, _LOG_LEVEL_RAW, logging.INFO)

logging.basicConfig(
    level=_LOG_LEVEL,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger bound to the central logging configuration."""
    return logging.getLogger(name)
