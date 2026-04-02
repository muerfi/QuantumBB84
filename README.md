# QuantumBB84

An educational repository for studying quantum key distribution (QKD), centered on **BB84** and **E91** simulations in Python/Qiskit.

This project is best read as a learning notebook plus runnable prototypes. It includes:
- conceptual notes (physics, information theory, limits),
- small protocol simulations,
- attack sketches,
- and supporting plots/scripts.

It is **not** a production-grade security implementation.

## What this repository actually covers

- **BB84 simulations** with and without an eavesdropper, including key sifting and a simple error-rate check.
- **E91 simulation** of entangled-pair measurements with key extraction from matching bases.
- **Attack-oriented scripts** (PNS and beam-splitting style models) meant as exploratory code.
- **Documentation** on quantum mechanics background, protocol flow, and practical constraints.

## Repository map

- `Docs/`
  - `BB84_Protocol.md` — BB84 workflow and assumptions.
  - `Quantum_Physics.md` — physical principles used by QKD.
  - `Quantum_Info.md` — information-theoretic framing.
  - `Practical-limits.md` — engineering/security limits in real deployments.
  - `Philosophy.md` — non-technical reflections.
  - `Equations/` — report PDF + figure generation scripts.

- `Quantum_security/`
  - `BB84_Simulation.py` — BB84 simulation pipeline.
  - `BB84_No_Eve.py`, `BB84_With_Eve.py` — split variants.
  - `Noise_Analysis.py`, `Multirun-stats.py`, `Interactive-visualization.py` — analysis utilities.

- `Protocols/`
  - `BB84/BB84_Simulation.py` + `README.md`
  - `E91/E91_Simulation.py` + `README.md`
  - `README.md` — high-level BB84 vs E91 comparison.

- `Attacks/`
  - `PNS_Attack.py`, `BeamSplit-Attack.py`, `Attack_q-bits.py`
  - `README.md` — scope and caveats of attack scripts.

- `Experiments/`
  - `simulation.md` — legacy simulation notes and outputs.

- `Resources/`
  - `glossary.md` and `references.md`.

## Requirements

- Python 3.8+
- Qiskit + Aer
- NumPy
- Matplotlib
- Plotly (optional; only for interactive visuals)

Example install:

```bash
pip install qiskit qiskit-aer numpy matplotlib plotly
```

## Quick start

```bash
git clone https://github.com/muerfi/QuantumBB84.git
cd QuantumBB84
python Protocols/BB84/BB84_Simulation.py
python Protocols/E91/E91_Simulation.py
```

## Expected behavior (high level)

- In BB84, adding interception should generally increase observed check-bit errors.
- In E91, matching-basis outcomes should show strong correlations/anti-correlations depending on state/bit mapping.

Because these are finite-shot simulations with simplified modeling, outcomes vary across runs.

## Scope and limitations

- The code uses idealized assumptions and simplified post-processing.
- Some scripts are exploratory and not harmonized into one API.
- Security claims should be read as **protocol-level intuition**, not implementation-level proof.

If you want to build on this project, start by tightening the simulation assumptions and adding reproducible statistical tests.
