# Simplified E91 Protocol Notes

## Recommended run command

Use the refactored package CLI for reproducible runs:

```bash
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

The older `E91_Simulation.py` script is retained as historical educational material and may depend on legacy Qiskit/Aer behavior.

## What the current model demonstrates

The package-level E91 simulation models entangled-pair intuition, random basis choices, matching-setting correlations, basis reconciliation, key sifting, and QBER estimation.

## What it does not include

- Explicit eavesdropper strategies.
- CHSH/Bell-test statistics.
- E91 security acceptance criteria.
- Finite-key analysis.
- Detector-efficiency or loophole modeling.
- Error correction, privacy amplification, or authentication.

This should be read as a compact entanglement-and-sifting demonstration, not as a full E91 security-proof implementation.
