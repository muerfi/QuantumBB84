import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from Code.utils import generate_random_bits, compare_bases, extract_key

# Global parameters
n = 4  # Target key length
delta = 0  # No additional margin of error here
total_qubits = int((4 + delta) * n)  # Total number of qubits sent
shots = 1024  # Number of simulations for statistics
error_threshold = 0.05  # Error threshold for detecting Eve

def simulate_bb84(with_eve=False):
    """Simulates the BB84 protocol with or without Eve."""
    # Alice generates random bits and bases
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    print(f"Alice's bits: {alice_bits}")
    print(f"Alice's bases: {alice_bases}")

    # Create the quantum circuit
    qc = QuantumCircuit(total_qubits, total_qubits)

    # Alice prepares the qubits
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)  # |0⟩ → |1⟩
        if alice_bases[i] == 1:
            qc.h(i)  # Z basis → X basis (|+⟩ or |-⟩)

    # Eve intercepts
    if with_eve:
        eve_bases = generate_random_bits(total_qubits)
        print(f"Eve's bases: {eve_bases}")
        for i in range(total_qubits):
            if eve_bases[i] == 1:
                qc.h(i)  # Measure in X
            qc.measure(i, i)  # Eve measures and disturbs
            qc.reset(i)  # Resets for simulating the transmission
            if alice_bits[i] == 1:
                qc.x(i)  # Recreates the state (approximation)
            if alice_bases[i] == 1:
                qc.h(i)

    # Bob measures
    bob_bases = generate_random_bits(total_qubits)
    print(f"Bob's bases: {bob_bases}")
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)  # Measure in X
        qc.measure(i, i)

    # Simulation
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts()
    bob_meas = np.array([int(x) for x in list(counts.keys())[0][::-1]])
    print(f"Bob's measurements: {bob_meas}")

    # Base comparison
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        print("Error: Not enough matching bits. Protocol aborted.")
        return None, None

    # Extract keys and check bits
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    print(f"Alice's key: {alice_key}")
    print(f"Alice's check bits: {alice_check}")
    print(f"Bob's key: {bob_key}")
    print(f"Bob's check bits: {bob_check}")

    # Check for interference
    error_rate = np.mean(alice_check != bob_check)
    print(f"Error rate: {error_rate:.3f}")
    if error_rate > error_threshold:
        print("Interference detected! Protocol aborted.")
        return None, None
    else:
        print("Secure key successfully exchanged!")
        return alice_key, bob_key

if __name__ == "__main__":
    print("=== BB84 Simulation without Eve ===")
    key_no_eve, _ = simulate_bb84(with_eve=False)
    print("\n=== BB84 Simulation with Eve ===")
    key_with_eve, _ = simulate_bb84(with_eve=True)

    # Visualization of results (statistics)
    if key_no_eve is not None:
        print(f"Final key without Eve: {key_no_eve}")
    if key_with_eve is not None:
        print(f"Final key with Eve: {key_with_eve}")
      
