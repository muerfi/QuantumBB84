"""Simplified E91-style entanglement simulation.

This module demonstrates entangled-pair intuition and basis reconciliation.  It
is not a full E91 implementation: it does not perform a rigorous CHSH security
analysis, detector-efficiency treatment, or finite-key proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, isfinite
from typing import Optional

from quantum_bb84.analysis.qber import compute_qber
from quantum_bb84.simulation.noise import apply_noise
from quantum_bb84.utils.random import generate_random_bases, generate_random_bits, make_rng
from quantum_bb84.utils.validation import require_fraction, require_non_negative_int, require_probability


@dataclass(slots=True)
class E91SimulationResult:
    """Structured result for a simplified finite-shot E91-style run."""

    protocol: str
    pairs: int
    seed: Optional[int]
    alice_bases: list[int]
    bob_bases: list[int]
    alice_bits: list[int]
    bob_bits: list[int]
    sifted_indices: list[int]
    alice_key: list[int]
    bob_key: list[int]
    alice_check: list[int]
    bob_check: list[int]
    qber: float
    noise_probability: float
    accepted: bool
    threshold: float
    notes: tuple[str, ...]

    def summary(self) -> dict[str, object]:
        """Return a JSON-friendly summary without full bit arrays."""

        return {
            "protocol": self.protocol,
            "pairs": self.pairs,
            "seed": self.seed,
            "sifted_bits": len(self.sifted_indices),
            "candidate_key_bits": len(self.alice_key),
            "check_bits": len(self.alice_check),
            "qber": self.qber,
            "noise_probability": self.noise_probability,
            "accepted_under_toy_threshold": self.accepted,
            "threshold": self.threshold,
            "notes": list(self.notes),
        }


def simulate_e91(
    pairs: int = 1000,
    *,
    seed: Optional[int] = None,
    noise_probability: float = 0.0,
    check_fraction: float = 0.25,
    threshold: float = 0.11,
) -> E91SimulationResult:
    """Run a simplified finite-shot E91-style simulation.

    Matching settings are modeled as perfectly correlated Bell-pair outcomes
    before optional bit-flip noise.  Nonmatching settings are sampled as random
    outcomes and are discarded during key sifting.  The output is suitable for
    protocol intuition only and should not be described as real E91 security.
    """

    require_non_negative_int("pairs", pairs)
    require_probability("noise_probability", noise_probability)
    require_fraction("check_fraction", check_fraction)
    require_probability("threshold", threshold)

    rng = make_rng(seed)
    alice_bases = generate_random_bases(pairs, rng, basis_count=3)
    bob_bases = generate_random_bases(pairs, rng, basis_count=3)
    alice_bits = generate_random_bits(pairs, rng)
    bob_random = generate_random_bits(pairs, rng)
    bob_bits = [alice_bits[i] if alice_bases[i] == bob_bases[i] else bob_random[i] for i in range(pairs)]
    bob_bits = apply_noise(bob_bits, noise_probability=noise_probability, seed=rng)

    matching = [i for i, (a_base, b_base) in enumerate(zip(alice_bases, bob_bases)) if a_base == b_base]
    check_count = floor(len(matching) * check_fraction)
    check_indices = matching[:check_count]
    key_indices = matching[check_count:]
    alice_check = [alice_bits[i] for i in check_indices]
    bob_check = [bob_bits[i] for i in check_indices]
    qber = compute_qber(alice_check, bob_check)
    accepted = bool(isfinite(qber) and qber <= threshold)
    notes = (
        "Simplified E91-style entanglement and sifting demonstration.",
        "No CHSH/Bell-test security workflow or finite-key proof is implemented.",
    )
    return E91SimulationResult(
        protocol="E91-simplified",
        pairs=pairs,
        seed=seed,
        alice_bases=alice_bases,
        bob_bases=bob_bases,
        alice_bits=alice_bits,
        bob_bits=bob_bits,
        sifted_indices=matching,
        alice_key=[alice_bits[i] for i in key_indices],
        bob_key=[bob_bits[i] for i in key_indices],
        alice_check=alice_check,
        bob_check=bob_check,
        qber=qber,
        noise_probability=noise_probability,
        accepted=accepted,
        threshold=threshold,
        notes=notes,
    )
