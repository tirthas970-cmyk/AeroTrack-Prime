import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData 
from TrajectoryEngine import MockAsteroidEngine
import pandas as pd
st.set_page_config(layout="wide")



# Setup Data
API_KEY = st.secrets["nasa_key"]
today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)


asteroid_id = "2000001"  # Ceres (Has diameter, albedo, mass, etc.)
collect_asteroid_data.jpl_data(asteroid_id)

collect_asteroid_data.get_csv()