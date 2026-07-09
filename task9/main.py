import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34
c = 2.99792458e8
m_e = 9.1093837015e-31

# A typical X-ray wavelength for Compton scattering
initial_wavelength = 0.071e-9
compton_wavelength = h / (m_e * c)

theta = np.linspace(0, np.pi, 500)
theta_degrees = np.degrees(theta)

# Compton wavelength shift
wavelength_shift = compton_wavelength * (1 - np.cos(theta))
scattered_wavelength = initial_wavelength + wavelength_shift
fractional_shift = wavelength_shift / initial_wavelength

# Photon energies before and after scattering
initial_energy = h * c / initial_wavelength
scattered_energy = h * c / scattered_wavelength
electron_kinetic_energy = initial_energy - scattered_energy

# Relativistic recoil speed from kinetic energy = (gamma - 1) m c^2
gamma = 1 + electron_kinetic_energy / (m_e * c**2)
recoil_speed = c * np.sqrt(1 - 1 / gamma**2)

# Recoil angle follows from momentum conservation in x and y directions.
initial_photon_momentum = h / initial_wavelength
scattered_photon_momentum = h / scattered_wavelength
electron_px = initial_photon_momentum - scattered_photon_momentum * np.cos(theta)
electron_py = scattered_photon_momentum * np.sin(theta)
recoil_angle = np.degrees(np.arctan2(electron_py, electron_px))
recoil_angle[0] = np.nan

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(theta_degrees, fractional_shift)
axes[0].grid(True)
axes[0].set_xlabel(r"Photon scattering angle $\theta$ / degrees")
axes[0].set_ylabel(r"Fractional shift $\Delta\lambda/\lambda$")
axes[0].set_title("Compton wavelength shift")

axes[1].plot(theta_degrees, recoil_speed / c)
axes[1].grid(True)
axes[1].set_xlabel(r"Photon scattering angle $\theta$ / degrees")
axes[1].set_ylabel(r"Electron recoil speed $v/c$")
axes[1].set_title("Electron recoil speed")

axes[2].plot(theta_degrees, recoil_angle)
axes[2].grid(True)
axes[2].set_xlabel(r"Photon scattering angle $\theta$ / degrees")
axes[2].set_ylabel(r"Electron recoil angle $\phi$ / degrees")
axes[2].set_title("Electron recoil angle")

plt.tight_layout()
plt.show()
