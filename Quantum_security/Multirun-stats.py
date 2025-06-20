import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key
import pandas as pd

# Parameters
n = 4
total_qubits = 4 * n
shots = 1
runs = 100  # Number of runs
threshold = 0.05

def run_single(with_eve=False):
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)
    
    qc = QuantumCircuit(total_qubits, total_qubits)
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)
    
    if with_eve:
        eve_bases = generate_random_bits(total_qubits)
        for i in range(total_qubits):
            if eve_bases[i] == 1:
                qc.h(i)
            qc.measure(i, i)
            qc.reset(i)
            if alice_bits[i] == 1:
                qc.x(i)
            if alice_bases[i] == 1:
                qc.h(i)
    
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])
    
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        return False, float('inf')
    
    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    error_rate = np.mean(alice_check != bob_check)
    success = error_rate <= threshold and np.array_equal(alice_key, bob_key)
    return success, error_rate

def multi_run_stats():
    stats = {'no_eve': {'success': [], 'error_rates': []}, 'with_eve': {'success': [], 'error_rates': []}}
    
    for _ in range(runs):
        success_no_eve, error_no_eve = run_single(with_eve=False)
        stats['no_eve']['success'].append(success_no_eve)
        stats['no_eve']['error_rates'].append(error_no_eve)
        
        success_with_eve, error_with_eve = run_single(with_eve=True)
        stats['with_eve']['success'].append(success_with_eve)
        stats['with_eve']['error_rates'].append(error_with_eve)
    
    # Analysis
    df = pd.DataFrame({
        'Without Eve - Success': stats['no_eve']['success'],
        'Without Eve - Error Rates': stats['no_eve']['error_rates'],
        'With Eve - Success': stats['with_eve']['success'],
        'With Eve - Error Rates': stats['with_eve']['error_rates']
    })
    df.to_csv("Experiments/multi_run_stats.csv", index=False)
    
    print("=== Statistics ===")
    print(f"Without Eve - Success Rate: {np.mean(stats['no_eve']['success']):.3f}")
    print(f"Without Eve - Average Error Rate: {np.mean(stats['no_eve']['error_rates']):.3f}")
    print(f"With Eve - Success Rate: {np.mean(stats['with_eve']['success']):.3f}")
    print(f"With Eve - Average Error Rate: {np.mean(stats['with_eve']['error_rates']):.3f}")

if __name__ == "__main__":
    multi_run_stats()
