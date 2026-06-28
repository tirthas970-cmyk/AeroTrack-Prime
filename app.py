import streamlit as st
from datetime import timedelta, date
import requests
import json
from AsteroidData import CollectAsteroidData



st.title("AeroTrack Prime")

API_KEY = st.secrets["nasa_key"]

today = date.today()
tomorrow = today + timedelta(days=1)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, tomorrow)

asteroid_data = collect_asteroid_data.get_data()

#st.subheader("1. Interactive Table (st.dataframe)")
#st.dataframe(asteroid_data, use_container_width=True)


st.subheader("2. Static Table (st.table)")
st.table(asteroid_data)
