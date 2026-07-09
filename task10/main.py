import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial, genlaguerre

try:
    from scipy.special import sph_harm_y

    def complex_spherical_harmonic(l, m, theta, phi):
        return sph_harm_y(l, m, theta, phi)

except ImportError:
    from scipy.special import sph_harm

    def complex_spherical_harmonic(l, m, theta, phi):
        return sph_harm(m, l, phi, theta)


# Bohr radius
a0 = 5.29177210903e-11


def radial_wavefunction(n, l, r, Z=1):
    rho = 2 * Z * r / (n * a0)
    normalisation = np.sqrt(
        (2 * Z / (n * a0)) ** 3
        * factorial(n - l - 1)
        / (2 * n * factorial(n + l))
    )
    laguerre = genlaguerre(n - l - 1, 2 * l + 1)(rho)
    return normalisation * np.exp(-rho / 2) * rho**l * laguerre


def real_spherical_harmonic(l, m, theta, phi):
    if m == 0:
        return complex_spherical_harmonic(l, 0, theta, phi).real

    if m > 0:
        return np.sqrt(2) * (-1) ** m * complex_spherical_harmonic(l, m, theta, phi).real

    return np.sqrt(2) * (-1) ** abs(m) * complex_spherical_harmonic(l, abs(m), theta, phi).imag


def probability_density(n, l, m, x, y, z, Z=1):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.zeros_like(r)
    nonzero = r > 0
    theta[nonzero] = np.arccos(z[nonzero] / r[nonzero])
    phi = np.arctan2(y, x)

    psi = radial_wavefunction(n, l, r, Z) * real_spherical_harmonic(l, m, theta, phi)
    return np.abs(psi) ** 2


def normalised_density(n, l, m, x, y, z):
    density = probability_density(n, l, m, x, y, z)
    return density / density.max()


# 2D z = 0 slices for representative S, P and D orbitals.
slice_limit_angstrom = 16
grid_points = 350
axis_angstrom = np.linspace(-slice_limit_angstrom, slice_limit_angstrom, grid_points)
axis_m = axis_angstrom * 1e-10
X, Y = np.meshgrid(axis_m, axis_m)
Z0 = np.zeros_like(X)

orbitals_2d = [
    (1, 0, 0, "1s"),
    (2, 1, 1, "2p x-like"),
    (3, 2, -2, "3d xy-like"),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (n, l, m, label) in zip(axes, orbitals_2d):
    density = normalised_density(n, l, m, X, Y, Z0)
    masked_density = np.ma.masked_less(density, 0.02)

    image = ax.imshow(
        masked_density,
        extent=[-slice_limit_angstrom, slice_limit_angstrom, -slice_limit_angstrom, slice_limit_angstrom],
        origin="lower",
        cmap="magma",
        vmin=0,
        vmax=1,
    )
    ax.contour(axis_angstrom, axis_angstrom, density, levels=[0.15], colors="cyan", linewidths=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel("x / Angstrom")
    ax.set_ylabel("y / Angstrom")
    ax.set_title(f"{label}: z = 0 slice")
    fig.colorbar(image, ax=ax, label=r"$|\psi|^2 / |\psi|^2_{max}$")

plt.tight_layout()

# 3D visualization for one chosen orbital.
n3, l3, m3 = 3, 2, 0
volume_limit_angstrom = 18
volume_points = 55
volume_axis_angstrom = np.linspace(-volume_limit_angstrom, volume_limit_angstrom, volume_points)
volume_axis_m = volume_axis_angstrom * 1e-10
X3, Y3, Z3 = np.meshgrid(volume_axis_m, volume_axis_m, volume_axis_m, indexing="ij")
density_3d = normalised_density(n3, l3, m3, X3, Y3, Z3)

# Keep only the denser part of the orbital, similar to an isodensity surface.
mask = density_3d > 0.08
points = np.column_stack((X3[mask], Y3[mask], Z3[mask])) / 1e-10
values = density_3d[mask]

if len(values) > 8000:
    strongest = np.argsort(values)[-8000:]
    points = points[strongest]
    values = values[strongest]

fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection="3d")
scatter = ax.scatter(
    points[:, 0],
    points[:, 1],
    points[:, 2],
    c=values,
    cmap="magma",
    s=8,
    alpha=0.45,
    edgecolors="none",
)

ax.set_xlabel("x / Angstrom")
ax.set_ylabel("y / Angstrom")
ax.set_zlabel("z / Angstrom")
ax.set_title(r"3d $z^2$-like orbital: high-density points")
ax.set_box_aspect((1, 1, 1))
fig.colorbar(scatter, ax=ax, label=r"$|\psi|^2 / |\psi|^2_{max}$")

plt.tight_layout()
plt.show()
