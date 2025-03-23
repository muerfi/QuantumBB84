import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from Code.utils import generate_random_bits, compare_bases, extract_key
import matplotlib.pyplot as plt

# Parameters
n = 4  # Key length
total_qubits = 4 * n
shots = 1024
error_rates = [0.0, 0.01, 0.05, 0.1]  # Different noise levels
threshold = 0.05

def simulate_with_noise(noise_level, with_eve=False):
    """Simulates BB84 with noise in the channel."""
    # Alice's preparation
    alice_bits = generate_random_bits(total_qubits)
    alice_bases = generate_random_bits(total_qubits)

    # Circuit
    qc = QuantumCircuit(total_qubits, total_qubits)
    for i in range(total_qubits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)

    # Adding noise (depolarizing error)
    noise_model = NoiseModel()
    error = depolarizing_error(noise_level, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'h'])
    
    # Eve (optional)
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

    # Bob's measurement
    bob_bases = generate_random_bits(total_qubits)
    for i in range(total_qubits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)

    # Simulation with noise
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots, noise_model=noise_model).result()
    bob_meas = np.array([int(x) for x in list(result.get_counts().keys())[0][::-1]])

    # Comparison
    matching_indices = compare_bases(alice_bases, bob_bases)
    if len(matching_indices) < 2 * n:
        return None, float('inf')

    alice_key, alice_check = extract_key(alice_bits, matching_indices, n)
    bob_key, bob_check = extract_key(bob_meas, matching_indices, n)
    error_rate = np.mean(alice_check != bob_check)
    return (alice_key, bob_key), error_rate

def analyze_noise_impact():
    """Analyzes the impact of noise on BB84."""
    results = {'no_eve': [], 'with_eve': []}
    for noise in error_rates:
        print(f"\n=== Noise level: {noise} ===")
        
        # Without Eve
        _, error_no_eve = simulate_with_noise(noise, with_eve=False)
        results['no_eve'].append(error_no_eve)
        print(f"Error rate without Eve: {error_no_eve:.3f}")
        
        # With Eve
        _, error_with_eve = simulate_with_noise(noise, with_eve=True)
        results['with_eve'].append(error_with_eve)
        print(f"Error rate with Eve: {error_with_eve:.3f}")

    # Visualization
    plt.plot(error_rates, results['no_eve'], label="Without Eve", marker='o')
    plt.plot(error_rates, results['with_eve'], label="With Eve", marker='o')
    plt.axhline(y=threshold, color='r', linestyle='--', label=f"Threshold ({threshold})")
    plt.xlabel("Noise level")
    plt.ylabel("Error rate")
    plt.title("Impact of noise on Eve's detection")
    plt.legend()
    plt.grid()
    plt.savefig("Examples/noise_impact.png")
    plt.show()

if __name__ == "__main__":
    analyze_noise_impact()
