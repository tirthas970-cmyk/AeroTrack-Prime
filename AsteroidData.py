import requests
import pandas as pd
import math
from TrajectoryEngine import MockAsteroidEngine
import datetime
import json
import math 
import joblib 
import numpy as np  
from scipy.spatial.distance import cdist
from scipy.spatial import KDTree

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
        self.absolute_mag_list = []


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
                    asteroid_miss_distance = float(asteroid["close_approach_data"][0]["miss_distance"]["miles"])

                    absolute_mag = asteroid["absolute_magnitude_h"]

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
                    self.absolute_mag_list.append(absolute_mag)
         
        else:
            print(f"NOT WORKING  {response.status_code}")
    
  
    def get_st_table(self):
        self.get_data()

        asteroid_data = pd.DataFrame(
            {
                "Name": self.name_list,
                "Size (meters)": self.size_list,
                "Speed (mph)": self.speed_list,
            }
        )

        return asteroid_data
    

    def get_asteroid_cluster_group(self, asteroid_name):

        self.get_data()
        try:
            asteroid_index = self.name_list.index(asteroid_name)
        except ValueError:
            asteroid_index = 0

        asteroid_csv_ready = pd.DataFrame({
            "absolute_magnitude": [self.absolute_mag_list[asteroid_index]],
            "estimated_diameter_max": [math.log10(self.size_list[asteroid_index])],
            "relative_velocity": [self.speed_list[asteroid_index]],
            "miss_distance": [math.log10(self.miss_distance[asteroid_index])],
        })

        scaler = joblib.load("scalerv3.joblib")
        asteroid_csv_ready.columns = scaler.feature_names_in_

        scaled_new = scaler.transform(asteroid_csv_ready)

        reducer = joblib.load("pca_reducerv3.joblib")
        pca_new = reducer.transform(scaled_new)

        kmeans = joblib.load("kmeans_modelv3.joblib")

        #puts into flaot64
        if hasattr(kmeans, 'cluster_centers_'):
           kmeans.cluster_centers_ = np.asarray(kmeans.cluster_centers_, dtype=np.float64, order='C')

        pca_new_stable = np.asarray(pca_new, dtype=np.float64, order='C')
        new_clusters = kmeans.predict(pca_new_stable)

        cluster_num = int(np.atleast_1d(new_clusters)[0])

        scaled_data = joblib.load("scaled_data_v2.joblib")
        tree = KDTree(scaled_data)
        distance, indices = tree.query(scaled_new, k=5)
        asteroid_names = joblib.load("asteroid_namesv2.joblib")
        top_five_name = asteroid_names.iloc[indices[0]]['name'].tolist()

        return {
            "Cluster": cluster_num,
            "point": pca_new_stable,
            "top_five": top_five_name
        }

    def get_cluster_info(self):
      #freqeuncy numbers are derived from the notebook

        cluster_info_map = [
        {
            0: "High-Velocity Deep-Space Giants",
            "Frequency": 17.93,
            "Characteristic1": "Massive bulk: Possess the largest physical diameter and highest visual brightness with the lowest absolute magnitude.",
            "Characteristic2": "Blazing speed: Travel at the fastest relative velocity in the entire dataset.",
            "Characteristic3": "Deep space: Pass by Earth at a massive distance, leaving a wide clearance gap."
        },
        {
            1: "Lumbering Small-Scale Cruisers",
            "Frequency": 38.29,
            "Characteristic1": "Compact structure: Feature small physical sizes with quite faint visual profiles.",
            "Characteristic2": "Sluggish pace: Move at the absolute slowest relative velocity among all tracked groups.",
            "Characteristic3": "Standard clearance: Maintain an intermediate, safe transit distance away from Earth."
        },
        {
            2: "Close-Approach Miniature Hazards",
            "Frequency": 14.31,
            "Characteristic1": "Extreme proximity: Record the closest miss distance, tracking significantly closer to Earth than any other cluster.",
            "Characteristic2": "Sub-compact frame: Represent the absolute smallest and visually faintest objects in the dataset.",
            "Characteristic3": "Brisk transit: Cruise at a moderate-to-high velocity through local space."
        },
        {
            3: "Mid-Sized Outerspace Transits",
            "Frequency": 29.48,
            "Characteristic1": "Intermediate scale: Form a solid mid-to-large size tier with moderate visual brightness.",
            "Characteristic2": "Steady pace: Maintain a stable, baseline cruising speed.",
            "Characteristic3": "Distant corridor: Transit along a far-reaching outer orbital path away from Earth."
        }
    ]


        return cluster_info_map

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

        potetnial_energy = MockAsteroidEngine(radius=self.size_list[highest_index]/2, speed=meters_per_sec, initial_distance=70000000)

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
        cluster = self.get_asteroid_cluster_group(asteroid_name).get("Cluster")
        map = self.get_cluster_info()

        try:
            asteroid_index = self.name_list.index(asteroid_name)
        except ValueError:
            asteroid_index = 0
        
        date = datetime.datetime.now()

        month = date.strftime("%B")
        day = date.day
        time = date.strftime("%H:%M")

        #calcualte angle --> tan(angle) = miss distance/relative velocity

        angle = round(math.degrees(math.atan(self.miss_distance[asteroid_index]/self.speed_list[asteroid_index])), 2)


        simulate_asteroid = MockAsteroidEngine(radius=self.size_list[asteroid_index]/2, speed=self.speed_list[asteroid_index] * 0.44704, angle=angle, initial_distance=700000) #intial_distance is arbitary value
    

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
Is Hazardous: {self.is_hazardous_list[asteroid_index]}

TRAJECTORY ANALYSIS
-----------------------
Path Intersects Earth: {simulate_asteroid.calculate_path()}
Max Potential Energy: {simulate_asteroid.calculate_potential_energy()} mt

AI Group Analysis:
--------------------------
Cluster Group: {cluster} - {map[cluster][cluster]}




====================================================================
            END OF REPORT""")

 
        
       