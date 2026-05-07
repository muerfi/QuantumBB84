"""Small key-rate utilities for idealized simulations."""

from __future__ import annotations


def sifted_fraction(sifted_bits: int, transmitted_signals: int) -> float:
    """Return the fraction of transmitted signals retained after basis sifting."""

    if transmitted_signals <= 0:
        return float("nan")
    return float(sifted_bits / transmitted_signals)
