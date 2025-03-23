# QuantumBB84 - Quantum Cryptography with BB84

Welcome to QuantumBB84, an educational and practical project dedicated to the BB84 protocol, one of the first Quantum Key Distribution (QKD) methods. This repository explores how BB84 works, its foundations in quantum physics, and its philosophical implications, while also providing Python simulations with Qiskit.

## Why BB84 ?
In a world where data security is crucial, BB84 leverages the laws of quantum mechanics to ensure secure key distribution between Alice and Bob, even in the presence of an eavesdropper like Eve. This project takes you to the heart of this technological revolution !

## Repository Structure

- **`Docs/`** : Detailed explanations of the protocol, quantum physics, and philosophy.
  - [BB84_Protocol.md](Docs/BB84_Protocol.md) : The core of the protocol.
  - [Quantum_Physics.md](Docs/Quantum_Physics.md) : Superposition, measurement, and entanglement.
  - [Philosophy.md](Docs/Philosophy.md) : Reflections on reality and security.
  - [Practical_Limits.md](Docs/Practical_Limits.md) : Practical considerations in QKD.
  - [Quantum_Info.md](Docs/Quantum_Info.md) : Quantum information theory applied to BB84 (von Neumann entropy, channel capacity, etc.).
  - **`Equations/`** : Mathematical analysis and documentation.
    - [QuantumBB84_Equation.pdf](Docs/Equations/QuantumBB84_Equation.pdf) : Detailed report with equations and simulations.
    - [QuantumBB84_Advanced.tex](Docs/Equations/QuantumBB84_Advanced.tex) : LaTeX source for the report.
    - **`figs/`** : Figures used in the report (figure1.png, figure2.png, etc.).
    - **`scripts/`** : Python scripts to generate the figures in the report (generate_figure1.py, etc.).

- **`Code/`** : Python simulations using Qiskit.
  - [BB84_Simulation.py](Code/BB84_Simulation.py) : Complete simulation.
  - [BB84_No_Eve.py](Code/BB84_No_Eve.py) : Without interception.
  - [BB84_With_Eve.py](Code/BB84_With_Eve.py) : With Eve.
  - [Noise_Analysis.py](Code/Noise_Analysis.py) : Analysis of noise effects.
  - [Interactive_Visualization.py](Code/Interactive_Visualization.py) : Interactive visualizations.
  - [MultiRun_Stats.py](Code/MultiRun_Stats.py) : Statistics over multiple runs.
  - [utils.py](Code/utils.py) : Utility functions.

- **`Attacks/`** : Implementations of quantum attacks.
  - [PNS_Attack.py](Attacks/PNS_Attack.py) : Photon Number Splitting attack.
  - [Beam_Split_Attack.py](Attacks/Beam_Split_Attack.py) : Beam Split attack.
  - [Attack_q-bits.py](Attacks/Attack_q-bits.py) : Another implementation of a PNS attack with q-bit simulation.
  - [README.md](Attacks/README.md) : Explanations of the attacks.

- **`Protocols/`** : Comparison of QKD protocols.
  - **`BB84/`** : BB84 implementation.
    - [BB84_Simulation.py](Protocols/BB84/BB84_Simulation.py) : Main BB84 simulation.
    - [README.md](Protocols/BB84/README.md) : Details on BB84.
  - **`E91/`** : E91 implementation.
    - [E91_Simulation.py](Protocols/E91/E91_Simulation.py) : E91 simulation.
    - [README.md](Protocols/E91/README.md) : Details on E91 and Comparison of BB84 vs E91

- **`Examples/`** : Concrete results from simulations.
  - [simulation.md](Examples/simulation.md) : Example simulation results.

- **`Resources/`** : Links and a glossary for further learning.
  - [glossary.md](Resources/glossary.md) : Glossary of terms.
  - [references.md](Resources/references.md) : References and further reading.

## Prerequisites

- **Python 3.8+** : Ensure you have Python 3.8 or higher installed.
- **Qiskit** : For quantum simulations (`pip install qiskit qiskit-aer`).
  - Note: `qiskit-aer` is required for simulation backends like QASM simulator.
- **NumPy** : For numerical computations (`pip install numpy`).
- **Matplotlib** : For generating graphs (`pip install matplotlib`).
- **LaTeX Distribution** : To compile the PDF (`QuantumBB84_Equation.pdf`), install a LaTeX distribution like TeX Live or MiKTeX.
  - On Windows: Install MiKTeX (https://miktex.org/download).
  - On Linux/Mac: Install TeX Live (`sudo apt install texlive-full` on Ubuntu).
- **Plotly** (optional) : For interactive visualizations in `Interactive_Visualization.py` (`pip install plotly`).

## How to Use This Repository ?
1. **Clone the repository** :
   ```bash
   git clone https://github.com/muerfi/QuantumBB84.git
   cd QuantumBB84
