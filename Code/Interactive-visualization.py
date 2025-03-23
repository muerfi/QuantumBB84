import numpy as np
from qiskit import QuantumCircuit, execute, Aer
from Code.utils import generate_random_bits, compare_bases
import plotly.graph_objects as go

# Parameters
n = 4
total_qubits = 4 * n
shots = 1024

def run_simulation(with_eve=False):
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
    return result.get_counts()

def plot_interactive(counts_no_eve, counts_with_eve):
    fig = go.Figure()
    
    # Without Eve
    states_no_eve = list(counts_no_eve.keys())
    probs_no_eve = [count / shots for count in counts_no_eve.values()]
    fig.add_trace(go.Bar(x=states_no_eve, y=probs_no_eve, name="Without Eve", marker_color='blue'))
    
    # With Eve
    states_with_eve = list(counts_with_eve.keys())
    probs_with_eve = [count / shots for count in counts_with_eve.values()]
    fig.add_trace(go.Bar(x=states_with_eve, y=probs_with_eve, name="With Eve", marker_color='red'))
    
    fig.update_layout(
        title="Distribution of Bob's measurements",
        xaxis_title="Measured States",
        yaxis_title="Probability",
        barmode='group',
        bargap=0.15
    )
    fig.write_html("Examples/distribution.html")
    fig.show()

if __name__ == "__main__":
    counts_no_eve = run_simulation(with_eve=False)
    counts_with_eve = run_simulation(with_eve=True)
    plot_interactive(counts_no_eve, counts_with_eve)
