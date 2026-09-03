import math

from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
import os
import tempfile


class AsteroidStatus(Enum):
    HIT = "HIT"
    MISS = "MISS"
    LOST = "LOST"
    STABLE = "STABLE"
    BURNED = "BURNED"


class MockAsteroidEngine:
    def __init__(self, radius,speed, initial_distance, angle=0,):
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.initial_distance = initial_distance

        self.closest_aproach_dist = None

        #constants
        self.GRAVITY = 6.674e-11
        self.EARTH_MASS = 5.972e24
        self.EARTH_RADIUS = 6.371e6
        self.EARTH_x = 0
        self.EARTH_y = 0
        self.AVERAGE_DENSITY = 3000  #3,000 kg/m^3
    

    def calculate_path(self):
        #math for trajectory
        """
        1) Find volume (assume spherical): V = 4/3pir^3
        2) Find mass: volume x density
        3) Trig to split inital speed and angle into horizontal and vertical speeds:
           * vx = v* cos(theta)
           * vy = V * sin(theta)
        4) Set initial starting conditions (position of asteroid and time(dt))
        5) While loop:
           * Distance: r = sqrt(x^2 + y^2)
           * acceleration = (G * M)/ r^2  --> M is earth's mass
           * accerlation_x = -accerlaton * (x/r)
           * accerleration_y = -accerlation * (y/r)
           * Update velocity:
                - vx += acceleration_x * (dt)
                - vy += acceleration_y * dt
                - x += vx * dt
                - y += vy * dt
        6) Check hit or msiss: 
            * Hit: if r <= Earth Radius, break loop
            * Miss: If x passes Earth and vx > 0 (moving away) OR r begins growing drastically larger than starting distance
            
        """
        #trig        
        vx = self.speed * math.cos(math.radians(self.angle))
        vy = self.speed * math.sin(math.radians(self.angle))

        #picked these numbers so the asteroid is around 10 Earth Radii away
        asteroid_x = -self.initial_distance #meters
        asteroid_y = 0 #meters
        
        dt = 10 #updates every 10 second

        min_approach_dist = float("inf")
        initial_distance = math.sqrt(asteroid_x**2 + asteroid_y**2)

        running = True
        steps = 0
        max_steps = 5000
       
        while running:
            steps += 1
            r = math.sqrt(asteroid_x**2 + asteroid_y**2)

            if r > self.EARTH_RADIUS * 5:
                dt = 30.0 
            elif r > self.EARTH_RADIUS * 1.5:
                dt = 5.0   
            else:
                dt = 0.1   

            accerlation = (self.GRAVITY * self.EARTH_MASS) / (r**2)
            accerlation_x = -accerlation * (asteroid_x/r)
            accerlation_y = -accerlation * (asteroid_y/r) #look into why -accerlation

            vx += accerlation_x * dt
            vy += accerlation_y * dt
            asteroid_x += vx * dt
            asteroid_y += vy * dt

            r = math.sqrt(asteroid_x**2 + asteroid_y**2)
            if r < min_approach_dist:
                min_approach_dist = r

            #vector dot product 
            # < 0 -> asteroid moves towards Earth
            # =0: Perpendicular to Earth
            # > 0 --> moving away from Earth
            moving_away = (asteroid_x * vx + asteroid_y * vy) > 0

            if r <= self.EARTH_RADIUS + self.radius:
                self.closest_aproach_dist = round(min_approach_dist, 2)
                if self.radius < 25:
                    return AsteroidStatus.BURNED
                else:
                    return AsteroidStatus.HIT
            elif moving_away and r > self.EARTH_RADIUS * 3:
                if min_approach_dist < initial_distance:
                    self.closest_aproach_dist = round(min_approach_dist, 2)
                    return AsteroidStatus.MISS
                else:
                    return AsteroidStatus.LOST
                            
            if steps >= max_steps:
                return AsteroidStatus.STABLE

    def calculate_potential_energy(self):

        #Equations:
        # Mass (m) = (4/3 * pi * (diameter(in meters)/2)^3)
        # Energy in Megatons =  (.5 * m * v(m/s)^2)/(4.184 * 10^15)

        mass = ((4/3) * math.pi * (self.radius)**3) * self.AVERAGE_DENSITY


        energy_megatons = (.5 * mass * self.speed**2)/(4.184 * 10**15)

        return round(energy_megatons, 2)

    def animate(self): 
        self.vx = self.speed * math.cos(math.radians(self.angle)) 
        self.vy = self.speed * math.sin(math.radians(self.angle)) 
        self.asteroid_x = -self.initial_distance #meters 
        self.asteroid_y = 0 #meters 
        dt = 200 
        self.min_approach_dist = float("inf") 
        self.initial_distancev2 = math.sqrt(self.asteroid_x**2 + self.asteroid_y**2) 
        
        fig, ax = plt.subplots(figsize=(6, 6)) 
        fig.patch.set_facecolor('black') 
        ax.set_facecolor('black') 
        
        earth = ax.scatter(0, 0, s=1500, color='#1f77b4', edgecolors='#4a90e2', label='Earth') 
        asteroid, = ax.plot([], [], marker='p', color='#8c8c8c', markersize=12, linestyle='None', label='Asteroid') 
        status_text = ax.text(0.01, 0.90, ' ' * 50, transform=ax.transAxes, color='red', fontsize=12, weight='bold') 
        status_text_speed = ax.text(0.01, 0.75, ' ' * 50, transform=ax.transAxes, color='blue', fontsize=12, weight='bold') 
        x_history, y_history = [], [] 
        trail, = ax.plot([], [], "w-", alpha=0.3) 
        self.end_frame = None 

        def init(): 
            ax.set_xlim(-12, 12) 
            ax.set_xlim(-12, 12) 
            ax.set_ylim(-12, 12) 
            return asteroid, earth, trail, status_text, status_text_speed, 

        def update(frame): 
            # FIX: Do not raise StopIteration. Just keep returning the elements without updating position.
            if self.end_frame is not None and frame >= self.end_frame: 
                return asteroid, earth, trail, status_text, status_text_speed, 
                
            if self.end_frame is None: 
                r = math.sqrt(self.asteroid_x**2 + self.asteroid_y**2) 
                accerlation = (self.GRAVITY * self.EARTH_MASS) / (r**2) 
                accerlation_x = -accerlation * (self.asteroid_x/r) 
                accerlation_y = -accerlation * (self.asteroid_y/r) 
                self.vx += accerlation_x * dt 
                self.vy += accerlation_y * dt 
                self.asteroid_x += self.vx * dt 
                self.asteroid_y += self.vy * dt 
                r = math.sqrt(self.asteroid_x**2 + self.asteroid_y**2) 
                if r < self.min_approach_dist: 
                    self.min_approach_dist = r 
                plot_x = self.asteroid_x / self.EARTH_RADIUS 
                plot_y = self.asteroid_y / self.EARTH_RADIUS 
                x_history.append(plot_x) 
                y_history.append(plot_y) 
                asteroid.set_data([plot_x], [plot_y]) 
                trail.set_data(x_history, y_history) 
                status_text_speed.set_text(f"Velocity: {round(math.sqrt(self.vx**2 + self.vy**2), 2)} (m/s)") 
                
                if (abs(plot_x) > 12 or abs(plot_y) > 12) and self.end_frame is None: 
                    if self.min_approach_dist < self.initial_distancev2: 
                        status_text.set_text("ASTEROID MISSES EARTH!") 
                    else: 
                        status_text.set_text("ASTEROID IS LOST") 
                    status_text_speed.set_text(f"Final velocity: {round(math.sqrt(self.vx**2 + self.vy**2), 2)} (m/s)") 
                    self.end_frame = frame + 30 
                    
                if r <= self.EARTH_RADIUS and self.end_frame is None: 
                    if self.radius < 25: 
                        status_text.set_text("ASTEROID BURNS UP IN EARTH'S ATMOSPHERE") 
                    else: 
                        status_text.set_text("ASTEROID HITS EARTH!") 
                    status_text_speed.set_text(f"Final velocity: {round(math.sqrt(self.vx**2 + self.vy**2), 2)} (m/s)") 
                    self.end_frame = frame + 30 
            else: 
                plot_x = self.asteroid_x / self.EARTH_RADIUS 
                plot_y = self.asteroid_y / self.EARTH_RADIUS 
                
            return asteroid, earth, trail, status_text, status_text_speed, 

        self.ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=False, interval=30, cache_frame_data=False) 
        
        # Safe multi-frame file handling
        gif_buffer = io.BytesIO() 
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
            tmp_path = tmpfile.name

        try:
            self.ani.save(tmp_path, writer="pillow", fps=30, metadata={"loop": 0})
            with open(tmp_path, "rb") as f:
                gif_buffer.write(f.read())
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        plt.close(fig) 
        gif_buffer.seek(0) 
        return gif_buffer


