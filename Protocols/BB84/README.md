# BB84 Protocol (Implementation Notes)

## What this script demonstrates

`BB84_Simulation.py` models a basic BB84 flow:
1. Alice generates random bits and random bases.
2. Bob measures each qubit in random bases.
3. Alice/Bob keep only matching-basis positions (sifting).
4. A subset is used as check bits to estimate error rate.
5. Remaining bits become a candidate key if the error rate is below a threshold.

The script can optionally include an intercept-resend style eavesdropper.

## Security interpretation

In ideal BB84, random interception tends to increase the quantum bit error rate. This script uses that idea as a detection heuristic.

## What is simplified here

- Device imperfections are not modeled in depth.
- Error correction/privacy amplification are represented conceptually, not as full protocol modules.
- Reported key lengths and error rates are for teaching/demonstration.

## Run

```bash
python Protocols/BB84/BB84_Simulation.py
```
