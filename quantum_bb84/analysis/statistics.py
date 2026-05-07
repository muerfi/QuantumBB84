"""Finite-shot statistical summaries for simulation outputs."""

from __future__ import annotations

from math import sqrt


def normal_approximation_interval(proportion: float, shots: int, z: float = 1.96) -> tuple[float, float]:
    """Return a simple clipped normal approximation interval for a proportion.

    This helper is intentionally modest: it summarizes finite-shot uncertainty
    for educational plots and CLI output, and should not be read as a security
    statement.
    """

    if shots <= 0:
        return (float("nan"), float("nan"))
    if not 0.0 <= proportion <= 1.0:
        return (float("nan"), float("nan"))
    half_width = z * sqrt(proportion * (1.0 - proportion) / shots)
    return (max(0.0, proportion - half_width), min(1.0, proportion + half_width))
