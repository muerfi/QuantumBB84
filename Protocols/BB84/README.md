# BB84 Protocol

## Overview of BB84

The BB84 protocol allows two parties, Alice and Bob, to securely share a cryptographic key using the principles of quantum mechanics. It ensures security against eavesdropping by leveraging the no-cloning theorem and the effect of measurement on quantum states.

### Key Steps of BB84

1. **Qubit Preparation (Alice)**:
   - Alice generates a random bit string (e.g., \( 0, 1 \)).
   - For each bit, she randomly chooses a basis: Z basis (\(|0\rangle\), \(|1\rangle\)) or X basis (\(|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}\), \(|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}\)).
   - She prepares qubits accordingly and sends them to Bob over a quantum channel.

2. **Measurement (Bob)**:
   - Bob receives the qubits and measures each one in a randomly chosen basis (Z or X).
   - If Bob’s basis matches Alice’s, he measures the correct bit. If not, his measurement introduces a 50% error rate.

3. **Sifting**:
   - Alice and Bob publicly compare their bases (not the bits) and keep only the bits where their bases match.

4. **Error Estimation**:
   - They sacrifice a portion of their sifted key to estimate the error rate by comparing a subset of bits.
   - A high error rate (e.g., >5%) indicates the presence of an eavesdropper (Eve).

5. **Error Correction and Privacy Amplification**:
   - If the error rate is acceptable, they perform error correction to fix discrepancies.
   - They apply privacy amplification (e.g., hashing) to reduce Eve’s potential knowledge of the key to a negligible amount.

### Security Principles

- **No-Cloning Theorem**: Eve cannot copy an unknown quantum state without disturbing it.
- **Measurement Disturbance**: If Eve measures a qubit in the wrong basis, she introduces errors that Alice and Bob can detect.
- **Information-Theoretic Security**: The security of BB84 relies on quantum mechanics, not computational assumptions.

## Implementation in This Project

This directory contains a simulation of the BB84 protocol implemented using Qiskit, IBM's quantum computing framework.

### Files

- **[BB84_Simulation.py](BB84_Simulation.py)**:
  - A Python script that simulates the BB84 protocol with the following features:
    - Alice prepares and sends qubits.
    - Optional interception by Eve with a configurable probability.
    - Bob measures the qubits.
    - Sifting, error estimation, and key extraction.
    - Detection of Eve based on a threshold error rate.
  - The script uses utility functions from `Code/utils.py` (`generate_random_bits`, `compare_bases`, `extract_key`).

### Usage

To run the BB84 simulation:

1. Ensure you have the prerequisites installed (see the main [README.md](../../README.md)).
2. Navigate to this directory:
   ```bash
   cd Protocols/BB84
