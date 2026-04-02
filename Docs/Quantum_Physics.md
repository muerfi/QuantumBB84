# Physical Foundations Behind BB84

This note summarizes the quantum-mechanical ideas used by BB84.

## Qubits and bases

A qubit can be prepared in different measurement bases.

- **Z basis**: \(|0\rangle, |1\rangle\)
- **X basis**: \(|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}\), \(|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}\)

In BB84, Alice encodes each classical bit using a randomly chosen basis (Z or X).

## Why basis mismatch matters

If Bob measures in the same basis Alice used, he can recover her bit (in an ideal channel).
If he measures in the other basis, his result is random relative to Alice's bit.

That same mechanism is what makes interception detectable: an eavesdropper who guesses bases incorrectly introduces extra errors.

## Measurement disturbance and no-cloning

Two principles motivate BB84 security intuition:

1. **Measurement disturbance**: measuring a state in an incompatible basis changes outcome statistics.
2. **No-cloning theorem**: unknown quantum states cannot be copied perfectly.

Together, they make passive undetectable copying impossible in the idealized protocol.

## Entanglement and relation to E91

BB84 does not require entanglement. Entanglement-based protocols (such as E91) use related physics but different security tests.

## Practical caveat

Real channels and detectors add noise and loss, so observed errors are not always caused by adversaries. That is why practical QKD systems need calibrated thresholds and stronger post-processing than toy simulations.
