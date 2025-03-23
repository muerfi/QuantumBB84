# The BB84 Protocol - Quantum Key Distribution  

## Protocol Steps  
1. **Preparation by Alice**:  
   - Alice generates `(4 + δ)n` random bits (e.g., `[1 0 1 0]`).  
   - She randomly chooses a basis for each bit (0 for Z: `{|0⟩, |1⟩}`, 1 for X: `{|+⟩, |-⟩}`).  
   - Example: Bits `[1 0 1 0]`, bases `[1 0 1 0]` → `[|-⟩ |0⟩ |-⟩ |0⟩]`.  

2. **Transmission**:  
   - Alice sends these qubits to Bob via a quantum channel (e.g., polarized photons).  

3. **Measurement by Bob**:  
   - Bob randomly chooses bases (e.g., `[1 0 1 1]`) and measures the qubits.  
   - Result: `[1 0 1 1]`.  

4. **Basis Announcement**:  
   - Alice reveals her bases (`[1 0 1 0]`).  
   - Bob compares them with his and keeps the bits where the bases match (here: `[1 0 1]`).  

5. **Verification**:  
   - They select `n` bits to test for interference (check bits).  
   - If too many errors (>5%) occur, they suspect Eve and discard the key.  

6. **Final Key**:  
   - The remaining `n` bits form the shared key.  

## Quantum Security  
- **Measurement Principle**: Measuring a qubit in the wrong basis disturbs it (50% chance of error).  
- **Eve Detection**: If Eve intercepts and measures, she introduces detectable errors during verification.  

## Example with Interception  
- Alice: `[1 0 1 0]` (bases: `[1 0 1 0]`)  
- Eve: Measures in `[0 1 0 1]`, disturbs the qubits.  
- Bob: `[1 1 0 1]` (bases: `[1 0 1 0]`)  
- Check bits: Mismatch → Eve detected!  

## References  
- [BB84 Paper](https://arxiv.org/abs/quant-ph/0003004)  
- Qiskit Documentation  
