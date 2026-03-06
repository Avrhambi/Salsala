from typing import Any, Dict
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.services import list as list_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)


class SyncRequest(BaseModel):
    list_id: UUID
    item_update: Dict[str, Any]


async def handle_sync(
    request: SyncRequest,
    db: AsyncSession,
):
    """
    Orchestrate a real-time list sync.
    Validates the incoming shape, delegates to the list service,
    and maps internal errors to appropriate HTTP status codes.
    """
    if not request.item_update:
        raise HTTPException(status_code=422, detail="item_update must not be empty.")

    try:
        updated_list = await list_service.update_list_state(
            request.list_id, request.item_update, db
        )
        return updated_list
    except ValueError as exc:
        _logger.warning("Sync validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except NotImplementedError as exc:
        _logger.error("Sync not implemented: %s", exc)
        raise HTTPException(status_code=501, detail="Sync service not yet available.")
    except Exception as exc:
        _logger.error("Unexpected sync error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
