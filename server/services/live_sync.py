from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.list import ShoppingList
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def update_list_state(
    list_id: UUID, item_update: Dict[str, Any], db: AsyncSession
) -> ShoppingList:
    """
    Apply a Last-Write-Wins update to a shared list and persist the new state.
    Returns the updated ShoppingList for WebSocket broadcast.
    """
    if not item_update:
        raise ValueError("item_update payload must not be empty.")

    try:
        current_list = await _fetch_list(list_id, db)
        updated_list = _apply_lww_update(current_list, item_update)
        await _persist_list(updated_list, db)
        _logger.info(
            "List %s state updated at %s.", list_id, updated_list.sync_timestamp
        )
        return updated_list
    except Exception as exc:
        _logger.error("Failed to update state for list %s: %s", list_id, exc)
        raise


async def _fetch_list(list_id: UUID, db: AsyncSession) -> ShoppingList:
    """Retrieve the current list state from the database."""
    _logger.debug("Fetching list %s.", list_id)
    # Placeholder — replace with: await db.get(ShoppingListORM, list_id)
    raise NotImplementedError("Database layer not yet connected.")


def _apply_lww_update(
    current_list: ShoppingList, update: Dict[str, Any]
) -> ShoppingList:
    """Merge the incoming update using Last-Write-Wins strategy."""
    return current_list.model_copy(
        update={"sync_timestamp": datetime.now(tz=timezone.utc)}
    )


async def _persist_list(updated_list: ShoppingList, db: AsyncSession) -> None:
    """Write the updated list state back to the database."""
    _logger.debug("Persisting list %s.", updated_list.list_id)
    # Placeholder — replace with: db.add(updated_orm); await db.commit()
