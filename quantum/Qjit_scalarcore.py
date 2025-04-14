from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session
import sympy
import numpy as np
import os

# 🔥 Step 1: Setup Quantum Stabilization Parameters
num_qubits = 35
num_cycles = 9013
error_threshold = 11
reset_threshold = 3
prime_cap = 10**32
known_error_positions = [0, 1, 8, 127]

# 🔥 Step 2: Define Spatial QJIT Pre-Filter
def spatial_qjit(cycles, prime_ref):
    stabilized_states = []
    for i in range(cycles):
        bitstring = bin(i % 2**num_qubits)[2:].zfill(num_qubits)
        stabilized_states.append(bitstring)
        if i % prime_ref == 0 and len(stabilized_states) >= reset_threshold:
            prime_ref = sympy.prevprime(prime_ref)
    return stabilized_states, prime_ref

# 🔥 Step 3: Define Quantum QJIT Refinement
def quantum_qjit(stabilized_states):
    qc = QuantumCircuit(num_qubits, num_qubits)
    for i, state in enumerate(stabilized_states[:num_qubits]):
        if state[-1] == '1':
            qc.x(i)  # Flip qubit state
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

# 🔥 Step 4: Initialize IBM Quantum Service
service = QiskitRuntimeService()
backend = service.backend("ibm_kyiv")  # Select IBM backend

# 🔥 Step 5: Loop QJIT Execution Three Times
output_files = []
for run_idx in range(3):
    print(f"\n🔄 Running QJIT Execution on IBM - Attempt {run_idx + 1} 🔄")

    # 🔥 Step 6: Execute Spatial QJIT First
    spatial_states, final_prime = spatial_qjit(num_cycles, prime_cap)

    # 🔥 Step 7: Feed to Quantum QJIT
    sim_qc = quantum_qjit(spatial_states)

    # 🔥 Step 8: Transpile and Submit to IBM
    transpiled_qc = transpile(sim_qc, backend)

    with Session(backend=backend) as session:
        sampler = Sampler()
        job = sampler.run([transpiled_qc])
        result = job.result()

    # 🔥 Step 9: Save IBM Quantum Output
    filename = f"qjit_results_ibm_run_{run_idx + 1}.txt"
    output_files.append(filename)

    with open(filename, "w") as f:
        f.write(str(result))

    print(f"✅ Quantum Measurement Output Saved: {filename}")

# 🔥 Step 10: Print Summary
print("\n✅ All three IBM QJIT runs completed and saved. Files:")
for file in output_files:
    print(f"📂 {file}")

print("\n⚡ Now proceed with external validation by comparing these outputs.")

