"""Toy photon-number-splitting sketch.

This module deliberately implements only a lightweight bookkeeping sketch for
multi-photon pulses.  A real PNS analysis requires source statistics, channel
loss, detector behavior, Eve's memory assumptions, basis disclosure timing, and
decoy-state countermeasures.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from quantum_bb84.utils.random import RandomLike, make_rng
from quantum_bb84.utils.validation import require_probability


@dataclass(slots=True)
class PhotonNumberSplittingSketch:
    """Summary of a toy PNS opportunity model."""

    multi_photon_mask: list[bool]
    eve_known_bits: list[int]
    known_fraction: float


def sketch_photon_number_splitting(
    alice_bits: Sequence[int],
    *,
    multi_photon_probability: float = 0.2,
    seed: Optional[int | RandomLike] = None,
) -> PhotonNumberSplittingSketch:
    """Mark pulses where a toy Eve could keep a copy after basis disclosure."""

    require_probability("multi_photon_probability", multi_photon_probability)
    bits = [int(bit) for bit in alice_bits]
    rng = make_rng(seed)
    mask = [rng.random() < multi_photon_probability for _ in bits]
    eve_known = [bit if selected else -1 for bit, selected in zip(bits, mask)]
    known_fraction = sum(mask) / len(mask) if mask else float("nan")
    return PhotonNumberSplittingSketch(mask, eve_known, known_fraction)
