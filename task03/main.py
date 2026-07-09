import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34
c = 2.99792458e8
k = 1.380649e-23
R = 8.314462618

# Planck black-body radiation spectrum
wavelength = np.linspace(100e-9, 3000e-9, 1000)
temperatures = [3000, 4000, 5000, 6000]

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)

for T in temperatures:
    B = (2 * h * c**2 / wavelength**5) / (np.exp(h * c / (wavelength * k * T)) - 1)
    plt.plot(wavelength * 1e9, B, label=f"{T} K")

plt.grid(True)
plt.xlabel("Wavelength / nm")
plt.ylabel("Spectral radiance")
plt.title("Planck black-body spectrum")
plt.legend()

# Einstein model of molar heat capacity of solids
T = np.linspace(1, 1000, 1000)

# Approximate characteristic temperatures in K
crystals = {
    "Gold": 170,
    "Copper": 240,
    "Iron": 470,
}

plt.subplot(1, 2, 2)

for crystal, theta_E in crystals.items():
    x = theta_E / T
    exp_minus_x = np.exp(-x)
    C = 3 * R * x**2 * exp_minus_x / (1 - exp_minus_x) ** 2
    plt.plot(T, C, label=crystal)

plt.axhline(3 * R, color="black", linestyle="--", label="Dulong-Petit limit")
plt.grid(True)
plt.xlabel("Temperature / K")
plt.ylabel("Molar heat capacity / J mol$^{-1}$ K$^{-1}$")
plt.title("Einstein heat capacity model")
plt.legend()

plt.tight_layout()
plt.show()
