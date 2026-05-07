# Protocol Notes: BB84 and Simplified E91

This directory contains legacy protocol notes and scripts. For reproducible command-line simulations, prefer the refactored package interface:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

## Shared goal

BB84 and E91-style protocols are studied because they show how quantum measurement statistics and authenticated public discussion can help Alice and Bob estimate whether their raw data are suitable for further post-processing.

In this repository, both protocols are educational simulations. They produce candidate key material and QBER estimates under simplified assumptions; they do not produce deployable cryptographic keys.

## BB84 in this repository

- Uses single-qubit preparation choices represented by random bits and two basis labels.
- Uses random Bob measurement bases and retains only matching-basis positions.
- Includes a toy intercept-resend option in the refactored package.
- Uses a simple QBER threshold as a teaching heuristic, not as a finite-key security statement.

## Simplified E91 in this repository

- Uses entangled-pair intuition and random basis labels.
- Models matching-basis correlations and key extraction from matching settings.
- Does not currently implement CHSH/Bell-test statistics, explicit E91 security acceptance criteria, or finite-key analysis.

## Practical differences

| Aspect | BB84 implementation | Simplified E91 implementation |
|---|---|---|
| Quantum resource modeled | Prepared single-qubit states | Entangled-pair correlations |
| Sifting rule | Keep matching preparation/measurement bases | Keep matching measurement settings |
| Toy eavesdropper model | Intercept-resend in package CLI | Not currently implemented |
| Bell/CHSH test | Not applicable to BB84 flow | Not currently implemented |
| Security interpretation | Protocol intuition only | Entanglement-and-sifting demonstration only |

## Important caveat

Real QKD systems require authenticated classical channels, error correction, privacy amplification, finite-key analysis, calibrated hardware models, and implementation-security review. The simulations here are useful for learning protocol mechanics, not for certifying practical secrecy.
