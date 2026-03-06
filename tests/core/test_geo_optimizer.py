"""
Unit tests for server/core/geo_optimizer.py.

Covers: ranking, top-3 cap, data sufficiency filtering, item filtering,
empty inputs, and invalid input validation.
No DB or HTTP dependencies required.
"""
import uuid

import pytest

from server.core.geo_optimizer import (
    MINIMUM_DATA_POINTS,
    TOP_STORE_RESULT_LIMIT,
    calculate_optimal_basket,
)
from server.models.benchmark import Benchmark

# ── Fixtures / helpers ────────────────────────────────────────────────────────

ITEM_A = uuid.uuid4()
ITEM_B = uuid.uuid4()
STORE_1 = uuid.uuid4()
STORE_2 = uuid.uuid4()
STORE_3 = uuid.uuid4()
STORE_4 = uuid.uuid4()


def make_benchmark(item_id: uuid.UUID, store_id: uuid.UUID, avg: float, points: int = MINIMUM_DATA_POINTS) -> Benchmark:
    return Benchmark(item_id=item_id, store_id=store_id, national_avg=avg, data_points=points)


# ── Happy path ────────────────────────────────────────────────────────────────

def test_single_store_single_item_returns_one_result():
    benchmarks = [make_benchmark(ITEM_A, STORE_1, 5.00)]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert len(result) == 1
    assert result[0].store_id == STORE_1
    assert result[0].total_basket_cost == pytest.approx(5.00)
    assert result[0].item_count == 1


def test_stores_ranked_ascending_by_basket_cost():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 10.00),
        make_benchmark(ITEM_A, STORE_2, 7.00),
        make_benchmark(ITEM_A, STORE_3, 12.00),
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    costs = [r.total_basket_cost for r in result]
    assert costs == sorted(costs)


def test_basket_cost_sums_multiple_items_per_store():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 5.00),
        make_benchmark(ITEM_B, STORE_1, 3.00),
    ]
    result = calculate_optimal_basket([ITEM_A, ITEM_B], benchmarks)
    assert result[0].total_basket_cost == pytest.approx(8.00)
    assert result[0].item_count == 2


def test_cheapest_store_is_first():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 20.00),
        make_benchmark(ITEM_A, STORE_2, 5.00),
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert result[0].store_id == STORE_2


# ── Top-3 cap ─────────────────────────────────────────────────────────────────

def test_returns_at_most_top_store_result_limit():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 10.00),
        make_benchmark(ITEM_A, STORE_2, 9.00),
        make_benchmark(ITEM_A, STORE_3, 8.00),
        make_benchmark(ITEM_A, STORE_4, 7.00),
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert len(result) == TOP_STORE_RESULT_LIMIT


def test_returns_fewer_than_limit_when_fewer_stores_exist():
    benchmarks = [make_benchmark(ITEM_A, STORE_1, 5.00)]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert len(result) == 1


# ── Data sufficiency filtering ────────────────────────────────────────────────

def test_benchmarks_below_minimum_data_points_are_excluded():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 5.00, points=MINIMUM_DATA_POINTS - 1),
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert result == []


def test_only_sufficient_benchmarks_contribute_to_ranking():
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 5.00, points=MINIMUM_DATA_POINTS),      # valid
        make_benchmark(ITEM_A, STORE_2, 3.00, points=MINIMUM_DATA_POINTS - 1),  # filtered
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert len(result) == 1
    assert result[0].store_id == STORE_1


# ── Item filtering ────────────────────────────────────────────────────────────

def test_benchmarks_for_unrequested_items_are_ignored():
    unrelated_item = uuid.uuid4()
    benchmarks = [make_benchmark(unrelated_item, STORE_1, 99.00)]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert result == []


def test_only_requested_items_contribute_to_basket_cost():
    unrelated_item = uuid.uuid4()
    benchmarks = [
        make_benchmark(ITEM_A, STORE_1, 5.00),
        make_benchmark(unrelated_item, STORE_1, 100.00),
    ]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert result[0].total_basket_cost == pytest.approx(5.00)


# ── Empty / edge inputs ───────────────────────────────────────────────────────

def test_empty_benchmarks_returns_empty_list():
    result = calculate_optimal_basket([ITEM_A], [])
    assert result == []


def test_all_benchmarks_filtered_returns_empty_list():
    benchmarks = [make_benchmark(ITEM_A, STORE_1, 5.00, points=0)]
    result = calculate_optimal_basket([ITEM_A], benchmarks)
    assert result == []


# ── Invalid input ─────────────────────────────────────────────────────────────

def test_raises_for_empty_item_ids():
    with pytest.raises(ValueError, match="item_ids must not be empty"):
        calculate_optimal_basket([], [make_benchmark(ITEM_A, STORE_1, 5.00)])
