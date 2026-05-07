"""Quantum Key Distribution Simulation Lab.

``quantum_bb84`` provides reproducible educational simulations of BB84 and a
simplified E91-style protocol, together with toy attack and noise models.  The
package is designed for protocol intuition and finite-shot experiments; it is
not production-grade cryptography and does not prove real-world QKD security.
"""

from quantum_bb84.analysis.qber import compute_qber
from quantum_bb84.attacks.intercept_resend import apply_intercept_resend
from quantum_bb84.protocols.bb84 import sift_key, simulate_bb84
from quantum_bb84.protocols.e91 import simulate_e91
from quantum_bb84.simulation.noise import apply_noise
from quantum_bb84.utils.random import generate_random_bases, generate_random_bits

__all__ = [
    "apply_intercept_resend",
    "apply_noise",
    "compute_qber",
    "generate_random_bases",
    "generate_random_bits",
    "sift_key",
    "simulate_bb84",
    "simulate_e91",
]

__version__ = "0.1.0"
