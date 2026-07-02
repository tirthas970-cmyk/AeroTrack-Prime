import requests
import requests
import pandas as pd
import math

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


        #PIVOT: 
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

        #Equations:

        # Mass (m) = (4/3 * pi * (diameter(in meters)/2)^3) * 2000 kg/m^3
        # Energy in Megatons =  (.5 * m * v(m/s)^2)/(4.184 * 10^15)

        mass = ((4/3) * math.pi * (self.size_list[highest_index]/2)**3) * 2000

        meters_per_sec = self.speed_list[highest_index] * .44704

        energy_megatons = (.5 * mass * meters_per_sec**2)/(4.184 * 10**15)

        highest_potential_energy = {
            "Name": self.name_list[highest_index],
            "Energy": round(energy_megatons, 2),
            "Size": self.size_list[highest_index],
            "Speed": self.speed_list[highest_index]
        }

        return highest_potential_energy

       