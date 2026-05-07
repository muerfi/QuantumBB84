"""Idealized finite-shot BB84 simulation.

The implementation models BB84 at the level of classical preparation choices,
basis-dependent measurements, optional bit-flip channel noise, and optional toy
intercept-resend disturbance.  It is useful for protocol intuition and finite-
shot demonstrations.  It is not production cryptography and does not establish
real-world QKD security.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import floor, isfinite
from typing import Optional

from quantum_bb84.analysis.qber import compute_qber
from quantum_bb84.attacks.intercept_resend import InterceptResendResult, apply_intercept_resend
from quantum_bb84.simulation.noise import apply_noise
from quantum_bb84.utils.random import generate_random_bases, generate_random_bits, make_rng
from quantum_bb84.utils.validation import require_fraction, require_non_negative_int, require_probability


@dataclass(slots=True)
class SiftedKey:
    """Key material retained after Alice and Bob announce bases.

    ``key`` is the untested candidate key kept for later demonstrations;
    ``check`` is the public comparison sample used to estimate QBER in this toy
    simulation.
    """

    key: list[int]
    check: list[int]
    indices: list[int]


@dataclass(slots=True)
class BB84SimulationResult:
    """Structured result for one finite-shot BB84 simulation."""

    protocol: str
    qubits: int
    seed: Optional[int]
    alice_bits: list[int]
    alice_bases: list[int]
    bob_bases: list[int]
    bob_bits: list[int]
    sifted_indices: list[int]
    alice_key: list[int]
    bob_key: list[int]
    alice_check: list[int]
    bob_check: list[int]
    qber: float
    noise_probability: float
    eve: Optional[str]
    eve_rate: float
    eve_bits: Optional[list[int]]
    accepted: bool
    threshold: float
    notes: tuple[str, ...]

    def summary(self) -> dict[str, object]:
        """Return a JSON-friendly summary without exposing full bit arrays."""

        return {
            "protocol": self.protocol,
            "qubits": self.qubits,
            "seed": self.seed,
            "sifted_bits": len(self.sifted_indices),
            "candidate_key_bits": len(self.alice_key),
            "check_bits": len(self.alice_check),
            "qber": self.qber,
            "noise_probability": self.noise_probability,
            "eve": self.eve,
            "eve_rate": self.eve_rate,
            "accepted_under_toy_threshold": self.accepted,
            "threshold": self.threshold,
            "notes": list(self.notes),
        }


def sift_key(
    alice_bits: Sequence[int],
    bob_bits: Sequence[int],
    alice_bases: Sequence[int],
    bob_bases: Sequence[int],
    *,
    check_fraction: float = 0.25,
) -> tuple[SiftedKey, SiftedKey]:
    """Sift Alice and Bob keys by retaining positions with matching bases.

    The first ``check_fraction`` of matching positions is reserved for public
    comparison and QBER estimation.  The remaining positions are candidate key
    material for the simulation output.
    """

    require_fraction("check_fraction", check_fraction)
    arrays = [list(map(int, values)) for values in (alice_bits, bob_bits, alice_bases, bob_bases)]
    if len({len(values) for values in arrays}) != 1:
        raise ValueError("bit and basis arrays must have the same length")
    a_bits, b_bits, a_bases, b_bases = arrays
    matching = [i for i, (a_base, b_base) in enumerate(zip(a_bases, b_bases)) if a_base == b_base]
    check_count = floor(len(matching) * check_fraction)
    check_indices = matching[:check_count]
    key_indices = matching[check_count:]
    return (
        SiftedKey(key=[a_bits[i] for i in key_indices], check=[a_bits[i] for i in check_indices], indices=matching),
        SiftedKey(key=[b_bits[i] for i in key_indices], check=[b_bits[i] for i in check_indices], indices=matching),
    )


def simulate_bb84(
    qubits: int = 1000,
    *,
    seed: Optional[int] = None,
    eve: Optional[str] = None,
    eve_rate: float = 0.0,
    noise_probability: float = 0.0,
    check_fraction: float = 0.25,
    threshold: float = 0.11,
) -> BB84SimulationResult:
    """Run one idealized BB84 finite-shot simulation.

    Parameters describe a pedagogical prepare-and-measure model.  If
    ``eve='intercept_resend'``, Eve measures a random subset of signals in
    random BB84 bases and resends the state she inferred.  The resulting QBER is
    a finite-sample disturbance statistic, not a security proof.
    """

    require_non_negative_int("qubits", qubits)
    require_probability("eve_rate", eve_rate)
    require_probability("noise_probability", noise_probability)
    require_fraction("check_fraction", check_fraction)
    require_probability("threshold", threshold)
    if eve not in (None, "intercept_resend"):
        raise ValueError("eve must be None or 'intercept_resend'")

    rng = make_rng(seed)
    alice_bits = generate_random_bits(qubits, rng)
    alice_bases = generate_random_bases(qubits, rng, basis_count=2)
    transmitted_bits = alice_bits.copy()
    transmitted_bases = alice_bases.copy()
    eve_bits = None

    if eve == "intercept_resend":
        attack: InterceptResendResult = apply_intercept_resend(
            alice_bits,
            alice_bases,
            intercept_rate=eve_rate,
            seed=rng,
        )
        transmitted_bits = attack.resent_bits
        transmitted_bases = attack.resent_bases
        eve_bits = attack.eve_bits

    bob_bases = generate_random_bases(qubits, rng, basis_count=2)
    random_measurements = generate_random_bits(qubits, rng)
    bob_bits = [transmitted_bits[i] if bob_bases[i] == transmitted_bases[i] else random_measurements[i] for i in range(qubits)]
    bob_bits = apply_noise(bob_bits, noise_probability=noise_probability, seed=rng)

    alice_sifted, bob_sifted = sift_key(
        alice_bits,
        bob_bits,
        alice_bases,
        bob_bases,
        check_fraction=check_fraction,
    )
    qber = compute_qber(alice_sifted.check, bob_sifted.check)
    accepted = bool(isfinite(qber) and qber <= threshold)
    notes = (
        "Idealized finite-shot BB84 simulation; not production cryptography.",
        "Acceptance is only a toy threshold decision for this simulated sample.",
    )
    return BB84SimulationResult(
        protocol="BB84",
        qubits=qubits,
        seed=seed,
        alice_bits=alice_bits,
        alice_bases=alice_bases,
        bob_bases=bob_bases,
        bob_bits=bob_bits,
        sifted_indices=alice_sifted.indices,
        alice_key=alice_sifted.key,
        bob_key=bob_sifted.key,
        alice_check=alice_sifted.check,
        bob_check=bob_sifted.check,
        qber=qber,
        noise_probability=noise_probability,
        eve=eve,
        eve_rate=eve_rate,
        eve_bits=eve_bits,
        accepted=accepted,
        threshold=threshold,
        notes=notes,
    )
