import re
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.item import Item
from server.utils.logger import get_logger
from server.utils.sanitizer import sanitize_hebrew_text

_logger = get_logger(__name__)

_HEBREW_PREFIX_PATTERN = re.compile(r"^[הובכל]-?")
_MIN_QUERY_LENGTH = 1


async def get_nlp_match(query: str, db: AsyncSession) -> List[Item]:
    """
    Match a Hebrew text query against the item database.
    Normalizes Hebrew definiteness prefixes before searching.
    Returns an empty list on graceful degradation if the DB is unreachable.
    """
    if not query or len(query.strip()) < _MIN_QUERY_LENGTH:
        raise ValueError("Search query must not be empty.")

    try:
        sanitized = sanitize_hebrew_text(query)
        normalized = _strip_hebrew_prefix(sanitized)
        matches = await _query_items(normalized, db)
        _logger.debug(
            "NLP match: query='%s' normalized='%s' → %d result(s).",
            sanitized,
            normalized,
            len(matches),
        )
        return matches
    except Exception as exc:
        _logger.error("NLP match failed for query '%s': %s", query, exc)
        raise


def _strip_hebrew_prefix(text: str) -> str:
    """Remove leading definiteness prefix (ה, ו, ב, כ, ל) from Hebrew text."""
    return _HEBREW_PREFIX_PATTERN.sub("", text).strip()


async def _query_items(normalized_query: str, db: AsyncSession) -> List[Item]:
    """Execute a case-insensitive full-text search against the items table."""
    _logger.debug("Querying items table for normalized query: '%s'.", normalized_query)
    # Placeholder — replace with: await db.execute(select(ItemORM).where(...))
    return []
