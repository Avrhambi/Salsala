from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.controllers.item import SearchRequest, handle_search
from server.db.client import get_db_session

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/search")
async def search_items(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await handle_search(request, db)
