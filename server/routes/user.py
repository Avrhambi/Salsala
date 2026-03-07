from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.client import get_db_session
from server.services import user as user_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)

router = APIRouter(prefix="/user", tags=["User"])


class CreateUserRequest(BaseModel):
    display_name: str


@router.post("/create")
async def create_user(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db_session),
):
    try:
        return await user_service.create_user(request.display_name, db)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error("create_user failed: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
