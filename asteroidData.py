import requests
import requests
import pandas as pd

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
                    
                   #if is_hazardous:
                        #status = "✔️"
                    #else:
                       # status = "❌"
                    #is_hazardous_emoji = is_hazardous.replace("false", "❌").replace("true", "✔️")
                    

                    
                    self.name_list.append(clean_name)
                    self.size_list.append(diameter)
                    self.speed_list.append(velocity)
                    self.is_hazardous_list.append(is_hazardous)
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

    def get_critical_hazardous_status(self):
        self.get_data

        hazardous_indices = []

        for i, hazardous_status in enumerate(self.is_hazardous_list):
            if hazardous_status:
                hazardous_indices.append(i)

        
        min_difference = float('inf')
        min_index = None
        for index in hazardous_indices:
            try:
                difference = self.miss_distance[index] - 6371

                if difference < min_difference:
                    min_difference = difference
                    min_index = index
            except IndexError:
                continue 

        
        if min_index is not None:
            return f"The smallest difference is {min_difference},  at {min_index}"
        else:
            return "It is none"


   