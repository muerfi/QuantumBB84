import numpy as np

def generate_random_bits(size):
    """Generates an array of random bits."""
    return np.random.randint(2, size=size)

def compare_bases(bases1, bases2):
    """Returns the indices where the bases match."""
    return np.where(bases1 == bases2)[0]

def extract_key(bits, indices, n):
    """Extracts the key and the check bits from the matching indices."""
    selected_bits = bits[indices]
    key = selected_bits[:n]
    check = selected_bits[n:2*n]
    return key, check
