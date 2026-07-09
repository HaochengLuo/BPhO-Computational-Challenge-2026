import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34
hbar = h / (2 * np.pi)
m_e = 9.1093837015e-31
e = 1.602176634e-19

# Width of the one-dimensional infinite square well
a = 1.0e-9


def energy(n):
    return n**2 * np.pi**2 * hbar**2 / (2 * m_e * a**2)


def probability_density(n, x):
    return (2 / a) * np.sin(n * np.pi * x / a) ** 2


n_values = np.arange(1, 9)
energies_ev = energy(n_values) / e

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Energy levels grow as n^2 for a particle in a box.
axes[0].plot(n_values, energies_ev, marker="o")
axes[0].grid(True)
axes[0].set_xlabel("Quantum number n")
axes[0].set_ylabel("Energy / eV")
axes[0].set_title("Energy levels")

# Probability density is zero at the walls and has n antinodes.
x = np.linspace(0, a, 1000)
x_nm = x * 1e9

for n in range(1, 5):
    density_per_nm = probability_density(n, x) * 1e-9
    axes[1].plot(x_nm, density_per_nm, label=f"n = {n}")

axes[1].grid(True)
axes[1].set_xlabel("Position x / nm")
axes[1].set_ylabel(r"$|\psi_n(x)|^2$ / nm$^{-1}$")
axes[1].set_title("Probability densities")
axes[1].legend()

# Extension check: every stationary state satisfies Delta x Delta p >= hbar / 2.
delta_x = a * np.sqrt(1 / 12 - 1 / (2 * n_values**2 * np.pi**2))
delta_p = n_values * np.pi * hbar / a
uncertainty_ratio = delta_x * delta_p / hbar

axes[2].plot(n_values, uncertainty_ratio, marker="o", label=r"$\Delta x\Delta p/\hbar$")
axes[2].axhline(0.5, color="black", linestyle="--", label="Heisenberg limit")
axes[2].grid(True)
axes[2].set_xlabel("Quantum number n")
axes[2].set_ylabel(r"$\Delta x\Delta p/\hbar$")
axes[2].set_title("Uncertainty principle check")
axes[2].legend()

plt.tight_layout()
plt.show()
