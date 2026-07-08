import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34
c = 2.99792458e8
e = 1.602176634e-19

# Bohr model energy constant for hydrogen
E0 = 13.6

max_n = 8
series_names = {
    1: "Lyman",
    2: "Balmer",
    3: "Paschen",
    4: "Brackett",
    5: "Pfund",
}

for n_final in range(1, max_n):
    wavelengths = []
    photon_energies = []
    labels = []

    for n_initial in range(n_final + 1, max_n + 1):
        energy = E0 * (1 / n_final**2 - 1 / n_initial**2)
        wavelength = h * c / (energy * e)

        wavelengths.append(wavelength * 1e9)
        photon_energies.append(energy)
        labels.append(f"{n_initial} to {n_final}")

    if wavelengths:
        plt.scatter(wavelengths, photon_energies, label=series_names.get(n_final, f"n={n_final}"))

        for wavelength, energy, label in zip(wavelengths, photon_energies, labels):
            plt.text(wavelength, energy, label, fontsize=7)

plt.grid(True)
plt.xlabel("Wavelength / nm")
plt.ylabel("Photon energy / eV")
plt.title("Hydrogen emission spectrum")
plt.legend()
plt.show()
