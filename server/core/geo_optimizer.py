from typing import List
from uuid import UUID

from pydantic import BaseModel

from server.models.benchmark import Benchmark
from server.utils.logger import get_logger

_logger = get_logger(__name__)

TOP_STORE_RESULT_LIMIT = 3
MINIMUM_DATA_POINTS = 3


class StoreRank(BaseModel):
    """Ranked store result from the geographic basket optimizer."""

    store_id: UUID
    total_basket_cost: float
    item_count: int


def calculate_optimal_basket(
    item_ids: List[UUID],
    store_benchmarks: List[Benchmark],
) -> List[StoreRank]:
    """
    Rank stores by ascending total basket cost for the given item list.

    Groups crowdsourced benchmarks by store, sums national_avg for each
    item present, and returns the top-ranked stores. Benchmarks with
    insufficient data points are excluded.

    Pure logic — no database or HTTP dependencies.
    """
    if not item_ids:
        raise ValueError("item_ids must not be empty.")
    if not store_benchmarks:
        _logger.warning("No store benchmarks provided; returning empty rankings.")
        return []

    try:
        valid = _filter_by_data_sufficiency(store_benchmarks)
        store_totals = _aggregate_by_store(item_ids, valid)
        ranked = sorted(store_totals, key=lambda r: r.total_basket_cost)

        _logger.debug(
            "Basket optimization: %d items, %d eligible benchmarks, %d stores ranked.",
            len(item_ids),
            len(valid),
            len(ranked),
        )
        return ranked[:TOP_STORE_RESULT_LIMIT]

    except Exception as exc:
        _logger.error("calculate_optimal_basket failed: %s", exc)
        raise


def _filter_by_data_sufficiency(benchmarks: List[Benchmark]) -> List[Benchmark]:
    """Exclude benchmarks with too few data points to be statistically reliable."""
    return [b for b in benchmarks if b.data_points >= MINIMUM_DATA_POINTS]


def _aggregate_by_store(
    item_ids: List[UUID], benchmarks: List[Benchmark]
) -> List[StoreRank]:
    """Sum benchmark national_avg per store for all requested item_ids."""
    item_id_set = set(item_ids)
    store_costs: dict[UUID, float] = {}
    store_counts: dict[UUID, int] = {}

    for benchmark in benchmarks:
        if benchmark.item_id not in item_id_set:
            continue
        store_id = benchmark.store_id
        store_costs[store_id] = store_costs.get(store_id, 0.0) + benchmark.national_avg
        store_counts[store_id] = store_counts.get(store_id, 0) + 1

    return [
        StoreRank(
            store_id=store_id,
            total_basket_cost=round(total, 2),
            item_count=store_counts[store_id],
        )
        for store_id, total in store_costs.items()
    ]
