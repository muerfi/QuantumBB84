from math import isfinite

from quantum_bb84.protocols.bb84 import simulate_bb84
from quantum_bb84.protocols.e91 import simulate_e91


def test_bb84_simulation_is_seed_reproducible_without_eve_or_noise():
    first = simulate_bb84(qubits=256, seed=42, check_fraction=0.5)
    second = simulate_bb84(qubits=256, seed=42, check_fraction=0.5)

    assert first == second
    assert first.qber == 0.0
    assert first.accepted is True
    assert first.summary()["protocol"] == "BB84"


def test_bb84_simulation_different_seeds_are_allowed_to_differ():
    first = simulate_bb84(qubits=256, seed=1, check_fraction=0.5)
    second = simulate_bb84(qubits=256, seed=2, check_fraction=0.5)

    assert first.alice_bits != second.alice_bits or first.bob_bases != second.bob_bases


def test_bb84_intercept_resend_exposes_finite_shot_disturbance_metrics():
    result = simulate_bb84(
        qubits=1000,
        seed=42,
        eve="intercept_resend",
        eve_rate=1.0,
        check_fraction=0.5,
    )

    assert result.eve == "intercept_resend"
    assert result.eve_rate == 1.0
    assert result.eve_bits is not None
    assert len(result.eve_bits) == result.qubits
    assert isfinite(result.qber)
    assert result.qber > 0.0
    assert result.summary()["qber"] == result.qber


def test_bb84_with_noise_changes_observed_qber_for_known_seed():
    result = simulate_bb84(qubits=256, seed=42, noise_probability=1.0, check_fraction=0.5)

    assert result.qber == 1.0
    assert result.accepted is False


def test_e91_simulation_basic_sanity_and_seed_reproducibility():
    first = simulate_e91(pairs=300, seed=42, check_fraction=0.5)
    second = simulate_e91(pairs=300, seed=42, check_fraction=0.5)

    assert first == second
    assert first.protocol == "E91-simplified"
    assert first.pairs == 300
    assert len(first.sifted_indices) > 0
    assert len(first.alice_check) > 0
    assert first.qber == 0.0
    assert first.accepted is True
    assert first.summary()["protocol"] == "E91-simplified"
