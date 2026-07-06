import numpy as np
import matplotlib.pyplot as plt

# Number of steps and step size
N = 500
s = 1

# Random direction for each step
theta = np.random.uniform(0, 2 * np.pi, N)

# Components of each step
dx = s * np.cos(theta)
dy = s * np.sin(theta)

# Position after each step
x = np.concatenate(([0], np.cumsum(dx)))
y = np.concatenate(([0], np.cumsum(dy)))

# Plot random walk
plt.plot(x, y)
plt.scatter(x[0], y[0], color="green", label="Start")
plt.scatter(x[-1], y[-1], color="red", label="End")
plt.grid(True)
plt.axis("equal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Random walk")
plt.legend()
plt.show()
