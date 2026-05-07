# Attack Scripts and Toy Models

This directory contains small educational attack-oriented scripts related to QKD assumptions. The refactored package currently exposes a toy BB84 intercept-resend model through the CLI:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
```

## Included legacy files

- `PNS_Attack.py` — photon-number-splitting style exploration for weak coherent pulse settings.
- `BeamSplit-Attack.py` — beam-splitting style toy model.
- `Attack_q-bits.py` — additional interception/coherent-interaction experiments.

## Scope

These scripts are not a complete adversarial framework and should not be interpreted as security analyses. They illustrate why implementation details such as multi-photon emissions, detector behavior, channel loss, timing, and calibration matter in practice.

A toy attack that passes a simple threshold in a finite simulation should be described as "not detected by this toy check sample," not as a successful real-world attack. Conversely, a threshold failure indicates disturbance in the model, not proof of a specific adversary.
