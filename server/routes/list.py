from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from server.controllers.list import SyncRequest, handle_sync
from server.db.client import get_db_session
from server.utils.logger import get_logger

_logger = get_logger(__name__)

router = APIRouter(prefix="/list", tags=["List"])


@router.post("/sync")
async def sync_list(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await handle_sync(request, db)


@router.websocket("/ws/{list_id}")
async def websocket_sync(websocket: WebSocket, list_id: str):
    """
    WebSocket endpoint for real-time collaborative list synchronization.
    Broadcasts state changes to all connected household members.
    """
    await websocket.accept()
    _logger.info("WebSocket connection opened for list %s.", list_id)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({"status": "received", "list_id": list_id, "data": data})
    except WebSocketDisconnect:
        _logger.info("WebSocket connection closed for list %s.", list_id)
