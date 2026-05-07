"""Validation helpers shared by simulations and the CLI."""

from __future__ import annotations


def require_non_negative_int(name: str, value: int) -> None:
    """Validate a count-like argument."""

    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def require_probability(name: str, value: float) -> None:
    """Validate a probability in the closed interval [0, 1]."""

    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


def require_fraction(name: str, value: float) -> None:
    """Validate a fraction in the half-open interval [0, 1)."""

    if not 0.0 <= value < 1.0:
        raise ValueError(f"{name} must be at least 0 and less than 1")
