import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Operator
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key

# Parameters
n = 4
total_qubits = 4 * n
shots = 1024
threshold = 0.05

def coherent_attack_operator():
    """Defines a global unitary operation for the coherent attack."""
    # Custom operation: Eve entangles her qubits with Alice's qubits
    # Example: U = exp(-i θ H), where H is an interaction Hamiltonian
    theta = np.pi / 8  # Small angle to minimize disturbances
    matrix = np.array([
        [np.cos(theta), 0, 0, -1j * np.sin(theta)],
        [0, np.cos(theta), -1j * np.sin(theta), 0],
        [0, -1j * np.sin(theta), np.cos(theta), 0],
        [-1j * np.sin(theta), 0, 0, np.cos(theta)]
    ])
    return Operator(matrix)

def simulate_coherent_attack():
    """Simulates a coherent attack on BB84."""
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    
    # Circuit with Eve's qubits
    qc = QuantumCircuit(total_qubits * 2, total_qubits)  # Eve adds her qubits
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)
    
    # Coherent attack: Eve applies an operation on pairs (Alice, Eve)
    attack_op = coherent_attack_operator()
    for i in range(total_qubits):
        qc.unitary(attack_op, [i, total_qubits + i], label='U_Eve')
    
    # Bob's measurement
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)
    
    # Simulation
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    
    # Eve measures her qubits
    qc_eve = QuantumCircuit(total_qubits * 2, total_qubits)
    qc_eve.compose(qc, qubits=range(total_qubits * 2), clbits=range(total_qubits))
    for i in range(total_qubits):
        qc_eve.measure(total_qubits + i, i)
    result_eve = execute(qc_eve, backend, shots=shots).result()
    eve_meas = np.array([int(x) for x in list(result_eve.get_counts().keys())[0][::-1]])
    
    # Comparison
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        return None, None, float('inf')
    
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    eve_key, _ = extract_key(eve_meas, matching_indices, n)
    error_rate = np.mean(alice_check != bob_check)
    
    print(f"Alice's key: {alice_key}")
    print(f"Bob's key: {bob_key}")
    print(f"Eve's key: {eve_key}")
    print(f"Error rate: {error_rate:.3f}")
    if error_rate > threshold:
        print("Interference detected!")
    else:
        print("Coherent attack successful without detection!")
    return alice_key, eve_key, error_rate

if __name__ == "__main__":
    simulate_coherent_attack()
