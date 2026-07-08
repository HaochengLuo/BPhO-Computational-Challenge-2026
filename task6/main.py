import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Physical constants
h = 6.62607015e-34
m_e = 9.1093837015e-31
e = 1.602176634e-19

# Graphite layer spacings and diffraction tube radius
d_values = {
    "d = 0.123 nm": 0.123e-9,
    "d = 0.213 nm": 0.213e-9,
}
tube_radius = 65e-3

# Accelerating voltage
V = np.linspace(1000, 5000, 200)

plt.figure(figsize=(12, 5))

# Model electron diffraction ring radius as voltage changes
plt.subplot(1, 2, 1)

for label, d in d_values.items():
    wavelength = h / np.sqrt(2 * m_e * e * V)
    phi = np.arcsin(wavelength / (2 * d))
    ring_radius = tube_radius * np.sin(2 * phi)
    plt.plot(V / 1000, ring_radius * 1000, label=label)

plt.grid(True)
plt.xlabel("Accelerating voltage / kV")
plt.ylabel("Ring radius / mm")
plt.title("Electron diffraction ring radius")
plt.legend()

# Draw diffraction rings for one selected voltage
plt.subplot(1, 2, 2)
selected_V = 3000
screen_radius = tube_radius * 1000

for label, d in d_values.items():
    wavelength = h / np.sqrt(2 * m_e * e * selected_V)
    phi = np.arcsin(wavelength / (2 * d))
    ring_radius = tube_radius * np.sin(2 * phi) * 1000
    ring = Circle((0, 0), ring_radius, fill=False, label=label)
    plt.gca().add_patch(ring)

screen = Circle((0, 0), screen_radius, fill=False, linestyle="--", color="black")
plt.gca().add_patch(screen)
plt.scatter(0, 0, color="black", s=10)
plt.xlim(-screen_radius, screen_radius)
plt.ylim(-screen_radius, screen_radius)
plt.gca().set_aspect("equal")
plt.grid(True)
plt.xlabel("x / mm")
plt.ylabel("y / mm")
plt.title(f"Electron diffraction rings at {selected_V / 1000:.1f} kV")
plt.legend()

plt.tight_layout()
plt.show()

# Straight-line check: 1/V is proportional to (2 sin phi)^2
plt.figure()

for label, d in d_values.items():
    wavelength = h / np.sqrt(2 * m_e * e * V)
    phi = np.arcsin(wavelength / (2 * d))
    x = (2 * np.sin(phi)) ** 2
    y = 1 / V
    plt.plot(x, y, label=label)

plt.grid(True)
plt.xlabel("$(2\\sin\\phi)^2$")
plt.ylabel("$1 / V$ / V$^{-1}$")
plt.title("Electron diffraction straight-line check")
plt.legend()
plt.show()
