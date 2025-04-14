# Quantum Vector Angular Mapping — Scalarcore Edition
import numpy as np
import matplotlib.pyplot as plt
import csv
import scalarcore as sc  # 🔗 Scalar constants and alignment functions

# Scalar-symbolic alignment base
alignment_base = 707.10678

# Angular projection function
def quantum_alignment(frequency):
    return (frequency / alignment_base) * (sc.SQRT2 / sc.PI)

# Reference frequencies
quantum_reference = {
    "photon": 282.24,
    "electron": 306.19,
    "neutron": 313.08,
    "proton": 323.91,
    "muon": 349.58,
    "tau": 377.96
}

stellar_reference = {
    "white_dwarf": 44.1,
    "neutron_star": 57.77,
    "red_giant": 76.08,
    "main_sequence": 33.11
}

planetary_reference = {
    "earth": 7.83,
    "venus": 9.78,
    "mars": 14.1,
    "jupiter": 21.7,
    "saturn": 26.7
}

full_reference = {**quantum_reference, **stellar_reference, **planetary_reference}

color_map = {
    "quantum": "cyan",
    "stellar": "orange",
    "planetary": "green"
}

def get_custom_magnitude(particle):
    if particle in quantum_reference:
        return 1.0
    elif particle in stellar_reference:
        return 0.7
    elif particle in planetary_reference:
        return 0.4
    return 0.5

def plot_vectors(ref_dict, label, savefig=False):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlim(0, 1.2)
    ax.set_rticks([])
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.set_title(f"{label} Zone Harmonics", va='bottom', fontsize=14)

    for angle, qlabel in [(0, "MEGA"), (sc.PI/2, "Genesis"), (sc.PI, "Outer"), (3*sc.PI/2, "Golden")]:
        ax.axvline(angle, linestyle=':', color='black', linewidth=0.8)
        ax.text(angle, 1.05, qlabel, fontsize=10, ha='center', va='bottom')

    ax.axvline(sc.PI/2, color='red', linestyle='-', linewidth=1.5)
    ax.text(sc.PI/2, 1.12, r"$\chi\rho$ = Fundamental Crosspoint", color='red', fontsize=9, ha='center', va='bottom')

    ax.plot(np.linspace(0, 2*sc.PI, 500), [0.1]*500, linestyle='--', color='gray', linewidth=0.5, alpha=0.4)
    ax.text(np.deg2rad(10), 1.15, r"$\theta = \frac{f}{a_H \times 2} \cdot \frac{\sqrt{2}}{\pi}$", fontsize=8)

    gold_theta = np.deg2rad(291.25)
    ax.axvline(gold_theta, color='gold', linestyle='--', linewidth=1.2)
    ax.text(gold_theta, 1.05, "Gold Ref", fontsize=9, color='gold', ha='center')

    for particle, freq in ref_dict.items():
        theta = quantum_alignment(freq)
        r = get_custom_magnitude(particle)
        color = (
            color_map["quantum"] if particle in quantum_reference else
            color_map["stellar"] if particle in stellar_reference else
            color_map["planetary"]
        )
        ax.plot(theta, r, 'o', label=particle, color=color)
        ax.text(theta, r + 0.05, particle, fontsize=8, ha='center')

    ax.legend(bbox_to_anchor=(1.1, 1.05))
    if savefig:
        plt.savefig(f"{label.replace(' ', '_')}_Harmonics_Polar.png", dpi=300, bbox_inches='tight')
    plt.show()

plot_vectors(full_reference, "Full Overlay", savefig=True)
plot_vectors(quantum_reference, "Quantum", savefig=True)
plot_vectors(stellar_reference, "Stellar", savefig=True)
plot_vectors(planetary_reference, "Planetary", savefig=True)

with open("vector_angles.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Particle", "Theta (deg)", "Magnitude"])
    for particle, freq in full_reference.items():
        theta = np.degrees(quantum_alignment(freq) % (2 * sc.PI))
        magnitude = get_custom_magnitude(particle)
        writer.writerow([particle, round(theta, 2), round(magnitude, 3)])

