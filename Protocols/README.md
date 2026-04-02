# BB84 vs E91 (Project-Level Comparison)

This document compares the two protocol implementations in this repository.

## Shared goal

Both protocols aim to let Alice and Bob establish a shared secret key while detecting eavesdropping through quantum effects.

## BB84 in this repo

- Uses single-qubit state preparation in two bases (Z/X).
- Security signal comes from disturbance introduced by incompatible measurements.
- Implementation includes optional interception and a simple error-threshold decision rule.

## E91 in this repo

- Uses entangled qubit pairs and random basis choices.
- Implementation focuses on key extraction from matching bases and error-rate reporting.
- The current script does **not** implement a full CHSH/Bell-inequality workflow.

## Practical differences

| Aspect | BB84 implementation | E91 implementation |
|---|---|---|
| Quantum resource | Prepared single qubits | Entangled pairs |
| Eavesdropper modeling | Included in script (intercept probability) | Not explicitly modeled |
| Bell/CHSH test | Not applicable | Not currently implemented |
| Complexity | Lower | Higher |

## Important caveat

This repository demonstrates protocol ideas, not a complete secure communications stack. Real QKD systems require careful device modeling, calibration, authenticated classical channels, and stronger post-processing.

## Run the examples

```bash
python Protocols/BB84/BB84_Simulation.py
python Protocols/E91/E91_Simulation.py
```
