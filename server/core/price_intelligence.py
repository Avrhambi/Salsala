from typing import List

from server.utils.logger import get_logger
from shared.types import TrendValue

_logger = get_logger(__name__)

TREND_THRESHOLD_PERCENT = 5.0
MINIMUM_HISTORICAL_PRICES = 1


def calculate_price_trend(
    current_price: float, historical_prices: List[float]
) -> TrendValue:
    """
    Determine the price trend for an item by comparing its current price
    against the historical average.

    Returns TrendValue.NA when there is insufficient data to make a
    reliable determination.

    Pure logic — no database or HTTP dependencies.
    """
    if current_price <= 0:
        raise ValueError(
            f"current_price must be greater than 0, received {current_price}."
        )
    if len(historical_prices) < MINIMUM_HISTORICAL_PRICES:
        _logger.warning(
            "No historical prices provided; cannot determine trend."
        )
        return TrendValue.NA

    try:
        historical_avg = _calculate_average(historical_prices)
        percent_change = _calculate_percent_change(current_price, historical_avg)
        trend = _classify_trend(percent_change)

        _logger.debug(
            "Price trend calculated: current=%.2f avg=%.2f change=%.2f%% trend=%s",
            current_price,
            historical_avg,
            percent_change,
            trend.value,
        )
        return trend

    except Exception as exc:
        _logger.error("Failed to calculate price trend: %s", exc)
        raise


def _calculate_average(prices: List[float]) -> float:
    """Return the arithmetic mean of a non-empty list of prices."""
    if not prices:
        raise ValueError("Cannot compute average of an empty list.")
    return sum(prices) / len(prices)


def _calculate_percent_change(current: float, reference: float) -> float:
    """Return percentage change from reference to current value."""
    if reference == 0:
        raise ValueError("Reference price cannot be zero when computing percent change.")
    return ((current - reference) / reference) * 100.0


def _classify_trend(percent_change: float) -> TrendValue:
    """Map a percentage change value to a TrendValue enum member."""
    if percent_change > TREND_THRESHOLD_PERCENT:
        return TrendValue.UP
    if percent_change < -TREND_THRESHOLD_PERCENT:
        return TrendValue.DOWN
    return TrendValue.STABLE
