# Comparison of QKD Protocols: BB84 vs E91

## Overview of BB84 and E91

### BB84 Protocol
- **Introduced**: 1984 by Charles Bennett and Gilles Brassard.
- **Core Mechanism**: Uses single qubits prepared in one of four states (\(|0\rangle\), \(|1\rangle\), \(|+\rangle\), \(|-\rangle\)) and sent from Alice to Bob.
- **Security Basis**: Relies on the no-cloning theorem and the disturbance caused by measurement in an incorrect basis.
- **Key Steps**:
  1. Alice sends qubits in random bases (Z or X).
  2. Bob measures in random bases.
  3. They sift the key by keeping bits where bases match.
  4. They estimate the error rate to detect Eve.
  5. Error correction and privacy amplification finalize the key.

### E91 Protocol
- **Introduced**: 1991 by Artur Ekert.
- **Core Mechanism**: Uses entangled qubit pairs (Bell states) shared between Alice and Bob.
- **Security Basis**: Relies on quantum entanglement and the violation of Bell’s inequalities to detect eavesdropping.
- **Key Steps**:
  1. A source generates entangled pairs (e.g., $$  |\psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}  $$).
  2. Alice and Bob measure their qubits in random bases (Z, X, or 45°).
  3. They sift the key by keeping measurements where bases match.
  4. They estimate the error rate and perform a CHSH test to confirm entanglement.
  5. Error correction and privacy amplification finalize the key.

## Comparison

### Similarities
- **Objective**: Both protocols aim to securely distribute a cryptographic key between Alice and Bob.
- **Quantum Principles**: Both rely on the no-cloning theorem to prevent Eve from copying quantum states without introducing errors.
- **Sifting**: Both protocols involve a sifting step where Alice and Bob discard measurements where their bases do not match.
- **Error Detection**: Both use error rate estimation to detect the presence of an eavesdropper.
- **Post-Processing**: Both require error correction and privacy amplification to finalize the key.

### Differences

| **Aspect**            | **BB84**                                                                 | **E91**                                                                 |
|-----------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Quantum Resource**  | Single qubits prepared in Z or X basis.                                 | Entangled qubit pairs (Bell states).                                     |
| **Security Mechanism**| Measurement disturbance (Eve’s incorrect basis introduces errors).      | Violation of Bell’s inequalities (CHSH test confirms entanglement).      |
| **Measurement Bases** | Two bases: Z (\( \theta = 0 \)) and X (\( \theta = \pi/2 \)).          | Three bases: Z (\( \theta = 0 \)), X (\( \theta = \pi/2 \)), 45° (\( \theta = \pi/4 \)). |
| **Key Correlation**   | Alice and Bob’s bits are identical when bases match.                   | Alice and Bob’s bits are anti-correlated (e.g., 0 for Alice, 1 for Bob).|
| **Eve Detection**     | Based solely on error rate (e.g., >5% indicates Eve).                  | Error rate + CHSH test (\( S \leq 2\sqrt{2} \); a lower \( S \) indicates Eve). |
| **Implementation**    | Simpler to implement experimentally (no entanglement required).         | Requires a source of entangled pairs, harder to implement.              |

### Security Analysis
- **BB84**:
  - Eve’s interception (e.g., intercept-resend attack) introduces a 25% error rate on average because she guesses the basis incorrectly 50% of the time, and half of the bits are kept after sifting.
  - Security relies on the error rate being low in the absence of Eve.
- **E91**:
  - Security is enhanced by the CHSH test. Even if Eve intercepts, she cannot replicate the quantum correlations required to violate Bell’s inequalities (\( S > 2 \)).
  - Provides a stronger theoretical guarantee of security due to entanglement.

## Implementations in This Project

### BB84 Implementation
- **Location**: [BB84/](BB84/)
- **Script**: [BB84_Simulation.py](BB84/BB84_Simulation.py)
- **Features**:
  - Simulates Alice sending single qubits to Bob.
  - Includes an optional Eve with configurable interception probability.
  - Performs sifting, error estimation, and key extraction.
  - Detects Eve based on a threshold error rate (default: 0.05).
- **Example Output (with Eve)**:
Alice's Key: [1 0 1 0]
Bob's Key: [1 0 0 1]
Eve's Key: [0 1 0 0]
Error Rate: 0.250
Interference detected! Aborting key exchange.

### E91 Implementation
- **Location**: [E91/](E91/)
- **Script**: [E91_Simulation.py](E91/E91_Simulation.py)
- **Features**:
- Simulates the generation of entangled Bell states.
- Alice and Bob measure in three bases (Z, X, 45°).
- Performs sifting and error estimation.
- Note: Does not currently simulate Eve or perform the CHSH test.
- **Example Output**:
Alice's key: [0 1 0 1]
Bob's key: [1 0 1 0]
Error rate: 0.000

- Keys are anti-correlated due to the entangled state.

## Usage

To run the simulations:

1. Ensure you have the prerequisites installed (see the main [README.md](../README.md)).
2. Navigate to the respective directories:
 - For BB84:
   ```bash
   cd Protocols/BB84
   python BB84_Simulation.py
  - For E91:
 ```bash
 cd Protocols/E91
python E91_Simulation.py
