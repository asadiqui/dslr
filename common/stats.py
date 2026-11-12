"""Hand-written descriptive statistics used by the DSLR analysis scripts."""

import math
from typing import Dict, List


def _require_values(data: List[float]) -> None:
    if not data:
        raise ValueError("cannot calculate statistics for an empty feature")


def mean(data: List[float]) -> float:
    _require_values(data)
    total = 0.0
    for value in data:
        total += value
    return total / len(data)


def variance(data: List[float], sample: bool = True) -> float:
    _require_values(data)
    if sample and len(data) < 2:
        return 0.0
    center = mean(data)
    squared = 0.0
    for value in data:
        difference = value - center
        squared += difference * difference
    denominator = len(data) - 1 if sample else len(data)
    return squared / denominator


def standard_deviation(data: List[float]) -> float:
    return math.sqrt(variance(data))


def quantile(data: List[float], probability: float) -> float:
    """Calculate a linearly interpolated quantile without a helper library."""
    _require_values(data)
    if probability < 0.0 or probability > 1.0:
        raise ValueError("probability must be between 0 and 1")
    ordered = sorted(data)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = lower + 1
    if upper >= len(ordered):
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def describe(data: List[float]) -> Dict[str, float]:
    """Return the mandatory describe rows plus useful bonus fields."""
    _require_values(data)
    first = data[0]
    smallest = first
    largest = first
    for value in data[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value
    lower_quartile = quantile(data, 0.25)
    upper_quartile = quantile(data, 0.75)
    return {
        "Count": float(len(data)),
        "Mean": mean(data),
        "Std": standard_deviation(data),
        "Min": smallest,
        "25%": lower_quartile,
        "50%": quantile(data, 0.50),
        "75%": upper_quartile,
        "Max": largest,
        "Variance": variance(data),
        "IQR": upper_quartile - lower_quartile,
    }
