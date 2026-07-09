import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def classical_mismatch(theta, phi):
    return 1 - np.cos(theta) ** 2 * np.cos(phi) ** 2 - np.sin(theta) ** 2 * np.sin(phi) ** 2


def quantum_mismatch(theta, phi):
    return np.sin(phi - theta) ** 2


theta_degrees = np.linspace(-90, 90, 181)
phi_degrees = np.linspace(-90, 90, 181)
theta_grid, phi_grid = np.meshgrid(np.radians(theta_degrees), np.radians(phi_degrees))

classical_grid = classical_mismatch(theta_grid, phi_grid)
quantum_grid = quantum_mismatch(theta_grid, phi_grid)

initial_theta = -30
initial_phi = 30

fig = plt.figure(figsize=(12, 7))
grid = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.18])

ax_classical = fig.add_subplot(grid[0:2, 0])
ax_quantum = fig.add_subplot(grid[0:2, 1])
ax_theta_slider = fig.add_subplot(grid[2, 0])
ax_phi_slider = fig.add_subplot(grid[2, 1])

extent = [theta_degrees.min(), theta_degrees.max(), phi_degrees.min(), phi_degrees.max()]

classical_image = ax_classical.imshow(
    classical_grid,
    origin="lower",
    extent=extent,
    vmin=0,
    vmax=1,
    aspect="auto",
    cmap="viridis",
)
quantum_image = ax_quantum.imshow(
    quantum_grid,
    origin="lower",
    extent=extent,
    vmin=0,
    vmax=1,
    aspect="auto",
    cmap="viridis",
)

fig.colorbar(classical_image, ax=ax_classical, label="Mismatch probability")
fig.colorbar(quantum_image, ax=ax_quantum, label="Mismatch probability")

classical_marker = ax_classical.scatter(initial_theta, initial_phi, color="red", s=60)
quantum_marker = ax_quantum.scatter(initial_theta, initial_phi, color="red", s=60)

for ax in (ax_classical, ax_quantum):
    ax.set_xlabel(r"Detector A angle $\theta$ / degrees")
    ax.set_ylabel(r"Detector B angle $\phi$ / degrees")
    ax.grid(color="white", alpha=0.25)

theta_slider = Slider(ax_theta_slider, "theta", -90, 90, valinit=initial_theta, valstep=1)
phi_slider = Slider(ax_phi_slider, "phi", -90, 90, valinit=initial_phi, valstep=1)


def update(_):
    theta_deg = theta_slider.val
    phi_deg = phi_slider.val
    theta = np.radians(theta_deg)
    phi = np.radians(phi_deg)

    classical_value = classical_mismatch(theta, phi)
    quantum_value = quantum_mismatch(theta, phi)

    classical_marker.set_offsets([[theta_deg, phi_deg]])
    quantum_marker.set_offsets([[theta_deg, phi_deg]])
    ax_classical.set_title(f"Classical mismatch = {classical_value:.3f}")
    ax_quantum.set_title(f"Quantum mismatch = {quantum_value:.3f}")
    fig.canvas.draw_idle()


theta_slider.on_changed(update)
phi_slider.on_changed(update)
update(None)

plt.tight_layout()
plt.show()
