import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34
e = 1.602176634e-19

# Work functions in eV
metals = {
    "Caesium": 2.14,
    "Sodium": 2.28,
    "Zinc": 4.31,
    "Copper": 4.70,
    "Platinum": 6.35,
}

frequency = np.linspace(2e14, 2e15, 1000)

for metal, work_function in metals.items():
    stopping_voltage = h * frequency / e - work_function
    stopping_voltage = np.maximum(stopping_voltage, 0)
    plt.plot(frequency / 1e14, stopping_voltage, label=metal)

plt.grid(True)
plt.xlabel("Frequency / $10^{14}$ Hz")
plt.ylabel("Stopping voltage / V")
plt.title("Photoelectric effect")
plt.legend()
plt.show()
