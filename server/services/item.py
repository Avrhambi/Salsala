from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.item import Item
from server.services import hebrew_nlp
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def get_nlp_match(query: str, db: AsyncSession) -> List[Item]:
    """
    Search for items matching a Hebrew text query.
    Delegates NLP processing to the hebrew_nlp sub-module.
    Falls back to an empty list if the smart database is unreachable,
    ensuring the user can still add a custom item.
    """
    if not query or not query.strip():
        raise ValueError("Search query must not be empty.")

    try:
        return await hebrew_nlp.get_nlp_match(query, db)
    except NotImplementedError:
        _logger.warning(
            "NLP database unavailable — graceful degradation to empty result."
        )
        return []
    except Exception as exc:
        _logger.error("item.get_nlp_match failed for query '%s': %s", query, exc)
        raise


async def get_item_by_id(item_id: UUID, db: AsyncSession) -> Item:
    """Retrieve a single item by its UUID."""
    if not item_id:
        raise ValueError("item_id must not be None.")

    try:
        _logger.debug("Fetching item %s.", item_id)
        # Placeholder — replace with: await db.get(ItemORM, item_id)
        raise NotImplementedError("Database layer not yet connected.")
    except Exception as exc:
        _logger.error("item.get_item_by_id failed for %s: %s", item_id, exc)
        raise
