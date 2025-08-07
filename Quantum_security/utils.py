"""Utility functions used across BB84 simulations.

The helpers defined here centralise common operations such as random bit
generation and key extraction.  They are intentionally lightweight so they
can be reused by the different scripts in the repository without creating
additional dependencies.
"""

from __future__ import annotations

import secrets
from typing import Dict

import numpy as np


def generate_random_bits(size: int) -> np.ndarray:
    """Return ``size`` cryptographically secure random bits.

    The previous implementation relied on :mod:`numpy.random` which is not
    suitable for cryptographic purposes.  Using :mod:`secrets` provides
    randomness backed by the operating system's CSPRNG.
    """

    return np.array([secrets.randbits(1) for _ in range(size)], dtype=int)


def compare_bases(bases1: np.ndarray, bases2: np.ndarray) -> np.ndarray:
    """Return the indices where the two basis selections match."""

    return np.where(bases1 == bases2)[0]


def extract_key(bits: np.ndarray, indices: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Extract a key and corresponding check bits from ``bits``.

    Parameters
    ----------
    bits:
        The bit array from which to extract the key.
    indices:
        Indices of the bits that Alice and Bob agree upon.
    n:
        Desired length of the final key.  An additional ``n`` bits are used as
        check bits.
    """

    selected_bits = bits[indices]
    key = selected_bits[:n]
    check = selected_bits[n : 2 * n]
    return key, check


def sample_counts(counts: Dict[str, int]) -> str:
    """Randomly sample a bitstring from a Qiskit ``counts`` dictionary.

    ``counts`` maps bitstrings to the number of times they were observed during
    execution.  This helper draws one bitstring proportionally to these
    frequencies using :mod:`secrets` to avoid bias.
    """

    total = sum(counts.values())
    choice = secrets.randbelow(total)
    cumulative = 0
    for bitstring, count in counts.items():
        cumulative += count
        if choice < cumulative:
            return bitstring

    # Fallback in case of an empty dictionary, though this should not happen
    return ""

