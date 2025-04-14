# 🌍 Planetary Spin Tilt vs Mass Visualization (Scalar-Aligned)
import matplotlib.pyplot as plt
import numpy as np
import scalarcore as sc  # 🔗 Scalar constants and utilities

# Planetary Data: mass in Earth-mass units, axial tilt in degrees
planet_data = {
    "Mercury": {"mass": 0.055, "tilt": 0.03},
    "Venus": {"mass": 0.815, "tilt": 177.4},
    "Earth": {"mass": 1.0, "tilt": 23.44},
    "Mars": {"mass": 0.107, "tilt": 25.19},
    "Jupiter": {"mass": 317.8, "tilt": 3.13},
    "Saturn": {"mass": 95.2, "tilt": 26.73},
    "Uranus": {"mass": 14.5, "tilt": 97.77},
    "Neptune": {"mass": 17.1, "tilt": 28.32},
    "Pluto": {"mass": 0.0022, "tilt": 57.47}
}

# Extract data
names = list(planet_data.keys())
masses = [planet_data[name]["mass"] for name in names]
tilts = [planet_data[name]["tilt"] for name in names]

# Normalize tilt for radial interpretation (0 to 180# Normalize tilt for radial interpretation (0 to 180\ub0 → 0 to π radians)
tilts_rad = np.deg2rad(tilts)

# Approximate planetary angular momentum = mass × sin(tilt)
angular_momentum_scale = [
    planet_data[name]['mass'] * np.sin(np.deg2rad(planet_data[name]['tilt']))
    for name in names
]

# Normalize to max for visual scaling
max_am = max(angular_momentum_scale)
am_scaled = [am / max_am for am in angular_momentum_scale]

# Optional: check for scalar resonance
resonant_labels = [
    f"{name}*" if sc.is_resonant_scalar(am) else name
    for name, am in zip(names, angular_momentum_scale)
]

# Plot polar tilt chart
plt.figure(figsize=(8, 8), dpi=150)
ax = plt.subplot(111, polar=True)
plt.title("Planetary Axial Tilt Scaled by Angular Momentum (Scalar Projection)")

# Plot each planet as a vector from center to tilt angle with radius based on log-mass
for i, name in enumerate(names):
    theta = tilts_rad[i]
    r = am_scaled[i]
    label = resonant_labels[i]
    ax.plot([0, theta], [0, r], label=label, linewidth=2)
    ax.plot(theta, r, 'o')

ax.set_theta_zero_location('N')
ax.set_theta_direction(1)
ax.set_rlabel_position(225)
ax.set_rticks([])
ax.legend(bbox_to_anchor=(1.25, 1.05))
plt.tight_layout()
plt.show()

