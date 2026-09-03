import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(6, 6))
earth = ax.scatter(0, 0, s=1500, color='#1f77b4', edgecolors='#4a90e2', label='Earth')
asteroid, = ax.plot([], [], marker='p', color='#8c8c8c', markersize=12, linestyle='None', label='Asteroid')


def init():
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    return asteroid, earth,

def update(frame):
    xdata = [frame]
    ydata = [np.sin(frame)]
    asteroid.set_data(xdata, ydata)
    return asteroid, earth,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()