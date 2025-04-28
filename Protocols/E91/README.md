# E91 Protocol

## Overview of E91

The E91 protocol uses entangled qubit pairs to allow Alice and Bob to generate a shared cryptographic key. It relies on the properties of quantum entanglement and the violation of Bell's inequalities to detect the presence of an eavesdropper (Eve).

### Key Steps of E91

1. **Entangled Pair Generation**:
   - A source (which could be a third party or Alice/Bob) generates entangled qubit pairs in a Bell state, such as \( |\psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}} \).
   - One qubit of each pair is sent to Alice, and the other to Bob.

2. **Random Basis Measurement**:
   - Alice and Bob each randomly choose a measurement basis for their qubits:
     - Alice: Z basis (\( \theta_A = 0 \)), X basis (\( \theta_A = \pi/2 \)), or a 45° basis (\( \theta_A = \pi/4 \)).
     - Bob: Z basis (\( \theta_B = 0 \)), X basis (\( \theta_B = \pi/2 \)), or a 45° basis (\( \theta_B = \pi/4 \)).
   - They measure their qubits in these bases.

3. **Sifting**:
   - Alice and Bob publicly announce their bases and keep the measurements where their bases match.
   - Due to the entangled state, their measurements are anti-correlated when bases match (e.g., if both measure in the Z basis, Alice gets 0 and Bob gets 1, or vice versa).

4. **Error Estimation and Bell Test**:
   - They use a subset of their measurements to estimate the error rate.
   - They also compute the CHSH correlation value \( S \) using measurements in non-matching bases (e.g., Alice in \( \pi/4 \), Bob in \( \pi/2 \)). In a quantum system, \( S \leq 2\sqrt{2} \), while classical systems are limited to \( S \leq 2 \). A value of \( S \) close to \( 2\sqrt{2} \) confirms the presence of entanglement and the absence of Eve.

5. **Error Correction and Privacy Amplification**:
   - If the error rate is low and the Bell test passes, they perform error correction and privacy amplification to finalize the key.

### Security Principles

- **Entanglement**: The use of entangled states ensures that Alice’s and Bob’s measurements are anti-correlated.
- **Bell’s Inequalities**: Violation of Bell’s inequalities (\( S > 2 \)) confirms that the system is quantum and not tampered with by Eve.
- **No-Cloning Theorem**: Eve cannot copy the entangled qubits without disturbing the system, which would reduce the CHSH value \( S \).

## Implementation in This Project

This directory contains a simulation of the E91 protocol implemented using Qiskit, IBM's quantum computing framework.

### Files

- **[E91_Simulation.py](E91_Simulation.py)**:
  - A Python script that simulates the E91 protocol with the following features:
    - Generation of entangled Bell states (\( |\psi^-\rangle \)).
    - Random basis measurements by Alice and Bob (Z, X, or 45°).
    - Sifting of keys based on matching bases.
    - Error rate estimation to detect interference.
  - Note: This implementation focuses on key generation and error estimation. It does not include Eve’s interference or the CHSH test for Bell’s inequalities, but these can be added for a more complete security analysis.

### Usage

To run the E91 simulation:

1. Ensure you have the prerequisites installed (see the main [README.md](../../README.md)).
2. Navigate to this directory:
   ```bash
   cd Protocols/E91
