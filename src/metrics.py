"""Simulation metrics utilities."""

from __future__ import annotations

from typing import Dict, Iterable, Sequence


def overshoot_depth(series: Sequence[float], limit: float) -> float:
    """Return the maximum depth below ``limit`` encountered in ``series``."""
    if not series:
        return 0.0
    return max(0.0, max(limit - value for value in series))


def inequality_index(values: Sequence[float]) -> float:
    """Calculate a simple Gini coefficient for ``values``."""
    n = len(values)
    if n == 0:
        return 0.0
    sorted_vals = sorted(values)
    cumulative = 0.0
    for i, v in enumerate(sorted_vals, start=1):
        cumulative += v * (2 * i - n - 1)
    mean = sum(sorted_vals) / n
    if mean == 0:
        return 0.0
    return cumulative / (n**2 * mean)


def welfare_indices(values: Sequence[float]) -> Dict[str, float]:
    """Return utilitarian, average and Rawlsian welfare indices."""
    if not values:
        return {"utilitarian": 0.0, "average": 0.0, "rawlsian": 0.0}
    utilitarian = sum(values)
    average = utilitarian / len(values)
    rawlsian = min(values)
    return {
        "utilitarian": utilitarian,
        "average": average,
        "rawlsian": rawlsian,
    }


def return_time_to_boundaries(
    series: Sequence[float], lower: float, upper: float
) -> int:
    """Return time steps to return within ``[lower, upper]`` after leaving."""
    def inside(value: float) -> bool:
        return lower <= value <= upper

    crossed = False
    steps = 0
    for value in series:
        if not crossed:
            if not inside(value):
                crossed = True
                steps = 0
        else:
            steps += 1
            if inside(value):
                return steps
    return steps if crossed else 0
