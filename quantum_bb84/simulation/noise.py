"""Simple channel-noise models for finite-shot simulations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional

from quantum_bb84.utils.random import RandomLike, make_rng
from quantum_bb84.utils.validation import require_probability


def apply_noise(
    bits: Sequence[int],
    *,
    noise_probability: float = 0.0,
    seed: Optional[int | RandomLike] = None,
) -> list[int]:
    """Apply independent classical bit-flip noise to measured bits.

    This is a toy channel/readout noise model for exploring how QBER changes
    under finite sampling.  It does not represent a calibrated optical channel
    or detector model.
    """

    require_probability("noise_probability", noise_probability)
    clean_bits = [int(bit) for bit in bits]
    if not clean_bits or noise_probability == 0.0:
        return clean_bits
    rng = make_rng(seed)
    return [bit ^ int(rng.random() < noise_probability) for bit in clean_bits]
