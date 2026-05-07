# BB84 Protocol Notes

## Recommended run command

Use the refactored package CLI for reproducible runs:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
```

The older `BB84_Simulation.py` script is retained as historical educational material and may depend on legacy Qiskit/Aer behavior.

## What the BB84 model demonstrates

The package-level BB84 simulation models a basic idealized flow:

1. Alice generates random bits and random bases.
2. Bob measures each signal in random bases.
3. Alice and Bob keep only matching-basis positions.
4. A subset of sifted bits is used as check bits to estimate QBER.
5. Remaining bits are reported as candidate key material if the toy threshold decision accepts.

The simulation can optionally include an intercept-resend toy eavesdropper.

## Security interpretation

In ideal BB84, random interception can increase the observed QBER because measurements in an incompatible basis disturb the signal state. This repository uses that idea as a finite-shot teaching model.

A low QBER in this code does not prove real-world security. The project does not implement finite-key bounds, authentication, error correction, privacy amplification, or device-security analysis.

## Simplifications

- Device imperfections are not modeled in depth.
- Noise is currently an independent bit-flip probability in the refactored package.
- Error correction and privacy amplification are not implemented as real post-processing modules.
- Reported candidate key lengths and QBER values are demonstration metrics.
