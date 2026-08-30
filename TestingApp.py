import os
os.environ['NUMBA_DISABLE_JIT'] = '1'

import streamlit as st
from datetime import timedelta, date
from AsteroidData import CollectAsteroidData 
from TrajectoryEngine import MockAsteroidEngine
import pandas as pd
from Plot import PlotNewPoint
st.set_page_config(layout="wide")



# Setup Data
API_KEY = st.secrets["nasa_key"]
today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)

plotter = PlotNewPoint()
plot = plotter.plot_new_point("485823 2012 DF61")
