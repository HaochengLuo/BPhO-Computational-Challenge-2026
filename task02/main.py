import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Small particles
N = 120
m = 1
r = 0.04
step_size = 0.15

# Large particle
M = 80
R = 0.35

# Simulation settings
box_size = 10
frames = 600

large_pos = np.array([box_size / 2, box_size / 2], dtype=float)
large_vel = np.array([0.0, 0.0])
large_path_x = [large_pos[0]]
large_path_y = [large_pos[1]]
small_pos = np.random.uniform(r, box_size - r, (N, 2))

for i in range(N):
    while np.linalg.norm(small_pos[i] - large_pos) < r + R:
        small_pos[i] = np.random.uniform(r, box_size - r, 2)


def reflect_from_walls(position, velocity, radius):
    for axis in range(2):
        if position[axis] < radius:
            position[axis] = radius
            velocity[axis] *= -1
        elif position[axis] > box_size - radius:
            position[axis] = box_size - radius
            velocity[axis] *= -1


def update(frame):
    global small_pos, large_pos, large_vel

    # Random walk for the small particles
    theta = np.random.uniform(0, 2 * np.pi, N)
    small_vel = step_size * np.column_stack((np.cos(theta), np.sin(theta)))
    small_pos += small_vel

    for i in range(N):
        reflect_from_walls(small_pos[i], small_vel[i], r)

    # Motion of the large particle
    large_pos += large_vel
    reflect_from_walls(large_pos, large_vel, R)

    # Collisions between small particles and the large particle
    for i in range(N):
        separation = small_pos[i] - large_pos
        distance = np.linalg.norm(separation)

        if distance < r + R:
            if distance == 0:
                normal = np.array([1.0, 0.0])
            else:
                normal = separation / distance
            relative_velocity = small_vel[i] - large_vel
            speed_along_normal = np.dot(relative_velocity, normal)

            if speed_along_normal < 0:
                impulse = -2 * speed_along_normal / (1 / m + 1 / M)
                small_vel[i] += (impulse / m) * normal
                large_vel -= (impulse / M) * normal

            small_pos[i] = large_pos + normal * (r + R)

    particles.set_offsets(small_pos)
    large_circle.center = large_pos
    large_path_x.append(large_pos[0])
    large_path_y.append(large_pos[1])
    path_line.set_data(large_path_x, large_path_y)
    return particles, large_circle, path_line


fig, ax = plt.subplots()
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Brownian motion")

particles = ax.scatter(small_pos[:, 0], small_pos[:, 1], s=10)
path_line, = ax.plot(large_path_x, large_path_y, color="red", linewidth=0.8)
large_circle = Circle(large_pos, R, color="orange")
ax.add_patch(large_circle)

animation = FuncAnimation(fig, update, frames=frames, interval=20, blit=True)
plt.show()
