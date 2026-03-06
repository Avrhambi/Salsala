from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.controllers.store import RecommendationRequest, handle_recommendation
from server.db.client import get_db_session

router = APIRouter(prefix="/store", tags=["Store"])


@router.post("/recommend")
async def recommend_stores(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await handle_recommendation(request, db)
