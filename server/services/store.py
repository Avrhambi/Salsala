from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.benchmark import Benchmark
from server.utils.logger import get_logger
from shared.types import GeoCoordinates

_logger = get_logger(__name__)

TOP_STORE_RESULT_LIMIT = 3
MINIMUM_BENCHMARK_DATA_POINTS = 3


async def get_optimal_basket(
    list_id: UUID, coordinates: GeoCoordinates, db: AsyncSession
) -> List[dict]:
    """
    Calculate the top stores for a user's active shopping list based on
    crowdsourced price benchmarks and GPS proximity.
    Returns up to TOP_STORE_RESULT_LIMIT store recommendations.
    """
    if not list_id:
        raise ValueError("list_id must not be None.")

    try:
        benchmarks = await _fetch_nearby_benchmarks(coordinates, db)
        valid_benchmarks = _filter_by_data_sufficiency(benchmarks)
        ranked_stores = _rank_stores_by_basket_cost(valid_benchmarks)
        top_stores = ranked_stores[:TOP_STORE_RESULT_LIMIT]

        _logger.info(
            "Basket optimization for list %s: %d stores found near (%.4f, %.4f).",
            list_id,
            len(top_stores),
            coordinates.latitude,
            coordinates.longitude,
        )
        return top_stores
    except Exception as exc:
        _logger.error(
            "get_optimal_basket failed for list %s: %s", list_id, exc
        )
        raise


async def _fetch_nearby_benchmarks(
    coordinates: GeoCoordinates, db: AsyncSession
) -> List[Benchmark]:
    """Query benchmarks from stores within a geographic radius."""
    _logger.debug(
        "Fetching benchmarks near (%.4f, %.4f).",
        coordinates.latitude,
        coordinates.longitude,
    )
    # Placeholder — replace with geo-indexed DB query using PostGIS or similar
    return []


def _filter_by_data_sufficiency(benchmarks: List[Benchmark]) -> List[Benchmark]:
    """Exclude benchmarks with too few data points to be statistically reliable."""
    return [b for b in benchmarks if b.data_points >= MINIMUM_BENCHMARK_DATA_POINTS]


def _rank_stores_by_basket_cost(benchmarks: List[Benchmark]) -> List[dict]:
    """Sort stores by ascending total basket cost derived from benchmark averages."""
    # Placeholder — replace with real basket aggregation per store
    return []
