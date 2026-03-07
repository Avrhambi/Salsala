import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.client import get_db_session
from server.services import list as list_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)

router = APIRouter(prefix="/list", tags=["List"])


class CreateListRequest(BaseModel):
    name: str
    users: List[uuid.UUID]


class AddItemRequest(BaseModel):
    item_id: str
    quantity: int = 1


class RenameListRequest(BaseModel):
    name: str


@router.post("/create", status_code=201)
async def create_list(
    request: CreateListRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.create_list(request.users, request.name, db)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error("create_list failed: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/history/{user_id}")
async def get_history(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.get_history(uuid.UUID(user_id), db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        _logger.error("get_history failed for user %s: %s", user_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/{list_id}")
async def get_list(
    list_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.get_list_by_id(uuid.UUID(list_id), db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("get_list failed for %s: %s", list_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.patch("/{list_id}")
async def rename_list(
    list_id: str,
    request: RenameListRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.rename_list(uuid.UUID(list_id), request.name, db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("rename_list failed for %s: %s", list_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete("/{list_id}", status_code=204)
async def delete_list(
    list_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        await list_service.delete_list(uuid.UUID(list_id), db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("delete_list failed for %s: %s", list_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/{list_id}/items")
async def add_item(
    list_id: str,
    request: AddItemRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.add_item_to_list(uuid.UUID(list_id), request.item_id, request.quantity, db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("add_item failed for list %s: %s", list_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.delete("/{list_id}/items/{item_id}")
async def remove_item(
    list_id: str,
    item_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.remove_item_from_list(uuid.UUID(list_id), uuid.UUID(item_id), db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("remove_item failed for list %s item %s: %s", list_id, item_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.patch("/{list_id}/items/{item_id}/bought")
async def mark_item_bought(
    list_id: str,
    item_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await list_service.mark_item_bought(uuid.UUID(list_id), uuid.UUID(item_id), db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        _logger.error("mark_item_bought failed for list %s item %s: %s", list_id, item_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
