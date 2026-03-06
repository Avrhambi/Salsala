from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.services import item as item_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)


class SearchRequest(BaseModel):
    query: str


async def handle_search(
    request: SearchRequest,
    db: AsyncSession,
):
    """
    Handle an item search request using Hebrew NLP matching.
    Returns an empty list on graceful degradation — never blocks the user.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=422, detail="Search query must not be empty.")

    try:
        matches = await item_service.get_nlp_match(request.query, db)
        return {"items": matches, "count": len(matches)}
    except ValueError as exc:
        _logger.warning("Search validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error("Unexpected search error for query '%s': %s", request.query, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
