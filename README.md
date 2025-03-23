# QuantumBB84 - Quantum Cryptography with BB84

Welcome to QuantumBB84, an educational and practical project dedicated to the BB84 protocol, one of the first Quantum Key Distribution (QKD) methods. This repository explores how BB84 works, its foundations in quantum physics, and its philosophical implications, while also providing Python simulations with Qiskit.

## Why BB84 ?
In a world where data security is crucial, BB84 leverages the laws of quantum mechanics to ensure secure key distribution between Alice and Bob, even in the presence of an eavesdropper like Eve. This project takes you to the heart of this technological revolution !

## Repository Structure
- **`Docs/`** : Detailed explanations of the protocol, quantum physics, and philosophy.
  - [BB84_Protocol.md](Docs/BB84_Protocol.md) : The core of the protocol
  - [Quantum_Physics.md](Docs/Quantum_Physics.md) : Superposition, measurement, and entanglement
  - [Philosophy.md](Docs/Philosophy.md) : Reflections on reality and security
- **`Code/`** : Python simulations using Qiskit.
  - [BB84_Simulation.py](Code/BB84_Simulation.py) : Complete simulation
  - [BB84_No_Eve.py](Code/BB84_No_Eve.py) : Without interception
  - [BB84_With_Eve.py](Code/BB84_With_Eve.py) : With Eve
- **`Examples/`** : Concrete results from simulations.
- **`Resources/`** : Links and a glossary for further learning.

## Prerequisites
- Python 3.8+
- Qiskit (`pip install qiskit`)
- NumPy (`pip install numpy`)
- Matplotlib (for graphs, optional : `pip install matplotlib`)

## How to Use This Repository ?
1. **Clone the repository** :
   ```bash
   git clone https://github.com/[ton-pseudo]/QuantumBB84.git
   cd QuantumBB84
