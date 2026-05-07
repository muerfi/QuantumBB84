"""Toy beam-splitting bookkeeping sketch.

The function here estimates which simulated pulses Eve samples.  It is not an
optical channel model and should not be presented as an implementation attack
analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from quantum_bb84.utils.random import RandomLike, make_rng
from quantum_bb84.utils.validation import require_probability


@dataclass(slots=True)
class BeamSplittingSketch:
    """Summary of a toy beam-splitting sampling model."""

    sampled_mask: list[bool]
    sampled_fraction: float


def sketch_beam_splitting(
    signal_count: int,
    *,
    split_fraction: float = 0.3,
    seed: Optional[int | RandomLike] = None,
) -> BeamSplittingSketch:
    """Sample signals diverted to Eve in a simplified beam-splitting sketch."""

    if signal_count < 0:
        raise ValueError("signal_count must be non-negative")
    require_probability("split_fraction", split_fraction)
    rng = make_rng(seed)
    mask = [rng.random() < split_fraction for _ in range(signal_count)]
    sampled_fraction = sum(mask) / signal_count if signal_count else float("nan")
    return BeamSplittingSketch(mask, sampled_fraction)
