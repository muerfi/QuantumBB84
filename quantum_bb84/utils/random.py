"""Reproducible random-number helpers for QKD simulations.

The laboratory uses pseudorandom generators by default so finite-shot examples
can be reproduced exactly from a seed.  This is appropriate for simulation and
teaching, but it is not a source of cryptographic randomness for deployed QKD.
"""

from __future__ import annotations

import random
from typing import Optional

RandomLike = random.Random


def make_rng(seed: Optional[int | RandomLike] = None) -> RandomLike:
    """Return a Python random generator for deterministic simulations."""

    if isinstance(seed, random.Random):
        return seed
    return random.Random(seed)


def generate_random_bits(size: int, seed: Optional[int | RandomLike] = None) -> list[int]:
    """Generate reproducible random bits for a simulation run.

    The returned bits model Alice's classical choices or measurement outcomes
    in an idealized finite-shot experiment.  They are not intended to be secret
    production keys.
    """

    if size < 0:
        raise ValueError("size must be non-negative")
    rng = make_rng(seed)
    return [rng.randrange(2) for _ in range(size)]


def generate_random_bases(
    size: int,
    seed: Optional[int | RandomLike] = None,
    *,
    basis_count: int = 2,
) -> list[int]:
    """Generate reproducible basis labels.

    For BB84, ``basis_count=2`` conventionally labels the rectilinear/Z basis
    as 0 and diagonal/X basis as 1.  The simplified E91 demonstration uses
    three labels to distinguish candidate measurement settings.
    """

    if size < 0:
        raise ValueError("size must be non-negative")
    if basis_count < 2:
        raise ValueError("basis_count must be at least 2")
    rng = make_rng(seed)
    return [rng.randrange(basis_count) for _ in range(size)]
