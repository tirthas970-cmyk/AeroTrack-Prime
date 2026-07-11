import requests
import requests
import pandas as pd
import math
from TrajectoryEngine import MockAsteroidEngine
import datetime
### TO DO: TRY- EXCEPT



class CollectAsteroidData:
    def __init__(self, API_KEY, today, next_days):
        self.query_params = {
            "api_key": API_KEY,
            "start_date": today,
            "end_date": next_days

        }
        self.name_list = []
        self.speed_list = []
        self.size_list = []
        self.is_hazardous_list = []
        self.miss_distance = []
        self.id_list = []
        self.close_approach_list = []

    def get_data(self):

        URL = "https://api.nasa.gov/neo/rest/v1/feed"
        response = requests.get(URL, params=self.query_params)

        if response.status_code == 200:
            data = response.json()

            neo = data["near_earth_objects"]

            for date, asteroids_info in neo.items():

                print(f"Asteriods of {date}")
                
                for asteroid in asteroids_info: 
                    name = asteroid["name"]
                    id = asteroid["id"]
                    closest_approach = asteroid["close_approach_data"][0]["close_approach_date_full"]

                    #name is formatted like this: (name)
                    #remove the ()
                    clean_name = name.replace("(", "").replace(")", "")
                           
                    #size
                    diameter = float(asteroid[ "estimated_diameter"]["meters"]["estimated_diameter_max"])
                  
                    #speeds
                    velocity = float(asteroid["close_approach_data"][0]["relative_velocity"]["miles_per_hour"])
        
                    #miss distance:
                    asteroid_miss_distance = float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"])
                    #miss_distance_km = asteroid_miss_distance["kilometers"]

                    is_hazardous = asteroid["is_potentially_hazardous_asteroid"]
                    
                    if is_hazardous:
                        status = "✔️"
                    else:
                       status = "❌"
                    
                    self.name_list.append(clean_name)
                    self.size_list.append(diameter)
                    self.speed_list.append(velocity)
                    self.is_hazardous_list.append(status)
                    self.miss_distance.append(asteroid_miss_distance)
                    self.id_list.append(id)
                    self.close_approach_list.append(closest_approach)

                    #return name_list, size_list, speed_list
         
        else:
            print(f"NOT WORKING  {response.status_code}")
    
    def get_table(self):
        self.get_data()

        asteroid_data = pd.DataFrame(
            {
                "Name": self.name_list,
                "Size (meters)": self.size_list,
                "Speed (mph)": self.speed_list,
                #"hazardous_status": self.is_hazardous_list

            }
        )

        return asteroid_data

    def maximun_potential_threat(self):

        #Find the max kinetic energy (not in mt)
         #d^3 * v^2
         #(\(d^3 \times v^2\)).
         #m/s = mph * .44704
       
        self.get_data()

        kinetic_energy_list = []
        for i in range(len(self.size_list)):
            kinetic_energy = (self.size_list[i] ** 3) * (self.speed_list[i] ** 2)
            kinetic_energy_list.append(kinetic_energy)
                
        highest_energy = max(kinetic_energy_list)
        highest_index = kinetic_energy_list.index(highest_energy)

        meters_per_sec = self.speed_list[highest_index] * .44704

        potetnial_energy = MockAsteroidEngine(radius=self.size_list[highest_index]/2, speed=meters_per_sec)

        energy_megatons = potetnial_energy.calculate_potential_energy()

        highest_potential_energy = {
            "Name": self.name_list[highest_index],
            "Energy": energy_megatons,
            "Size": self.size_list[highest_index],
            "Speed": self.speed_list[highest_index]
        }

        return highest_potential_energy
    

    def text_file(self, asteroid_name):

        #prepare info
        self.get_data()

        try:
            asteroid_index = self.name_list.index(asteroid_name)
        except ValueError:
            asteroid_index = 0
        
        date = datetime.datetime.now()

        month = date.strftime("%B")
        day = date.day
        time = date.strftime("%H:%M")

        simulate_asteroid = MockAsteroidEngine(radius=self.size_list[asteroid_index]/2, speed=self.speed_list[asteroid_index])
        simulate_asteroid.calculate_path




        with open("report.txt", "w", encoding="utf-8") as file:
    
            file.write(f"""===============================================================                   
ASTEROID REPORT:
Generated: {month}, {day}, {time}
================================================================    

OBJECT INFORMATION
--------------------
Asteroid ID: {self.id_list[asteroid_index]}
Asteroid Name: {asteroid_name}
Size: {self.size_list[asteroid_index]} meters
Velocity: {self.speed_list[asteroid_index]} mph
Closest Approach: {self.close_approach_list[asteroid_index]}

TRAJECTORY ANALYSIS
-----------------------
Impact Probability:
Path Intersects Earth: {simulate_asteroid.calculate_path()} //TO DO MAYBR CHANGE THIS (ANGLE IS ALWAYS 0)
Time of Closest Approach:
Max Potential Energy: {simulate_asteroid.calculate_potential_energy()} mt
Impact Time:

HISTORICAL DATA:
--------------------
Previous Observations: 
First Observed:
Known Passages:
Orbit Type:


RECOMMENDATION:
---------------



====================================================================
            END OF REPORT""")

 
        
       