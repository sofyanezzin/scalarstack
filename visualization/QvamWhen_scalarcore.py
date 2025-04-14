# Quantum-Vector Angular Model (Scalarcore-Aligned)
import numpy as np
import matplotlib.pyplot as plt
from sympy import Rational
import scalarcore as sc  # 🔗 Scalar symbolic constants

# Reference Frequencies
quantum_reference = {
    "photon": 1e15,
    "electron": 1e14,
    "proton": 1e12,
    "neutron": 1000 * sc.a_H/sc.PI # use a_H directly as neutron freq for alignment
}

stellar_reference = {
    "sun": 6e14,
    "neutron_star": 716,
    "neutron_star_high": 1432,
    "white_dwarf": 2.6e15,
    "brown_dwarf": 1e14,
    "red_giant_8M": 3.1e14,
    "red_giant_10M": 3.3e14,
    "red_giant_max": 3.2e14,
    "black_hole_7M": 143.2
}

planetary_reference = {
    "pluto": 1.2e12,
    "jupiter": 1.8e13,
    "mercury": 5.9e13,
    "venus": 3.1e13,
    "earth": 3e13,
    "mars": 2.4e13,
    "saturn": 1.3e13,
    "uranus": 1e13,
    "neptune": 8e12
}

full_reference = {**quantum_reference, **stellar_reference, **planetary_reference}

# Quantum alignment function
alignment_base = 707.10678

def quantum_alignment(frequency_hz, scale_base=alignment_base):
    return (frequency_hz / scale_base) * sc.SQRT2 / sc.PI

# Magnitude scaler
def get_custom_magnitude(particle):
    stellar_mass_map = { "sun": 1.0, "white_dwarf": 0.7, "neutron_star": 1.4, "neutron_star_high": 2.8,
                         "red_giant_8M": 8.0, "red_giant_10M": 10.0, "red_giant_max": 9.0, "black_hole_7M": 7.0 }
    planetary_mass_map = { "pluto": 0.0022, "mercury": 0.055, "venus": 0.815, "earth": 1.0,
                           "mars": 0.107, "jupiter": 317.8, "saturn": 95.2, "uranus": 14.5, "neptune": 17.1,
                           "brown_dwarf": 1.2 }
    if particle in quantum_reference: return 1.0
    if particle == "neutron": return 0.1
    if particle in stellar_mass_map:
        m, min_m, max_m = stellar_mass_map[particle], 0.1, 10.0
    elif particle in planetary_mass_map:
        m, min_m, max_m = planetary_mass_map[particle], 0.0022, 1.2
    else: return 0.01
    log_scale = np.log10(m / min_m + 1e-6) / np.log10(max_m / min_m + 1e-6)
    return 0.1 + log_scale * 0.9

# Plotter
def plot_vectors(reference_dict, title, filename):
    plt.figure(figsize=(10, 10), dpi=200)
    ax = plt.subplot(111, polar=True)
    plt.title(title)

    quadrant_labels = [
        (np.deg2rad(45), 1.1, "MEGA Zone (Μ Ε Γ Α)"),
        (np.deg2rad(135), 1.1, "Genesis Zone (Φ Σ Η Ι)"),
        (np.deg2rad(225), 1.1, "Outer Zone (Α Π Ε Κ)"),
        (np.deg2rad(315), 1.1, "Golden Zone (Φ Τ Ω Π)")
    ]
    for angle, radius, label in quadrant_labels:
        ax.text(angle, radius, label, ha='center', va='center', fontsize=9, color='gray')

    for particle, freq in reference_dict.items():
        theta = quantum_alignment(freq) % (2 * sc.PI)
        magnitude = get_custom_magnitude(particle)
        line = ax.plot([0, theta], [0, magnitude], label=particle.title(), linewidth=2)
        color = line[0].get_color()
        ax.plot(theta, magnitude, 'o', color=color, markersize=6)

    ax.plot([0, np.deg2rad(291.25)], [0, 0.8], label="Golden Axis", linewidth=2, color='gold')
    ax.plot([0, np.deg2rad(90)], [0, 1.0], label="Chi-Rho (ΧΡ)", linestyle='--', color='black')
    ax.text(np.deg2rad(90), 1.05, "χρ = Emergence of Light / Matter", fontsize=8, ha='center', color='black')

    ax.set_theta_zero_location('E')
    ax.set_theta_direction(1)
    ax.legend(bbox_to_anchor=(1.5, 1.05), fontsize=8)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

plot_vectors(quantum_reference, "Quantum Particle Frequencies", "quantum_particles.png")
plot_vectors(planetary_reference, "Planetary Frequencies", "planetary_frequencies.png")
plot_vectors(stellar_reference, "Stellar Mass Frequencies", "stellar_frequencies.png")
plot_vectors(full_reference, "Quantum → Planetary → Stellar: Polar Scalar Overlay", "full_overlay.png")

