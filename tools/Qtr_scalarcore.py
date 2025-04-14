# qtr_gate.py

def qtr_gate(ei_expr: str) -> float:
    """
    Applies the Quantum Temporal Reflection Gate (QTR-Gate)
    to correct energy-information expressions with imaginary phase.
    """
    if "i^4" in ei_expr:
        return -1
    elif "i^2" in ei_expr:
        real_part = float(ei_expr.split("*")[0])
        return real_part - 1
    else:
        return float(ei_expr)


# qtr_cycle.py

def run_qtr_bit_cycle(seed: str, iterations=36):
    bit_length = 35
    current = seed.ljust(bit_length, '0')[:bit_length]
    results = []

    for i in range(iterations + 1):
        results.append((i, current))
        flipped = current[:18][::-1]
        shifted = current[18:] + current[:1]
        current = flipped + shifted
        current = current[-bit_length:]

    return results


# equations.py
import scalarcore as sc  # 🔗 Scalar constants + Te function
from qtr_gate import qtr_gate

def calculate_te(ei_expr: str, f: float, c: float, a: float) -> float:
    corrected_ei = qtr_gate(ei_expr)
    return sc.Te(corrected_ei, 1, f, a)  # Simplified: i=1, e=corrected_ei


# main.py
from qtr_cycle import run_qtr_bit_cycle
from equations import calculate_te

if __name__ == "__main__":
    seed = "111111110011111111"
    print("\nQTR Bit Reflection Cycle:")
    bit_cycles = run_qtr_bit_cycle(seed)
    for idx, state in bit_cycles:
        print(f"Iteration {idx}: {state}")

    print("\nQTR-Gate Te Calculation Example:")
    ei_expr = "3*i^2"
    f, c, a = 4096, 2, 2  # Can be tuned later
    te_value = calculate_te(ei_expr, f, c, a)
    print(f"Te = {te_value:.6f} for ei = {ei_expr}")

