import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Code.utils import generate_random_bits, compare_bases, extract_key

# Parameters
n = 4  # Length of the final key
total_qubits = 4 * n  # Total qubits sent (before sifting)
shots = 1024  # Number of shots for simulation
eve_present = True  # Toggle Eve's presence (True/False)
intercept_prob = 0.5  # Probability that Eve intercepts a qubit
threshold = 0.05  # Error rate threshold for detecting Eve

def simulate_bb84(eve_present=True, intercept_prob=0.5):
    """
    Simulate the BB84 protocol with or without Eve's interception.
    
    Args:
        eve_present (bool): If True, Eve intercepts with given probability.
        intercept_prob (float): Probability that Eve intercepts a qubit.
    
    Returns:
        tuple: (alice_key, bob_key, eve_key, error_rate)
    """
    # Step 1: Alice generates random bits and bases
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)  # 0 for Z basis, 1 for X basis
    
    # Step 2: Alice prepares qubits
    qc = QuantumCircuit(total_qubits, total_qubits)
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)  # Encode |1⟩
        if alice_bases[i] == 1:
            qc.h(i)  # Use Hadamard (X basis) if basis is 1
    
    # Step 3: Eve's interception (if present)
    eve_bits = np.zeros(total_qubits, dtype=int) if eve_present else None
    if eve_present:
        eve_bases = generate_random_bits(total_qubits)  # Eve chooses random bases
        for i in range(total_qubits):
            if np.random.random() < intercept_prob:  # Eve decides to intercept
                if eve_bases[i] == 0:  # Z basis
                    qc.measure(i, i)  # Measure in Z basis
                    result = execute(qc, Aer.get_backend('qasm_simulator'), shots=1).result()
                    eve_bits[i] = int(list(result.get_counts().keys())[0][0])
                    qc.reset(i)  # Reset qubit
                    if eve_bits[i] == 1:
                        qc.x(i)  # Re-prepare qubit
                else:  # X basis
                    qc.h(i)  # Switch to X basis
                    qc.measure(i, i)  # Measure in X basis
                    result = execute(qc, Aer.get_backend('qasm_simulator'), shots=1).result()
                    eve_bits[i] = int(list(result.get_counts().keys())[0][0])
                    qc.reset(i)  # Reset qubit
                    if eve_bits[i] == 1:
                        qc.x(i)  # Re-prepare qubit
                    qc.h(i)  # Switch back to original basis
    
    # Step 4: Bob measures in random bases
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)  # Use Hadamard (X basis) if basis is 1
        qc.measure(i, i)
    
    # Step 5: Run the simulation
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    
    # Step 6: Sift keys (keep only where bases match)
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        print("Not enough matching bases to extract a key!")
        return None, None, None, float('inf')
    
    # Step 7: Extract keys and check bits
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    eve_key = extract_key(eve_bits, matching_indices, n)[0] if eve_present else None
    
    # Step 8: Calculate error rate
    error_rate = np.mean(alice_check != bob_check)
    
    # Step 9: Output results
    print(f"Alice's Key: {alice_key}")
    print(f"Bob's Key: {bob_key}")
    if eve_present:
        print(f"Eve's Key: {eve_key}")
    print(f"Error Rate: {error_rate:.3f}")
    
    # Step 10: Check for Eve's presence
    if error_rate > threshold:
        print("Interference detected! Aborting key exchange.")
        return None, None, None, error_rate
    print("Key exchange successful!")
    return alice_key, bob_key, eve_key, error_rate

if __name__ == "__main__":
    alice_key, bob_key, eve_key, error_rate = simulate_bb84(eve_present=eve_present, intercept_prob=intercept_prob)
