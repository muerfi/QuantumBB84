from quantum_bb84.simulation.noise import apply_noise


def test_noise_probability_zero_preserves_bits():
    bits = [0, 1, 1, 0, 1]

    assert apply_noise(bits, noise_probability=0.0, seed=123) == bits


def test_noise_probability_one_flips_every_bit_in_bit_flip_model():
    assert apply_noise([0, 1, 1, 0], noise_probability=1.0, seed=123) == [1, 0, 0, 1]


def test_noise_is_seed_reproducible_for_intermediate_probability():
    assert apply_noise([0] * 32, noise_probability=0.25, seed=99) == apply_noise(
        [0] * 32,
        noise_probability=0.25,
        seed=99,
    )
