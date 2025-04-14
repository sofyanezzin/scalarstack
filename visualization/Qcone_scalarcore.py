import numpy as np
import plotly.graph_objects as go
import scalarcore as sc  # 🔗 Symbolic constants

# Constants
cone_radius = sc.PI
cone_height = sc.PI
sphere_radius = sc.a_H  # ≈ π / √2, Huckstead Scalar

# === Cone Surface ===
theta = np.linspace(0, 2 * sc.PI, 60)
z = np.linspace(0, cone_height, 60)
theta, z = np.meshgrid(theta, z)
r = cone_radius * (1 - z / cone_height)
x_cone = r * np.cos(theta)
y_cone = r * np.sin(theta)
z_cone = cone_height - z  # flip the cone, base at z=0

# === Sphere ===
phi = np.linspace(0, sc.PI, 40)
theta_s = np.linspace(0, 2 * sc.PI, 40)
phi, theta_s = np.meshgrid(phi, theta_s)

x_sphere = sphere_radius * np.sin(phi) * np.cos(theta_s)
y_sphere = sphere_radius * np.sin(phi) * np.sin(theta_s)
z_sphere = sphere_radius * np.cos(phi)
z_sphere += cone_height  # align equator with cone base

# === Plotly Figure ===
fig = go.Figure()

# Add cone surface
fig.add_trace(go.Surface(
    x=x_cone, y=y_cone, z=z_cone,
    colorscale='YlOrBr',
    opacity=0.9,
    showscale=False,
    name='PIne Cone'
))

# Add sphere surface
fig.add_trace(go.Surface(
    x=x_sphere, y=y_sphere, z=z_sphere,
    colorscale='Blues',
    opacity=0.5,
    showscale=False,
    name='Projection Sphere'
))

# Layout
fig.update_layout(
    title='PIne Cone Projection Geometry with Embedded Sphere π⁄√2 = aH',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='data'
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.show()
