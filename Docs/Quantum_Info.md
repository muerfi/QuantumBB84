# Quantum Information Theory Applied to BB84

## Von Neumann Entropy
Von Neumann entropy is the quantum analogue of Shannon entropy, defined for a quantum state described by a density matrix \( \rho \).

### Definition
For a quantum system with density matrix \rho, the von Neumann entropy is:
S(\rho) = - \text{Tr}(\rho \log_2 \rho)
where \text{Tr} is the trace and \log_2 is the base 2 logarithm.

- **Pure state**: If \rho = |\psi\rangle\langle\psi| (pure state), then S(\rho) = 0, because a pure state is perfectly determined.
- **Mixed state**: If \rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|, then S(\rho) = -\sum_i p_i \log_2 p_i, similar to classical entropy.

### Application to BB84
- **Before measurement**: Alice’s qubits are in pure states (e.g., |0\rangle \) or \( |+\rangle \)), so \( S(\rho_A) = 0.
- **After interception by Eve**: If Eve measures in a random basis, she creates a mixed state for Bob. For example, for a qubit |+\rangle measured in the Z-basis by Eve, the state becomes:
  \rho_B = \frac{1}{2} |0\rangle\langle 0| + \frac{1}{2} |1\rangle\langle 1|
  with S(\rho_B) = -(\frac{1}{2} \log_2 \frac{1}{2} + \frac{1}{2} \log_2 \frac{1}{2}) = 1 bit, indicating maximum uncertainty.

### Conditional Entropy
Quantum conditional entropy S(A|B) = S(AB) - S(B) quantifies the uncertainty about \( A \) given \( B \). In BB84:
- If Eve intercepts all qubits, S(K|E) (key given Eve) decreases, compromising security.
- Security requires S(K|E) \approx S(K), meaning Eve’s information about the key remains small.

## Quantum Channel Capacity
A quantum channel \mathcal{N} transforms an input density matrix \rho into an output \mathcal{N}(\rho). Its capacity measures the maximum amount of information it can transmit.

### Classical-Quantum Channel (BB84)
In BB84, the channel carries qubits prepared in \{|0\rangle, |1\rangle, |+\rangle, |-\rangle\}. Without Eve, the classical capacity C(\mathcal{N}) is:
C(\mathcal{N}) = \max_{p_x} I(X:B)
where I(X:B) = H(B) - H(B|X) is the mutual information, \( X \) is Alice's bits, and \( B \) is Bob's measurements. With a uniform distribution ( p_x = 1/4 ), and in the absence of noise, C \approx 1 bit per qubit (after sifting).

### Channel with Eve
If Eve intercepts, the channel becomes noisy. Holevo’s theorem limits the information accessible to Eve:
\chi(\mathcal{N}) = S(\mathcal{N}(\rho)) - \sum_x p_x S(\mathcal{N}(|\psi_x\rangle\langle\psi_x|))
For BB84 with random interception, \chi \leq 1 bit, but Eve introduces detectable errors.

### Quantum Capacity
Quantum capacity Q(\mathcal{N}) measures the transmission of entangled states. In BB84, Q = 0 because it does not use entanglement (unlike E91).

## Information-Theoretic Security of BB84
Security relies on:
- **Mutual Information**: I(A:B) \gg I(A:E), where \( A \) is Alice's key, \( B \) is Bob's key, and \( E \) is Eve’s knowledge.
- **Error correction and amplification**: After sifting, Alice and Bob use check bits to estimate S(K|E). If S(K|E) > 0, privacy amplification (hashing) reduces I(A:E) \to 0.

### Explicit Calculation
For a qubit intercepted by Eve in an incorrect basis:
- Post-measurement state: \rho = \frac{1}{2} I (maximally mixed state).
- S(\rho) = 1.
- Expected error rate: 25% (because Eve disturbs 50% of the qubits measured in a different basis, and half of the bits are kept after sifting).

## Advanced Concepts
- **Bell's Inequality and E91**: Unlike BB84, E91 uses S = 2\sqrt{2} to guarantee the absence of Eve, linking entanglement to S(AB) < S(A) + S(B) (subadditivity).
- **No-Cloning Theorem**: W: |\psi\rangle \to |\psi\rangle|\psi\rangle is impossible, ensuring that Eve cannot copy qubits without disturbance.
