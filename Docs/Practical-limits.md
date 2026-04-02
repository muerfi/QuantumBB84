# Practical Limits of BB84 Deployments

## Channel loss and noise

Real optical channels introduce attenuation and noise. As distance grows, key rates typically drop and error rates become harder to interpret.

## Device-level attacks

Security proofs assume ideal components, but hardware can deviate.
Examples include detector-targeting attacks and multi-photon leakage scenarios.

## Countermeasure direction (high level)

- Better source control (including decoy-state techniques in relevant systems).
- Detector hardening and monitoring.
- Conservative parameter estimation and finite-key analysis.

## Engineering cost

QKD requires specialized hardware, calibration, and operational discipline. That cost is often the practical bottleneck, not just protocol theory.

## Bottom line

BB84 is strong at the protocol level, but end-to-end security depends on implementation quality and operating assumptions.
