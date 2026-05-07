# Quantum Key Distribution Simulation Lab

`QuantumBB84` is a small scientific Python project for reproducible, educational simulations of quantum key distribution (QKD) ideas. The current package focuses on idealized finite-shot models of **BB84** and a **simplified E91-style** entanglement-and-sifting workflow, with metrics such as basis reconciliation, key sifting, quantum bit error rate (QBER), simple bit-flip noise, and a toy intercept-resend eavesdropper.

The project is intended for students, instructors, and researchers who want readable code for exploring protocol mechanics and simulation assumptions. It is not a cryptographic product.

## What this project does

- Runs seeded BB84 simulations with random preparation bases, random measurement bases, basis reconciliation, key sifting, check-bit sampling, QBER reporting, and a toy accept/abort threshold.
- Runs seeded simplified E91-style simulations that model entangled-pair correlations for matching measurement settings and discard nonmatching settings during sifting.
- Adds optional independent bit-flip noise to BB84 and E91-style runs.
- Adds an optional BB84 intercept-resend toy model in which Eve measures a configurable fraction of signals in random BB84 bases and resends the inferred state.
- Returns machine-readable JSON summaries from the command line.
- Provides tests for the refactored package API, CLI smoke behavior, random utilities, noise handling, QBER, and sifting.
- Keeps older exploratory Qiskit scripts and notes for educational context, while the importable `quantum_bb84` package is the recommended interface for reproducible runs.

## What this project does not claim

This repository does **not** claim to be:

- production cryptography;
- a security proof for BB84, E91, or deployed QKD systems;
- a finite-key security analysis;
- an implementation of error correction, privacy amplification, or authentication;
- a hardware-accurate model of sources, channels, detectors, timing, calibration, or side channels;
- evidence that a real system is secure because a toy simulation accepted a candidate key.

The JSON field `accepted_under_toy_threshold` means only that the simulated check-bit QBER was at or below the configured threshold for that finite sample. It is not a real-world security guarantee.

## Scientific motivation

QKD protocols are useful examples of how quantum measurement, incompatible bases, entanglement, public discussion, and statistical testing can be combined in cryptographic protocol design. Simulations help make these mechanisms visible:

- In BB84, Alice prepares single-qubit states in one of two bases. Bob measures in randomly chosen bases. Positions with matching bases can become candidate key material.
- In idealized intercept-resend examples, an eavesdropper who measures in the wrong basis can introduce errors that Alice and Bob may detect by publicly comparing a sample.
- In E91-style protocols, entanglement supplies correlations between Alice and Bob. A full E91 security workflow would also require Bell-test statistics and finite-key analysis; this repository currently implements only a simplified entanglement-and-sifting demonstration.
- With finite numbers of qubits or pairs, observed QBER and sifted-key length fluctuate from run to run. Seeded simulations make those fluctuations reproducible.

## Quick start

From a checked-out repository:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

Each command prints a JSON summary. The full bit arrays are intentionally omitted from CLI output so that examples stay compact.

## Installation

### Development checkout

```bash
git clone https://github.com/muerfi/QuantumBB84.git
cd QuantumBB84
python -m pip install -e '.[dev]'
```

The refactored `quantum_bb84` package uses the Python standard library for its core simulations. Optional legacy scripts may require Qiskit, Aer, NumPy, Matplotlib, or Plotly.

### Optional plotting or Qiskit extras

```bash
python -m pip install -e '.[plot,qiskit,dev]'
```

If your shell treats brackets specially, quote the requirement as shown above.

## CLI examples

### BB84 without Eve

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
```

Example output from the current implementation:

```json
{
  "accepted_under_toy_threshold": true,
  "candidate_key_bits": 44,
  "check_bits": 14,
  "eve": null,
  "eve_rate": 0.0,
  "noise_probability": 0.0,
  "notes": [
    "Idealized finite-shot BB84 simulation; not production cryptography.",
    "Acceptance is only a toy threshold decision for this simulated sample."
  ],
  "protocol": "BB84",
  "qber": 0.0,
  "qubits": 100,
  "seed": 42,
  "sifted_bits": 58,
  "threshold": 0.11
}
```

### BB84 with a toy intercept-resend Eve

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
```

Example output:

```json
{
  "accepted_under_toy_threshold": true,
  "candidate_key_bits": 32,
  "check_bits": 10,
  "eve": "intercept_resend",
  "eve_rate": 0.2,
  "noise_probability": 0.0,
  "notes": [
    "Idealized finite-shot BB84 simulation; not production cryptography.",
    "Acceptance is only a toy threshold decision for this simulated sample."
  ],
  "protocol": "BB84",
  "qber": 0.1,
  "qubits": 100,
  "seed": 42,
  "sifted_bits": 42,
  "threshold": 0.11
}
```

This particular seeded finite sample remains below the default toy threshold even though Eve was present in the simulation. That is a useful reminder: finite samples can fail to detect disturbance, and a threshold pass is not proof that no adversary exists.

### BB84 with simple bit-flip noise

```bash
python -m quantum_bb84 simulate bb84 --qubits 1000 --noise 0.03 --seed 7
```

The `--noise` value is an independent bit-flip probability applied to Bob's measured bits. It is a simple channel/noise sketch, not a calibrated optical hardware model.

### Simplified E91-style run

```bash
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

Example output:

```json
{
  "accepted_under_toy_threshold": true,
  "candidate_key_bits": 29,
  "check_bits": 9,
  "noise_probability": 0.0,
  "notes": [
    "Simplified E91-style entanglement and sifting demonstration.",
    "No CHSH/Bell-test security workflow or finite-key proof is implemented."
  ],
  "pairs": 100,
  "protocol": "E91-simplified",
  "qber": 0.0,
  "seed": 42,
  "sifted_bits": 38,
  "threshold": 0.11
}
```

## Repository structure

```text
quantum_bb84/              Refactored importable Python package
  protocols/               BB84 and simplified E91 simulation code
  attacks/                 Toy attack models used by package simulations
  analysis/                QBER, key-rate, and statistics helpers
  simulation/              Noise and simulation dispatch utilities
  utils/                   Validation and random-number helpers
  visualization/           Plotting helpers for future experiments
tests/                     Pytest suite for package and CLI behavior
docs/                      Current project documentation and audit notes
Docs/, Protocols/,         Legacy educational notes and exploratory scripts
Attacks/, Quantum_security/
Resources/, Experiments/   Historical materials retained for learning context
```

Prefer `python -m quantum_bb84 ...` or the package API for reproducible work. Treat older script directories as exploratory material unless their assumptions have been reviewed for your use case.

## Core concepts in plain language

### BB84

BB84 is a prepare-and-measure QKD protocol. Alice encodes random bits into quantum states chosen from two incompatible bases. Bob measures each signal in a randomly chosen basis. Later, Alice and Bob publicly compare only the bases, not the raw bit values, and retain positions where the bases matched.

### E91

E91 is an entanglement-based QKD protocol family. Alice and Bob measure entangled pairs with selected settings and use correlations, together with suitable statistical tests, to reason about adversarial disturbance. This repository's E91 code is intentionally limited: it demonstrates matching-setting correlations and sifting, but it does not implement a full Bell-test acceptance rule or finite-key proof.

### Basis reconciliation

Basis reconciliation is the public discussion step where Alice and Bob identify which positions used compatible bases. In the simulation this is represented by matching integer basis labels.

### Key sifting

Key sifting discards positions with incompatible bases and reserves a configurable fraction of the remaining positions as check bits. The rest are reported as `candidate_key_bits`. Real QKD would require further authenticated post-processing before producing final key material.

### QBER

The quantum bit error rate is the fraction of compared check bits where Alice and Bob disagree. In this repository QBER is a finite-sample statistic computed from the public check sample. Noise, modeling assumptions, finite sampling, bugs, or adversarial disturbance can all affect it.

### Intercept-resend attack

The implemented BB84 attack is a toy intercept-resend model. Eve intercepts a configurable fraction of signals, measures each intercepted signal in a random BB84 basis, and resends the inferred state. If Eve chooses an incompatible basis, Bob may later observe additional errors in positions used for QBER estimation.

### Finite-shot effects

Runs with small numbers of qubits or entangled pairs can give noisy estimates. A seeded run with 100 qubits is good for demonstration, not for reliable parameter estimation. Increase `--qubits` or `--pairs` and repeat runs when studying trends.

### Noise model

The current noise model is an independent bit flip applied to Bob's measured bits with probability `--noise`. It is useful for controlled experiments, but it does not represent the full physics of optical channels, detector behavior, dark counts, loss, misalignment, or calibration drift.

## Reproducibility notes

- Use `--seed` for deterministic pseudo-random runs.
- Record all simulation parameters: protocol, qubits or pairs, seed, Eve model and rate, noise probability, check fraction, and threshold.
- Prefer JSON CLI summaries for scripts and notebooks.
- Do not compare unseeded runs as if they were identical experiments.
- Treat small-shot examples as demonstrations; for trends, run multiple seeds and summarize uncertainty.

## Testing

Run the package tests with:

```bash
python -m pytest
```

Useful smoke checks:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

## Limitations

- No finite-key security analysis.
- No error-correction or privacy-amplification implementation.
- No authenticated classical-channel model.
- No detector-efficiency, dark-count, dead-time, timing, calibration, or side-channel model.
- No photon-number-splitting implementation in the refactored package API.
- Simplified E91 model lacks CHSH/Bell-test statistics and acceptance criteria.
- The toy threshold is not a composable security parameter.
- Legacy scripts may use older Qiskit APIs and are not the recommended reproducible interface.

## Roadmap

Near-term improvements are documented in [`docs/ROADMAP.md`](docs/ROADMAP.md). The main directions are finite-key analysis, richer noise channels, real post-processing modules, clearer device-imperfection models, benchmark experiments, notebooks, and improved visualization.

## Further reading

See [`docs/SCIENTIFIC_NOTES.md`](docs/SCIENTIFIC_NOTES.md) for background and caveats, [`docs/USAGE.md`](docs/USAGE.md) for practical command examples, and [`docs/REFERENCES.md`](docs/REFERENCES.md) for cautious reference pointers and suggested background topics.

## License

This project is distributed under the license in [`LICENSE`](LICENSE).
