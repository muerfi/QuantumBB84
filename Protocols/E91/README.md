# E91 Protocol (Implementation Notes)

## What this script demonstrates

`E91_Simulation.py` builds entangled pairs, applies random measurement settings for Alice and Bob, and extracts key/check bits from matching settings.

## What it does not yet include

- Explicit eavesdropper strategies.
- Full CHSH/Bell-test computation and acceptance criteria.
- End-to-end post-processing pipeline.

So this should be read as a compact entanglement-based key-generation demo, not a full E91 security proof implementation.

## Run

```bash
python Protocols/E91/E91_Simulation.py
```
