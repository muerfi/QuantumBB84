import numpy as np
from qiskit import QuantumCircuit, execute, Aer

# Parameters
n = 4
total_pairs = 4 * n
shots = 1024

def simulate_e91():
    """Run a minimal E91-style entanglement simulation for key extraction."""
    qc = QuantumCircuit(total_pairs * 2, total_pairs * 2)
    
    # Create entangled pairs (Bell state)
    for i in range(0, total_pairs * 2, 2):
        qc.h(i)
        qc.cx(i, i + 1)
    
    # Random bases for Alice and Bob
    alice_bases = np.random.choice([0, 1, 2], total_pairs)  # 0: Z, 1: X, 2: 45°
    bob_bases = np.random.choice([0, 1, 2], total_pairs)    # Same
    
    for i, (a_base, b_base) in enumerate(zip(alice_bases, bob_bases)):
        if a_base == 1:
            qc.h(2 * i)
        elif a_base == 2:
            qc.rz(np.pi / 4, 2 * i)
        if b_base == 1:
            qc.h(2 * i + 1)
        elif b_base == 2:
            qc.rz(np.pi / 4, 2 * i + 1)
        qc.measure(2 * i, 2 * i)
        qc.measure(2 * i + 1, 2 * i + 1)
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts()
    meas = np.array([int(x) for x in list(counts.keys())[0][::-1]])
    alice_meas = meas[::2]
    bob_meas = meas[1::2]
    
    matching_indices = np.where(alice_bases == bob_bases)[0]
    if len(matching_indices) < 2 * n:
        return None, float('inf')
    
    alice_key = alice_meas[matching_indices][:n]
    bob_key = bob_meas[matching_indices][:n]
    alice_check = alice_meas[matching_indices][n:2*n]
    bob_check = bob_meas[matching_indices][n:2*n]
    error_rate = np.mean(alice_check != bob_check)
    
    print(f"Alice's key: {alice_key}")
    print(f"Bob's key: {bob_key}")
    print(f"Error rate: {error_rate:.3f}")
    return alice_key, error_rate

if __name__ == "__main__":
    simulate_e91()
