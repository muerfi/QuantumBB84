"""Toy attack models and sketches."""

from quantum_bb84.attacks.beam_splitting import sketch_beam_splitting
from quantum_bb84.attacks.intercept_resend import apply_intercept_resend
from quantum_bb84.attacks.photon_number_splitting import sketch_photon_number_splitting

__all__ = ["apply_intercept_resend", "sketch_beam_splitting", "sketch_photon_number_splitting"]
