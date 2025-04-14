# Scalar Drift Simulation — Early Field Resonance Detector
import sympy
import math
import scalarcore as sc  # 🔗 Scalar constants

max_cycles = 9013
error_threshold = 11
prime_ref = max_cycles

# Trackers
errors = 0
prime_hits = 0
golden_hits = 0
pi_hits = 0
scalar_hits = 0

print("\n🌀 Scalar Drift Simulation Starting...")

for i in range(1, max_cycles + 1):
    if i % error_threshold == 0:
        errors += 1

    if i % prime_ref == 0:
        prime_hits += 1
        prime_ref = sympy.prevprime(prime_ref)

    phi_ratio = i / sc.PHI
    if abs(round(phi_ratio) - phi_ratio) < 0.0001:
        golden_hits += 1

    pi_ratio = i / sc.PI
    if abs(round(pi_ratio) - pi_ratio) < 0.0001:
        pi_hits += 1

    if sc.is_resonant_scalar(i, base=sc.a_H, tol=0.01):
        scalar_hits += 1

print("\n=== Scalar Drift Summary ===")
print(f"Cycle Count          : {max_cycles}")
print(f"Error Corrections    : {errors}")
print(f"Prime Resets         : {prime_hits}")
print(f"Golden Ratio Hits    : {golden_hits}")
print(f"Pi Ratio Hits        : {pi_hits}")
print(f"Scalar Resonances    : {scalar_hits}")
print("===========================")

