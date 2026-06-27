import streamlit as st
from datetime import timedelta, date
import requests
import json

###TO DO: MAKE INTO A FUNCTION

st.title("AeroTrack Prime")

API_KEY = st.secrets["nasa_key"]

today = date.today()
tomorrow = today + timedelta(days=1)

print(f"Tomorrow: {tomorrow}")


query_params = {
    "api_key": API_KEY,
    "start_date": today,
    "end_date": tomorrow
}

URL = "https://api.nasa.gov/neo/rest/v1/feed"

response = requests.get(URL, params=query_params)

if response.status_code == 200:
    data = response.json()

    neo = data["near_earth_objects"]

    for date, asteroids_info in neo.items():

        print(f"Asteriods of {date}")
        
        for asteroid in asteroids_info: 
            name = asteroid["name"]
            
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
          

            print(f"Asteroid Name: {name} | Hazardous: {is_hazardous} | Size: {meters_max} | Speed: {velocity_mph}")



else:
    print(f"NOT WORKING  {response.status_code}")




