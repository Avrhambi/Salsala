"""
Unit tests for server/core/price_intelligence.py.

Covers: happy path trends, threshold boundary, insufficient data, and
invalid input validation. No DB or HTTP dependencies required.
"""
import pytest

from server.core.price_intelligence import calculate_price_trend
from shared.types import TrendValue

# ── Happy path ────────────────────────────────────────────────────────────────

def test_price_up_when_increase_exceeds_threshold():
    # 10.50 vs avg 9.00 → +16.7% → UP
    result = calculate_price_trend(10.50, [9.00, 9.00, 9.00])
    assert result == TrendValue.UP


def test_price_down_when_decrease_exceeds_threshold():
    # 8.00 vs avg 10.00 → -20% → DOWN
    result = calculate_price_trend(8.00, [10.00, 10.00, 10.00])
    assert result == TrendValue.DOWN


def test_price_stable_when_change_within_threshold():
    # 10.20 vs avg 10.00 → +2% → STABLE
    result = calculate_price_trend(10.20, [10.00])
    assert result == TrendValue.STABLE


def test_price_stable_when_current_equals_average():
    result = calculate_price_trend(5.00, [5.00, 5.00, 5.00])
    assert result == TrendValue.STABLE


def test_uses_average_of_all_historical_prices():
    # avg = (8 + 10 + 12) / 3 = 10.00; current = 11.00 → +10% → UP
    result = calculate_price_trend(11.00, [8.00, 10.00, 12.00])
    assert result == TrendValue.UP


# ── Threshold boundary ────────────────────────────────────────────────────────

def test_exactly_at_upper_threshold_is_stable():
    # +5% exactly → STABLE (threshold is strict >)
    result = calculate_price_trend(10.50, [10.00])
    assert result == TrendValue.STABLE


def test_just_above_upper_threshold_is_up():
    result = calculate_price_trend(10.51, [10.00])
    assert result == TrendValue.UP


def test_exactly_at_lower_threshold_is_stable():
    # -5% exactly → STABLE
    result = calculate_price_trend(9.50, [10.00])
    assert result == TrendValue.STABLE


def test_just_below_lower_threshold_is_down():
    result = calculate_price_trend(9.49, [10.00])
    assert result == TrendValue.DOWN


# ── Insufficient data ─────────────────────────────────────────────────────────

def test_returns_na_when_no_historical_prices():
    result = calculate_price_trend(10.00, [])
    assert result == TrendValue.NA


# ── Invalid input ─────────────────────────────────────────────────────────────

def test_raises_for_zero_current_price():
    with pytest.raises(ValueError, match="current_price must be greater than 0"):
        calculate_price_trend(0.0, [10.00])


def test_raises_for_negative_current_price():
    with pytest.raises(ValueError, match="current_price must be greater than 0"):
        calculate_price_trend(-1.0, [10.00])


def test_raises_when_historical_average_is_zero():
    # avg of [0, 0] = 0 → divide by zero
    with pytest.raises((ValueError, ZeroDivisionError)):
        calculate_price_trend(5.00, [0.0, 0.0])
