"""Toy intercept-resend attack for BB84 simulations.

The model is intentionally simple: Eve independently chooses whether to
intercept each signal, measures in a random BB84 basis, and resends the state
matching her outcome and basis.  It illustrates disturbance from incompatible
measurements but is not a complete adversarial security model.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from quantum_bb84.utils.random import RandomLike, generate_random_bases, generate_random_bits, make_rng
from quantum_bb84.utils.validation import require_probability


@dataclass(slots=True)
class InterceptResendResult:
    """Signals after a toy intercept-resend operation."""

    resent_bits: list[int]
    resent_bases: list[int]
    eve_bits: list[int]
    eve_bases: list[int]
    intercepted: list[bool]


def apply_intercept_resend(
    alice_bits: Sequence[int],
    alice_bases: Sequence[int],
    *,
    intercept_rate: float = 1.0,
    seed: Optional[int | RandomLike] = None,
) -> InterceptResendResult:
    """Apply a finite-shot toy intercept-resend attack.

    When Eve chooses the same basis as Alice, this idealized model gives her the
    correct bit and resends an equivalent BB84 state.  With a mismatched basis,
    her result is random and she resends in the wrong basis, creating possible
    downstream errors when Alice and Bob later sift.
    """

    require_probability("intercept_rate", intercept_rate)
    bits = [int(bit) for bit in alice_bits]
    bases = [int(base) for base in alice_bases]
    if len(bits) != len(bases):
        raise ValueError("alice_bits and alice_bases must have the same length")

    rng = make_rng(seed)
    n = len(bits)
    intercepted = [rng.random() < intercept_rate for _ in range(n)]
    eve_bases = generate_random_bases(n, rng, basis_count=2)
    random_outcomes = generate_random_bits(n, rng)
    eve_bits = [bits[i] if intercepted[i] and eve_bases[i] == bases[i] else random_outcomes[i] for i in range(n)]
    resent_bits = bits.copy()
    resent_bases = bases.copy()
    for i, was_intercepted in enumerate(intercepted):
        if was_intercepted:
            resent_bits[i] = eve_bits[i]
            resent_bases[i] = eve_bases[i]
    return InterceptResendResult(resent_bits, resent_bases, eve_bits, eve_bases, intercepted)
