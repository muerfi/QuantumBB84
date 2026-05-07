"""Quantum bit error-rate utilities."""

from __future__ import annotations

from collections.abc import Sequence


def compute_qber(alice_bits: Sequence[int], bob_bits: Sequence[int]) -> float:
    """Compute the observed quantum bit error rate for paired check bits.

    QBER is the finite-sample fraction of compared bits that disagree.  In this
    project it is a simulation statistic, not a proof of security.  Empty input
    returns ``nan`` because no error rate was observed.
    """

    if len(alice_bits) != len(bob_bits):
        raise ValueError("alice_bits and bob_bits must have the same length")
    if not alice_bits:
        return float("nan")
    mismatches = sum(int(a != b) for a, b in zip(alice_bits, bob_bits))
    return mismatches / len(alice_bits)
