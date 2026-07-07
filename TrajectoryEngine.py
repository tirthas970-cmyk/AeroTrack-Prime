import math

class MockAsteroidEngine:
    def __init__(self, radius,speed, angle=0):
        self.radius = radius
        self.angle = angle
        self.speed = speed

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

        volume = (4/3) * (math.pi) * self.radius**3
        mass = volume * self.AVERAGE_DENSITY #maybe need later

        #trig        
        vx = self.speed * math.cos(math.radians(self.angle))
        vy = self.speed * math.sin(math.radians(self.angle))

        #picked these numbers so the asteroid is around 10 Earth Radii away
        asteroid_x = -70000000 #meters 
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

            if r < min_approach_dist:
                min_approach_dist = r

            accerlation = (self.GRAVITY * self.EARTH_MASS) / (r**2)
            accerlation_x = -accerlation * (asteroid_x/r)
            accerlation_y = -accerlation * (asteroid_y/r) #look into why -accerlation

            vx += accerlation_x * dt
            vy += accerlation_y * dt
            asteroid_x += vx * dt
            asteroid_y += vy * dt

            #vector dot product 
            # < 0 -> asteroid moves towards Earth
            # =0: Perpendicular to Earth
            # > 0 --> moving away from Earth
            moving_away = (asteroid_x * vx + asteroid_y * vy) > 0

            if r <= self.EARTH_RADIUS:
                self.closest_aproach_dist = round(min_approach_dist, 2)
                return "hit"
            elif moving_away and r > self.EARTH_RADIUS * 3:
                if min_approach_dist < initial_distance:
                    self.closest_aproach_dist = round(min_approach_dist, 2)
                    return "miss"
                else:
                    return "Lost"
                            
            if steps >= max_steps:
                return "stable"

    def calculate_potential_energy(self):

        #Equations:
        # Mass (m) = (4/3 * pi * (diameter(in meters)/2)^3) * 2000 kg/m^3
        # Energy in Megatons =  (.5 * m * v(m/s)^2)/(4.184 * 10^15)

        mass = ((4/3) * math.pi * (self.radius)**3) * 2000


        energy_megatons = (.5 * mass * self.speed**2)/(4.184 * 10**15)

        return round(energy_megatons, 2)
           
#Test
print("--- Asteroid 1 (Straight Line Shot) ---")
asteroid1 = MockAsteroidEngine(radius=1000, angle=0, speed=25000)
asteroid1.calculate_path()

print("\n--- Asteroid 2 (Deflected Angle Miss) ---")
asteroid2 = MockAsteroidEngine(radius=500, angle=15, speed=22000)
asteroid2.calculate_path()

print("\n--- Asteroid 3 (Fleeing Trajectory) ---")
asteroid3 = MockAsteroidEngine(radius=800, angle=180, speed=15000)
asteroid3.calculate_path()


