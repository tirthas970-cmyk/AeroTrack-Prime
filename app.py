import streamlit as st
from datetime import timedelta, date
from AsteroidData import CollectAsteroidData

import streamlit as st

st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
            background-blend-mode: multiply;
            height: 100vh;
            overflow: hidden;
        }
        
        .stApp::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(1px 1px at 20px 30px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 40px 70px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 150px 180px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 250px 110px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 300px 250px, #ffffff, rgba(0,0,0,0));
            background-repeat: repeat;
            background-size: 350px 350px;
            animation: starrySky 50s linear infinite;
            opacity: 0.8;
            pointer-events: none;
        }

        @keyframes starrySky {
            from { transform: translateY(0px); }
            to { transform: translateY(-350px); }
        }

        h1 {
            color: #FFBE46;
            text-align: center;
            font-family: Helvetica;
        }

        /* Your Custom Buttons */
        .stButton>button {
            background-color: #FFBE46;
            color: black;
            font-weight: bold;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)


st.title("AeroTrack Prime ☄️")

st.markdown("### Welcome aboard! ")

st.info("""
**What does this dashboard do?**
- **NASA Feed Table**: A clean, updating table that shows the real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's **actual** satellites
- **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!
- **Impact Zone Assessment**: Predicts landing and damage of the asteroid using Machine Leaning
- **Automated Report Generator**: A text ffile that details all information of an asteroid

        
        """)

API_KEY = st.secrets["nasa_key"]

today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)

asteroid_data = collect_asteroid_data.get_data()

st.table(asteroid_data)
