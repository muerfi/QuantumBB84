import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key

# Parameters
n = 4
total_qubits = 4 * n
shots = 1024
error_threshold = 0.05

def simulate_bb84_no_eve():
    """Simulates BB84 without Eve's interception."""
    # Alice prepares
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    print(f"Alice's bits: {alice_bits}")
    print(f"Alice's bases: {alice_bases}")

    # Circuit
    qc = QuantumCircuit(total_qubits, total_qubits)
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)

    # Bob measures
    bob_bases = generate_random_bits(total_qubits)
    print(f"Bob's bases: {bob_bases}")
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)

    # Simulation
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    print(f"Bob's measurements: {bob_meas}")

    # Comparison
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        print("Not enough matches. Aborted.")
        return None

    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    print(f"Alice's key: {alice_key}")
    print(f"Alice's check bits: {alice_check}")
    print(f"Bob's key: {bob_key}")
    print(f"Bob's check bits: {bob_check}")

    # Check
    error_rate = np.mean(alice_check != bob_check)
    print(f"Error rate: {error_rate:.3f}")
    if error_rate > error_threshold:
        print("Unexpected error! Aborted.")
        return None
    print("Secure key: ", alice_key)
    return alice_key

if __name__ == "__main__":
    key = simulate_bb84_no_eve()
