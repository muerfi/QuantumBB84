# Roadmap

This roadmap lists realistic improvements that would make the project more useful as an educational and computational QKD laboratory. It is not a promise of production cryptography or real-world security validation.

## Near-term documentation and reproducibility

- Keep CLI examples synchronized with the actual `quantum_bb84` interface.
- Add more reproducible example outputs with fixed seeds and recorded parameters.
- Add notebook examples that explain BB84, simplified E91 sifting, QBER, and finite-shot variation step by step.
- Add benchmark scripts that run multiple seeds and summarize mean QBER, variance, confidence intervals, sifted length, and candidate key length.
- Improve visualizations for basis matching, QBER versus Eve rate, QBER versus noise probability, and finite-shot distributions.

## Protocol modeling

- Add finite-key analysis examples with clearly labeled assumptions and security-parameter caveats.
- Add error-correction demonstrations, such as simple parity-based reconciliation or Cascade-style educational sketches.
- Add privacy-amplification demonstrations using universal hashing, while carefully explaining what is and is not proven.
- Add an authentication model for the classical discussion channel.
- Extend the E91 module with CHSH/Bell-test statistics, explicit measurement settings, and acceptance criteria.

## Noise and device models

- Add better noise channels beyond independent bit flips, such as depolarizing noise, basis-dependent misalignment, loss/erasure, and dark-count sketches.
- Add detector-efficiency models and threshold-detector simplifications.
- Add source-imperfection models, including weak coherent pulse statistics where appropriate.
- Add simple timing, dead-time, and calibration-drift demonstrations.
- Keep every device model labeled as educational unless it is validated against a specific hardware model.

## Attack sketches

- Improve the intercept-resend model with clearer event records and multi-run statistics.
- Add photon-number-splitting demonstrations for weak coherent pulse settings, with careful caveats and decoy-state context.
- Add beam-splitting and loss-based toy examples that distinguish channel loss from adversarial information gain.
- Add simplified detector-efficiency mismatch or detector-control sketches only with strong warnings that real attacks require hardware-specific modeling.
- Avoid naming toy sketches as complete attack implementations.

## Interfaces and experiments

- Provide a stable experiment-result schema with parameters, seed, package version, warnings, and output metrics.
- Add a small experiment registry under `examples/` or `experiments/` for reproducible runs.
- Add richer plots through `quantum_bb84.visualization`.
- Add a lightweight web or interactive interface only if it preserves reproducibility and makes assumptions visible.
- Maintain tests for CLI examples, deterministic seeds, edge cases, and documented outputs.

## Manual scientific review targets

- Review the simplified E91 model before presenting it as anything more than an entanglement-and-sifting demonstration.
- Review legacy Qiskit scripts for compatibility with current Qiskit/Aer APIs before treating them as supported examples.
- Review terminology around `accepted_under_toy_threshold` whenever new post-processing features are added.
