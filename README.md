# QuantumBB84 - Exploring Quantum Key Distribution

Welcome to QuantumBB84, an educational and practical project dedicated to Quantum Key Distribution (QKD). This repository explores two foundational QKD protocols BB84 and E91 along with their foundations in quantum physics, philosophical implications, theoretical analyses, attack implementations, and Python simulations using Qiskit.

## Project Motivation
In a world where data security is increasingly critical, Quantum Key Distribution (QKD) offers a revolutionary approach to secure communication by leveraging the laws of quantum mechanics. This project explores two foundational QKD protocols: BB84, which ensures secure key distribution using single qubits, and E91, which uses quantum entanglement and Bell's inequalities to detect eavesdroppers like Eve. Through simulations, theoretical analyses, and attack implementations, this project provides a comprehensive look at the principles, security, and practical challenges of quantum cryptography.

## Repository Structure

- **`Docs/`** : Detailed explanations of the protocol, quantum physics, and philosophy
  - [BB84_Protocol.md](Docs/BB84_Protocol.md) : The core of the protocol
  - [Quantum_Physics.md](Docs/Quantum_Physics.md) : Superposition, measurement, and entanglement
  - [Philosophy.md](Docs/Philosophy.md) : Reflections on reality and security
  - [Practical_Limits.md](Docs/Practical_Limits.md) : Practical considerations in QKD
  - [Quantum_Info.md](Docs/Quantum_Info.md) : Quantum information theory applied to BB84 (von Neumann entropy, channel capacity, etc..)
  - **`Equations/`** : Mathematical analysis and documentation.
    - [QuantumBB84_Equation.pdf](Docs/Equations/QuantumBB84_Equation.pdf) : Detailed report with equations and simulations
    - **`figs/`** : Figures used in the report
      - [figure1.png](Docs/Equations/figs/figure1.png)
      - [figure2.png](Docs/Equations/figs/figure2.png)
      - [figure3.png](Docs/Equations/figs/figure3.png)
      - [figure4.png](Docs/Equations/figs/figure4.png)
    - **`scripts/`** : Python scripts to generate the figures in the report
      - [model1.py](Docs/Equations/scripts/model1.py)
      - [model2.py](Docs/Equations/scripts/models2.py)
      - [model3.py](Docs/Equations/scripts/models3.py)
      - [model4.py](Docs/Equations/scripts/models4.py)

- **`Quantum_security/`** : Python simulations using Qiskit
  - [BB84_Simulation.py](Quantum_security/BB84_Simulation.py) : Complete simulation
  - [BB84_No_Eve.py](Quantum_security/BB84_No_Eve.py) : Without interception
  - [BB84_With_Eve.py](Quantum_security/BB84_With_Eve.py) : With Eve
  - [Noise_Analysis.py](Quantum_security/Noise_Analysis.py) : Analysis of noise effects
  - [Interactive_Visualization.py](Quantum_security/Interactive-visualization.py) : Interactive visualizations
  - [MultiRun_Stats.py](Quantum_security/Multirun-stats.py) : Statistics over multiple runs
  - [utils.py](Quantum_security/utils.py) : Utility functions

- **`Attacks/`** : Implementations of quantum attacks
  - [PNS_Attack.py](Attacks/PNS_Attack.py) : Photon Number Splitting attack
  - [Beam_Split_Attack.py](Attacks/Beam_Split_Attack.py) : Beam Split attack
  - [Attack_q-bits.py](Attacks/Attack_q-bits.py) : Another implementation of a PNS attack with q-bit simulation
  - [README.md](Attacks/README.md) : Explanations of the attacks

- **`Protocols/`** : Comparison of QKD protocols
  - **`BB84/`** : BB84 implementation
    - [BB84_Simulation.py](Protocols/BB84/BB84_Simulation.py) : Main BB84 simulation
    - [README.md](Protocols/BB84/README.md) : Details on BB84
  - **`E91/`** : E91 implementation
    - [E91_Simulation.py](Protocols/E91/E91_Simulation.py) : E91 simulation
    - [README.md](Protocols/E91/README.md) : Details on E91 and Comparison of BB84 vs E91
  - [README.md](Protocols/README.md) : Comparison of BB84 vs E91

- **`Experiments/`** : Concrete results from simulations
  - [simulation.md](Experiments/simulation.md) : Example simulation results

- **`Resources/`** : Links and a glossary for further learning
  - [glossary.md](Resources/glossary.md) : Glossary of terms
  - [references.md](Resources/references.md) : References and further reading

## Prerequisites

- **Python 3.8+** : Ensure you have Python 3.8 or higher installed
- **Qiskit** : For quantum simulations (`pip install qiskit qiskit-aer`)
  - Note: `qiskit-aer` is required for simulation backends like QASM simulator
- **NumPy** : For numerical computations (`pip install numpy`)
- **Matplotlib** : For generating graphs (`pip install matplotlib`)
- **Plotly** (optional) : For interactive visualizations (`pip install plotly`)

## How to Use This Repository ?
1. **Clone the repository** :
   ```bash
   git clone https://github.com/muerfi/QuantumBB84.git
   cd QuantumBB84
