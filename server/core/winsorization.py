from typing import List

from server.utils.logger import get_logger

_logger = get_logger(__name__)

DEFAULT_LOWER_PERCENTILE = 10.0
DEFAULT_UPPER_PERCENTILE = 90.0
MINIMUM_PRICE_COUNT = 2


def calculate_winsorized_average(
    prices: List[float],
    lower_percentile: float = DEFAULT_LOWER_PERCENTILE,
    upper_percentile: float = DEFAULT_UPPER_PERCENTILE,
) -> float:
    """
    Compute a winsorized mean from crowdsourced price data.

    Outliers beyond the given percentile bounds are clipped to the
    boundary values before averaging, making the result resilient to
    data-entry errors and price manipulation.

    Pure logic — no database or HTTP dependencies.
    """
    if len(prices) < MINIMUM_PRICE_COUNT:
        raise ValueError(
            f"At least {MINIMUM_PRICE_COUNT} price entries are required, "
            f"received {len(prices)}."
        )
    if not (0.0 <= lower_percentile < upper_percentile <= 100.0):
        raise ValueError(
            "Percentile bounds must satisfy 0 <= lower < upper <= 100. "
            f"Received lower={lower_percentile}, upper={upper_percentile}."
        )

    try:
        lower_bound = _calculate_percentile(prices, lower_percentile)
        upper_bound = _calculate_percentile(prices, upper_percentile)
        clipped_prices = _clip_prices(prices, lower_bound, upper_bound)
        result = sum(clipped_prices) / len(clipped_prices)

        _logger.debug(
            "Winsorized average: %.2f (n=%d, bounds=[%.2f, %.2f])",
            result,
            len(prices),
            lower_bound,
            upper_bound,
        )
        return result

    except Exception as exc:
        _logger.error("Failed to calculate winsorized average: %s", exc)
        raise


def _calculate_percentile(prices: List[float], percentile: float) -> float:
    """Return the value at the given percentile using linear interpolation."""
    sorted_prices = sorted(prices)
    index = (percentile / 100.0) * (len(sorted_prices) - 1)
    lower_index = int(index)
    upper_index = lower_index + 1
    fraction = index - lower_index

    if upper_index >= len(sorted_prices):
        return sorted_prices[lower_index]

    return sorted_prices[lower_index] + fraction * (
        sorted_prices[upper_index] - sorted_prices[lower_index]
    )


def _clip_prices(
    prices: List[float], lower_bound: float, upper_bound: float
) -> List[float]:
    """Clip each price to the [lower_bound, upper_bound] interval."""
    return [max(lower_bound, min(upper_bound, price)) for price in prices]
