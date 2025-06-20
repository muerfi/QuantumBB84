import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key

# Parameters
n = 4
total_qubits = 4 * n
shots = 1024
split_fraction = 0.3  # Fraction of photons diverted by Eve
threshold = 0.05

def simulate_split_beam_attack():
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    
    qc_bob = QuantumCircuit(total_qubits, total_qubits)
    qc_eve = QuantumCircuit(total_qubits, total_qubits)
    
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc_bob.x(i)
            qc_eve.x(i)
        if alice_bases[i] == 1:
            qc_bob.h(i)
            qc_eve.h(i)
    
    # Eve measures a fraction of the qubits
    eve_bits = np.zeros(total_qubits, dtype=int)
    for i in range(total_qubits):
        if np.random.random() < split_fraction:
            qc_eve.measure(i, i)
            result = execute(qc_eve, Aer.get_backend('qasm_simulator'), shots=1).result()
            eve_bits[i] = int(list(result.get_counts().keys())[0])
    
    # Bob measures
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc_bob.h(i)
        qc_bob.measure(i, i)
    
    result = execute(qc_bob, Aer.get_backend('qasm_simulator'), shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        return None, None, float('inf')
    
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    eve_key, _ = extract_key(eve_bits, matching_indices, n)
    error_rate = np.mean(alice_check != bob_check)
    
    print(f"Alice's key: {alice_key}")
    print(f"Bob's key: {bob_key}")
    print(f"Eve's (partial) key: {eve_key}")
    print(f"Error rate: {error_rate:.3f}")
    return alice_key, eve_key, error_rate

if __name__ == "__main__":
    simulate_split_beam_attack()
