# Usage Guide

This guide describes the supported package and command-line interface for the Quantum Key Distribution Simulation Lab.

## Installation

From a local checkout:

```bash
git clone https://github.com/muerfi/QuantumBB84.git
cd QuantumBB84
python -m pip install -e '.[dev]'
```

The core package currently has no mandatory third-party runtime dependencies. Development tests require `pytest` through the `dev` extra. Optional legacy or plotting workflows may require additional packages:

```bash
python -m pip install -e '.[plot,qiskit,dev]'
```

## Running CLI commands

The recommended CLI entry point during development is:

```bash
python -m quantum_bb84 --help
```

Run a BB84 simulation:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
```

Run BB84 with toy intercept-resend eavesdropping:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
```

Run BB84 with simple independent bit-flip noise:

```bash
python -m quantum_bb84 simulate bb84 --qubits 1000 --noise 0.03 --seed 7
```

Run the simplified E91-style simulation:

```bash
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

After installation, the console script may also be available as:

```bash
quantum-bb84 simulate bb84 --qubits 100 --seed 42
```

## Reproducing example simulations

To reproduce the README examples exactly, run:

```bash
python -m quantum_bb84 simulate bb84 --qubits 100 --seed 42
python -m quantum_bb84 simulate bb84 --qubits 100 --eve intercept_resend --eve-rate 0.2 --seed 42
python -m quantum_bb84 simulate e91 --pairs 100 --seed 42
```

The fixed seed controls pseudo-random bits, bases, Eve choices, and noise draws used by the refactored package. Different Python versions should produce stable outputs as long as the underlying implementation remains unchanged, but documented example outputs should still be checked after code changes.

## Understanding output metrics

The CLI prints JSON. Common fields include:

- `protocol`: `BB84` or `E91-simplified`.
- `qubits` / `pairs`: number of transmitted BB84 signals or entangled-pair trials requested.
- `seed`: pseudo-random seed used for reproducibility.
- `sifted_bits`: positions retained after basis reconciliation.
- `check_bits`: sifted positions publicly compared for QBER estimation.
- `candidate_key_bits`: sifted positions not used as check bits.
- `qber`: fraction of check bits where Alice and Bob disagree.
- `noise_probability`: independent bit-flip probability applied in the model.
- `eve`: optional toy Eve model for BB84.
- `eve_rate`: probability that Eve intercepts each BB84 signal in the toy attack.
- `threshold`: configured toy QBER threshold.
- `accepted_under_toy_threshold`: whether the finite-sample QBER was at or below `threshold`.
- `notes`: caveats emitted by the simulation.

Important interpretation: `candidate_key_bits` are not final secure key bits. The package does not currently implement authenticated discussion, error correction, privacy amplification, finite-key bounds, or hardware security analysis.

## Running tests

Run all tests:

```bash
python -m pytest
```

Run selected tests while developing:

```bash
python -m pytest tests/test_cli.py
python -m pytest tests/test_protocols.py
python -m pytest tests/test_qber_and_sifting.py
```

## Troubleshooting

### `No module named quantum_bb84`

Run commands from the repository root or install the package in editable mode:

```bash
python -m pip install -e '.[dev]'
```

### `pytest` is not installed

Install the development extra:

```bash
python -m pip install -e '.[dev]'
```

### JSON output differs from the README

Check that you used the same command, seed, qubit or pair count, Eve rate, noise probability, check fraction, and threshold. If the implementation changed, update the example output and include the change in tests or documentation review.

### A toy attack is not detected

This can happen, especially with small finite samples or low Eve rates. A threshold pass means only that the sampled check bits did not exceed the configured toy threshold. It does not prove that no adversary was present.

### Legacy Qiskit scripts fail

The supported reproducible interface is the `quantum_bb84` package. Older scripts under directories such as `Quantum_security/`, `Protocols/`, and `Attacks/` may rely on older Qiskit/Aer APIs or local plotting assumptions. Treat them as historical educational material unless they have been updated and tested in your environment.
