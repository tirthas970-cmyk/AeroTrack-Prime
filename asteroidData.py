import requests
import requests
import pandas as pd

class CollectAsteroidData:
    def __init__(self, API_KEY, today, next_days):
        self.query_params = {
            "api_key": API_KEY,
            "start_date": today,
            "end_date": next_days

        }

    def get_data(self):

        name_list = []
        size_list = []
        speed_list = []
        is_hazardous_list= []

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
                    diameter = asteroid[ "estimated_diameter"]
                    diameter_meters = diameter["meters"]
                    meters_max = diameter_meters["estimated_diameter_max"]

                    #speeds
                    approach_data = asteroid["close_approach_data"]
                    asteroid_approahc_facts = approach_data[0]
                    relative_velocity = asteroid_approahc_facts["relative_velocity"]
                    velocity_mph = relative_velocity["miles_per_hour"]

                    is_hazardous = asteroid["is_potentially_hazardous_asteroid"]
                    
                    if is_hazardous:
                        status = "✔️"
                    else:
                        status = "❌"
                    #is_hazardous_emoji = is_hazardous.replace("false", "❌").replace("true", "✔️")
                    
                    name_list.append(clean_name)
                    size_list.append(meters_max)
                    speed_list.append(velocity_mph)
                    is_hazardous_list.append(status)

            asteroid_data = pd.DataFrame(
                {
                    "Name": name_list,
                    "Size (meters)": size_list,
                    "speed_list (mph)": speed_list,
                    "Is Hazardous": is_hazardous_list,

                }
            )

            return asteroid_data
                    



        else:
            print(f"NOT WORKING  {response.status_code}")


