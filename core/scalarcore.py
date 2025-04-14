# scalarcore.py
# Core constants, symbolic math, and QTR functions for scalar computation

import math
import cmath
from sympy import Rational

# === Scalar Constants ===
PI = math.pi
SQRT2 = math.sqrt(2)
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
a_H = PI / SQRT2  # Huckstead Scalar
F_CLOCK = (3 * PI) / (4 * SQRT2)  # Slope-derived temporal limit factor

# Harmonic calendar day length (symbolic sidereal ratio from paper)
HARMONIC_DAY_LENGTH = Rational(37214688558, 37324800000)

# === Scalar Volume & Geometry ===
V_CONE = (PI**4) / 3  # Volume of PIne Cone: radius=pi, height=pi
R_SPHERE_EQ_VOL = (PI**3 / 4)**(1/3)  # Radius of sphere with same volume as cone
V_SPHERE_EQ_VOL = (4 / 3) * PI * (R_SPHERE_EQ_VOL ** 3)  # Should equal V_CONE

# === Slope-Based Energy Functions ===
def Te(e: float, i: float, f: float, a: float) -> float:
    """Quantum Pi-Limit energy slope function."""
    try:
        return math.sqrt(f * a * math.sqrt(e * i)) * (1 / PI)
    except ValueError:
        return float('nan')

# === Quantum Temporal Reflection (QTR) Logic ===
def QTR(e: float, i: float) -> float:
    """Temporal reflection modifier. Handles imaginary phase state logic."""
    imaginary = e * i
    # Phase corrections: subtract unit at i^2, invert at i^4
    if isinstance(imaginary, complex):
        if imaginary.imag != 0:
            phase = imaginary.imag
            if abs(phase) == 1:
                return abs(imaginary) - 1
            elif abs(phase) == 4:
                return -abs(imaginary)
    return abs(imaginary)

# === Harmonic Tools ===
def cosine_similarity(vec1, vec2):
    """Returns cosine similarity between two harmonic vectors."""
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a**2 for a in vec1))
    norm2 = math.sqrt(sum(b**2 for b in vec2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0

# === Utility Functions ===
def is_resonant_scalar(x: float, base: float = a_H, tol=1e-3) -> bool:
    """Check if x aligns with a multiple of the Huckstead Scalar."""
    return abs((x % base)) < tol or abs((x % base) - base) < tol

# === Unit Tests ===
def test_scalar_geometry(verbose: bool = False):
    """Verifies cone and projection sphere volume agreement within tolerance."""
    epsilon = 1e-6
    diff = abs(V_CONE - V_SPHERE_EQ_VOL)
    if verbose:
        print("Cone Volume:", V_CONE)
        print("Sphere Volume (Computed):", V_SPHERE_EQ_VOL)
        print("Volume Difference:", diff)
    return diff < epsilon

# === Human-readable debug print ===
if __name__ == "__main__":
    print("Huckstead Scalar a_H =", a_H)
    print("Clock Slope Factor F_CLOCK =", F_CLOCK)
    print("Harmonic Day Length (Fraction) =", HARMONIC_DAY_LENGTH)
    print("Harmonic Day Length (Float) ≈", float(HARMONIC_DAY_LENGTH))
    print("Volume of PIne Cone =", V_CONE)
    print("Equal Volume Sphere Radius =", R_SPHERE_EQ_VOL)
    print("Volume Match Test Passed:", test_scalar_geometry(verbose=True))
