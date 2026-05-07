from math import isnan

import pytest

from quantum_bb84.analysis.qber import compute_qber
from quantum_bb84.protocols.bb84 import sift_key


def test_sift_key_keeps_only_matching_bases_and_splits_check_sample():
    alice_bits = [1, 0, 1, 1, 0]
    bob_bits = [1, 1, 1, 0, 0]
    alice_bases = [0, 0, 1, 1, 0]
    bob_bases = [0, 1, 1, 0, 0]

    alice_sifted, bob_sifted = sift_key(
        alice_bits,
        bob_bits,
        alice_bases,
        bob_bases,
        check_fraction=1 / 3,
    )

    assert alice_sifted.indices == [0, 2, 4]
    assert bob_sifted.indices == [0, 2, 4]
    assert alice_sifted.check == [1]
    assert bob_sifted.check == [1]
    assert alice_sifted.key == [1, 0]
    assert bob_sifted.key == [1, 0]


def test_sift_key_requires_equal_length_inputs():
    with pytest.raises(ValueError, match="same length"):
        sift_key([0, 1], [0], [0, 1], [0, 1])


def test_compute_qber_returns_zero_for_identical_keys():
    assert compute_qber([0, 1, 1, 0], [0, 1, 1, 0]) == 0.0


def test_compute_qber_returns_known_finite_error_rate():
    assert compute_qber([0, 1, 1, 0, 1], [1, 1, 0, 0, 1]) == 2 / 5


def test_compute_qber_empty_sample_is_nan():
    assert isnan(compute_qber([], []))
