from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.services import store as store_service
from server.utils.logger import get_logger
from shared.types import GeoCoordinates

_logger = get_logger(__name__)


class RecommendationRequest(BaseModel):
    list_id: UUID
    coordinates: GeoCoordinates


async def handle_recommendation(
    request: RecommendationRequest,
    db: AsyncSession,
):
    """
    Return the top-3 store recommendations for a user's active list,
    ranked by total basket cost at each nearby store.
    Pydantic validates list_id and GeoCoordinates bounds at deserialization.
    """
    try:
        top_stores = await store_service.get_optimal_basket(
            request.list_id, request.coordinates, db
        )
        return {"stores": top_stores, "count": len(top_stores)}
    except ValueError as exc:
        _logger.warning("Recommendation validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error(
            "Unexpected recommendation error for list %s: %s", request.list_id, exc
        )
        raise HTTPException(status_code=500, detail="Internal server error.")
