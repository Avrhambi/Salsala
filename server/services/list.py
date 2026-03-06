from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.list import ShoppingList
from server.services import live_sync
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def update_list_state(
    list_id: UUID, item_update: Dict[str, Any], db: AsyncSession
) -> ShoppingList:
    """
    Orchestrate a collaborative list update.
    Delegates sync logic to the live_sync sub-module to stay within
    the 150-line complexity limit.
    """
    if not list_id:
        raise ValueError("list_id must not be None.")
    if not item_update:
        raise ValueError("item_update payload must not be empty.")

    try:
        return await live_sync.update_list_state(list_id, item_update, db)
    except Exception as exc:
        _logger.error("list.update_list_state failed for %s: %s", list_id, exc)
        raise
