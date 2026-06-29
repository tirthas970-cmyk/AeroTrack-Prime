import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData

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
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(1px 1px at 20px 30px, #ffffff, rgba(0,0,0,0)), 
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

/* 🪐 SCI-FI SPACE THEME BUTTON 🪐 */
.stButton>button {
    background: linear-gradient(135deg, #111936 0%, #060b19 100%) !important; /* Deep cosmic blue/black */
    color: #FFBE46 !important;         /* Gold text to match your title */
    font-weight: bold !important;
    font-size: 24px !important;         /* Big "GO" text */
    padding: 12px 0px !important;       /* Tall height */
    border-radius: 8px !important;
    border: 2px solid #FFBE46 !important; /* Gold structural ring */
    letter-spacing: 2px !important;     /* Sci-fi wide lettering */
    text-shadow: 0px 0px 8px rgba(255, 190, 70, 0.6) !important; /* Glowing text */
    transition: all 0.4s ease-in-out !important;
}

/* ☄️ NEBULA HOVER GLOW ☄️ */
.stButton>button:hover {
    background: linear-gradient(135deg, #1b2735 0%, #111936 100%) !important;
    color: #ffffff !important;         /* Text flashes white on activation */
    border-color: #ffffff !important;   /* Border turns white-hot */
    box-shadow: 0px 0px 25px rgba(255, 190, 70, 0.8), 
                0px 0px 10px rgba(255, 255, 255, 0.5) !important; /* Intense propulsion glow */
    transform: translateY(-2px) scale(1.02); /* Slight lift-off effect */
}

/* Active click state */
.stButton>button:active {
    transform: translateY(1px) scale(0.98);
}
</style>
""", unsafe_allow_html=True)



st.title("AeroTrack Prime ☄️")

API_KEY = st.secrets["nasa_key"]

today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)

asteroid_data = collect_asteroid_data.get_table()

asteroid_hazardous_status = collect_asteroid_data.get_critical_hazardous_status()

print(asteroid_hazardous_status)

if "go" not in st.session_state:
    st.session_state.go = False

if st.session_state.go == False:
    st.markdown("### Welcome aboard! ")

    st.info("""
    **What does this dashboard do?**
    - **NASA Feed Table**: A clean, updating table that shows the real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's **actual** satellites
    - **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!
    - **Impact Zone Assessment**: Predicts landing and damage of the asteroid using Machine Leaning
    - **Automated Report Generator**: A text file that details all information of an asteroid

            
            """)
    
    col1, col2, col3 = st.columns([10, 5, 10])

    with col2:
        if st.button("GO", use_container_width=True):
            st.session_state.go = True
            st.rerun()


if st.session_state.go:
    st.table(asteroid_data)



