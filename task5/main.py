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

fig, ax = plt.subplots()
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

for series_number, n_final in enumerate(series_names):
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
        color = colors[series_number % len(colors)]
        wavelengths = np.array(wavelengths)
        photon_energies = np.array(photon_energies)
        series_limit_energy = E0 / n_final**2
        series_limit_wavelength = h * c / (series_limit_energy * e) * 1e9

        ax.axvspan(series_limit_wavelength, wavelengths.max(), color=color, alpha=0.15)
        ax.scatter(wavelengths, photon_energies, color=color, label=series_names[n_final], zorder=3)

        band_middle = np.sqrt(series_limit_wavelength * wavelengths.max())
        ax.text(
            band_middle,
            photon_energies.max() * 1.03,
            series_names[n_final],
            color=color,
            fontsize=9,
            ha="center",
            weight="bold",
        )

        ax.annotate(
            labels[0],
            (wavelengths[0], photon_energies[0]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=7,
            color=color,
        )
        ax.annotate(
            labels[-1],
            (wavelengths[-1], photon_energies[-1]),
            textcoords="offset points",
            xytext=(5, -10),
            fontsize=7,
            color=color,
        )

ax.set_xscale("log")
ax.grid(True, which="both")
ax.set_xlabel("Wavelength / nm")
ax.set_ylabel("Photon energy / eV")
ax.set_title("Hydrogen emission spectrum")
ax.legend()
plt.show()
