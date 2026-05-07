import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key

# Parameters
n = 4
total_qubits = 4 * n
shots = 1024
multi_photon_prob = 0.2  # Probability that a pulse has multiple photons
threshold = 0.05

def simulate_pns_attack():
    """Simulate a PNS attack on BB84."""
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    
    # Circuit
    qc = QuantumCircuit(total_qubits, total_qubits)
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)
    
    # Simulation of the PNS attack by Eve
    eve_bits = np.zeros(total_qubits, dtype=int)
    for i in range(total_qubits):
        if np.random.random() < multi_photon_prob:  # Multi-photon detected
            if alice_bases[i] == 0:  # Z basis
                eve_bits[i] = alice_bits[i]
            else:  # X basis
                qc.measure(i, i)  # Eve measures in X
                result = execute(qc, Aer.get_backend('qasm_simulator'), shots=1).result()
                eve_bits[i] = int(list(result.get_counts().keys())[0])
                qc.reset(i)
                if alice_bits[i] == 1:
                    qc.x(i)
                if alice_bases[i] == 1:
                    qc.h(i)
    
    # Bob's measurement
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    
    # Comparison
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        return None, None, float('inf')
    
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    eve_key, _ = extract_key(eve_bits, matching_indices, n)
    error_rate = np.mean(alice_check != bob_check)
    
    print(f"Alice's Key: {alice_key}")
    print(f"Bob's Key: {bob_key}")
    print(f"Eve's Key: {eve_key}")
    print(f"Error Rate: {error_rate:.3f}")
    if error_rate > threshold:
        print("Interference detected!")
        return None, None, error_rate
    print("Toy PNS-style disturbance not detected in this finite check sample.")
    return alice_key, eve_key, error_rate

if __name__ == "__main__":
    alice_key, eve_key, error_rate = simulate_pns_attack()
