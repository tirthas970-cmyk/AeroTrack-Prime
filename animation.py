import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Setup space background
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Set space boundaries
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.axis('off')

# Draw Earth (stationary blue circle in the center)
earth = ax.scatter(0, 0, s=1500, color='#1f77b4', edgecolors='#4a90e2', label='Earth')

# Initialize asteroid (gray, rough-edged marker)
asteroid, = ax.plot([], [], marker='p', color='#8c8c8c', markersize=12, linestyle='None', label='Asteroid')

# Generate asteroid trajectory (flyby path)
frames = 60
x_path = np.linspace(-5, 5, frames)
y_path = 0.5 * (x_path**2) - 3  # Parabolic flyby trajectory

# Update function for the animation
def update(frame):
    asteroid.set_data([x_path[frame]], [y_path[frame]])
    return asteroid,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

# Save the space animation as a GIF
writer = animation.PillowWriter(fps=20)
ani.save('asteroid_flyby.gif', writer=writer)
