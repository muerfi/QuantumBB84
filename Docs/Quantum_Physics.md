# Fondements physiques de la cryptographie quantique et du protocole BB84

## Introduction to Quantum Mechanics
Quantum mechanics is a branch of physics that describes the behavior of particles at microscopic scales. Unlike classical physics, it relies on probabilistic principles and counterintuitive states. The BB84 protocol exploits these principles to ensure unbreakable security.

### Quantum States and Qubits
A qubit, the fundamental unit of quantum information, differs from a classical bit (0 or 1) because it can exist in a superposition of states :
- Notation: |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex amplitudes, and |α|^2 + |β|^2 = 1.
- Example: A qubit in equal superposition, |ψ⟩ = (1/√2)|0⟩ + (1/√2)|1⟩, has a 50% probability of being measured as 0 or 1.

In BB84, Alice encodes her bits into qubits using two bases :
- Z basis: {|0⟩, |1⟩} (vertical/horizontal polarization for photons).
- X basis: {|+⟩, |-⟩} (diagonal states, where |+⟩ = (1/√2)(|0⟩ + |1⟩) and |-⟩ = (1/√2)(|0⟩ - |1⟩)).

### Superposition and Preparation
Superposition allows a qubit to be in an undetermined state until measured. Alice prepares her qubits by randomly selecting a basis (Z or X), making the initial state unpredictable for an external observer like Eve.

### Measurement Principle
When a qubit is measured, its state "collapses" into one of the eigenstates of the chosen basis :
- Measuring a |+⟩ qubit in the Z basis: 50% chance of obtaining |0⟩, 50% for |1⟩.
- Measuring a |0⟩ qubit in the X basis: 50% chance of obtaining |+⟩, 50% for |-⟩.

This principle is crucial for BB84: if Eve measures in a different basis than Alice, she disturbs the qubit’s state, introducing detectable errors.

### Entanglement (Broader Perspective)
Although BB84 does not directly use entanglement, this phenomenon illustrates the power of quantum mechanics. Two entangled qubits, such as |ψ⟩ = (1/√2)(|00⟩ + |11⟩), share an instantaneous correlation: measuring one determines the state of the other, even at a distance. While this inspires protocols like E91, BB84 relies solely on superposition and measurement.

### The Role of Photons
In real-world implementations, qubits are often represented by polarized photons :
- `|0⟩` : Vertical polarization (0°).
- `|1⟩` : Horizontal polarization (90°).
- `|+⟩` : Diagonal polarization (45°).
- `|-⟩` : PAnti-diagonal polarization (135°).

The quantum channel (optical fiber or free space) transmits these photons from Alice to Bob.

### Indeterminism and Security
Quantum indeterminism ensures that any interception attempt by Eve alters the qubits in a detectable way. This follows from the no-cloning theorem, which states that an unknown quantum state cannot be perfectly copied, making eavesdropping impossible without introducing disturbances.
## Application in BB84
- **Encodage** : Alice uses superposition to encode her bits in random bases.
- **Mesure aléatoire** : Bob independently selects bases, and errors due to incorrect bases are expected (50% match probability).
- **Détection** : Any additional disturbance (by Eve) increases the error rate beyond this natural threshold.

## Physical Limitations
- **Bruit** : In real-world scenarios, the quantum channel introduces noise (e.g., photon loss), requiring error correction.
- **Distance** : Decoherence limits the range without quantum repeaters.

This file explores essential physical foundations. For a practical simulation, see [BB84_Simulation.py](../Code/BB84_Simulation.py).
