from quantum_bb84.utils.random import generate_random_bases, generate_random_bits


def test_generate_random_bits_is_seed_reproducible_and_binary():
    bits = generate_random_bits(64, seed=1234)

    assert bits == generate_random_bits(64, seed=1234)
    assert set(bits) <= {0, 1}
    assert len(bits) == 64


def test_generate_random_bits_different_seeds_can_differ():
    assert generate_random_bits(64, seed=1) != generate_random_bits(64, seed=2)


def test_generate_random_bases_is_seed_reproducible_and_in_range():
    bases = generate_random_bases(64, seed=1234, basis_count=3)

    assert bases == generate_random_bases(64, seed=1234, basis_count=3)
    assert set(bases) <= {0, 1, 2}
    assert len(bases) == 64


def test_generate_random_bases_different_seeds_can_differ():
    assert generate_random_bases(64, seed=1) != generate_random_bases(64, seed=2)
