"""Simulation dispatch helpers used by the command-line interface."""

from __future__ import annotations

from typing import Any


def run_simulation(protocol: str, **kwargs: Any):
    """Dispatch a named protocol simulation."""

    normalized = protocol.lower()
    if normalized == "bb84":
        from quantum_bb84.protocols.bb84 import simulate_bb84

        return simulate_bb84(**kwargs)
    if normalized == "e91":
        from quantum_bb84.protocols.e91 import simulate_e91

        return simulate_e91(**kwargs)
    raise ValueError(f"unknown protocol: {protocol}")
