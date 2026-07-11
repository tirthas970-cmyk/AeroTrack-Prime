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
collect_asteroid_data.text_file("2007 AA2")

import streamlit as st
import pandas as pd

# 1. Initialize click tracking in Session State
if "clicked_row_idx" not in st.session_state:
    st.session_state.clicked_row_idx = None

# Mock data matching your exact image layout
asteroid_data = pd.DataFrame([
    {"Name": "2007 AA2", "Size (meters)": 71.4562, "Speed (mph)": 16136.8667},
    {"Name": "2008 EU68", "Size (meters)": 247.7650, "Speed (mph)": 54175.1767},
    {"Name": "2012 XM145", "Size (meters)": 494.3562, "Speed (mph)": 37747.9226},
    {"Name": "2018 LQ2", "Size (meters)": 59.4347, "Speed (mph)": 9968.2759},
])

with st.container():
    # 2. Inject CSS to turn pointer into a hand and highlight rows on hover
    st.markdown("""
        <style>
        /* Target the table component cells to make them look clickable */
        .stTable tbody tr {
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        /* Add a sleek hover background change */
        .stTable tbody tr:hover {
            background-color: rgba(0, 210, 255, 0.15) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Render your exact table
    st.table(asteroid_data)

    # 4. Inject JavaScript to listen for clicks on your st.table rows
    # It communicates the clicked index back to Streamlit natively via query parameters
    st.components.v1.html("""
        <script>
        // Wait briefly for Streamlit to render the table elements
        setTimeout(() => {
            const tableRows = window.parent.document.querySelectorAll('.stTable tbody tr');
            
            tableRows.forEach((row, index) => {
                row.addEventListener('click', () => {
                    // Send the clicked index back to Python via URL parameter safely
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('selected_row', index);
                    window.parent.location.href = url.href;
                });
            });
        }, 300);
        </script>
    """, height=0) # Hidden height=0 component just to execute the JavaScript

# 5. Extract and store the clicked information in Python
query_params = st.query_params
if "selected_row" in query_params:
    clicked_index = int(query_params["selected_row"])
    
    # Save it to your persistent session state
    st.session_state.clicked_row_idx = clicked_index
    
    # Extract the target data row
    selected_asteroid = asteroid_data.iloc[clicked_index]
    
    st.success(f"Row {clicked_index} Clicked! Asteroid: **{selected_asteroid['Name']}**")

# Use your stored state anywhere else in the app
if st.session_state.clicked_row_idx is not None:
    st.write(f"Currently stored row: {st.session_state.clicked_row_idx}")
