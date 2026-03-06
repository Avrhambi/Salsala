"""
Unit tests for server/core/winsorization.py.

Covers: happy path averaging, outlier clipping, custom percentiles,
edge cases at boundaries, and invalid input validation.
No DB or HTTP dependencies required.
"""
import pytest

from server.core.winsorization import calculate_winsorized_average

# ── Happy path ────────────────────────────────────────────────────────────────

def test_returns_mean_when_no_outliers():
    # Symmetric distribution — winsorizing has no effect
    prices = [10.0, 10.0, 10.0, 10.0, 10.0]
    result = calculate_winsorized_average(prices)
    assert result == pytest.approx(10.0)


def test_clips_high_outlier():
    # 100 is far above the 90th percentile of [1,2,3,4,100]
    prices = [1.0, 2.0, 3.0, 4.0, 100.0]
    result = calculate_winsorized_average(prices)
    # Without clipping: avg = 22.0; with clipping the high end is pulled down
    assert result < 22.0


def test_clips_low_outlier():
    prices = [0.01, 10.0, 10.0, 10.0, 10.0]
    result = calculate_winsorized_average(prices)
    # Low outlier is clipped up, result should be close to 10
    assert result > 5.0


def test_two_price_minimum_succeeds():
    result = calculate_winsorized_average([5.0, 15.0])
    assert isinstance(result, float)


def test_uniform_prices_return_same_value():
    result = calculate_winsorized_average([7.5] * 10)
    assert result == pytest.approx(7.5)


# ── Custom percentiles ────────────────────────────────────────────────────────

def test_zero_to_100_percentiles_equal_plain_mean():
    prices = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = calculate_winsorized_average(prices, lower_percentile=0.0, upper_percentile=100.0)
    assert result == pytest.approx(3.0)


def test_tight_percentiles_clip_aggressively():
    prices = [1.0, 5.0, 5.0, 5.0, 100.0]
    loose = calculate_winsorized_average(prices, lower_percentile=10.0, upper_percentile=90.0)
    tight = calculate_winsorized_average(prices, lower_percentile=25.0, upper_percentile=75.0)
    # Tighter bounds → outliers clipped harder → closer to the central value
    assert abs(tight - 5.0) <= abs(loose - 5.0)


# ── Boundary / edge cases ─────────────────────────────────────────────────────

def test_result_is_float():
    result = calculate_winsorized_average([3.0, 7.0, 5.0])
    assert isinstance(result, float)


def test_large_dataset_does_not_raise():
    prices = [float(i) for i in range(1, 1001)]
    result = calculate_winsorized_average(prices)
    assert result > 0


# ── Invalid input ─────────────────────────────────────────────────────────────

def test_raises_for_single_price():
    with pytest.raises(ValueError, match="At least 2 price entries are required"):
        calculate_winsorized_average([10.0])


def test_raises_for_empty_list():
    with pytest.raises(ValueError, match="At least 2 price entries are required"):
        calculate_winsorized_average([])


def test_raises_when_lower_equals_upper_percentile():
    with pytest.raises(ValueError, match="Percentile bounds must satisfy"):
        calculate_winsorized_average([1.0, 2.0, 3.0], lower_percentile=50.0, upper_percentile=50.0)


def test_raises_when_lower_exceeds_upper_percentile():
    with pytest.raises(ValueError, match="Percentile bounds must satisfy"):
        calculate_winsorized_average([1.0, 2.0, 3.0], lower_percentile=80.0, upper_percentile=20.0)


def test_raises_when_lower_percentile_is_negative():
    with pytest.raises(ValueError, match="Percentile bounds must satisfy"):
        calculate_winsorized_average([1.0, 2.0, 3.0], lower_percentile=-1.0, upper_percentile=90.0)


def test_raises_when_upper_percentile_exceeds_100():
    with pytest.raises(ValueError, match="Percentile bounds must satisfy"):
        calculate_winsorized_average([1.0, 2.0, 3.0], lower_percentile=10.0, upper_percentile=101.0)
