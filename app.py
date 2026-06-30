import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData 

st.set_page_config(layout="wide")

# The aesthetic of the dashboard
st.markdown(""" 
<style> 
.stApp { 
    background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%); 
    background-blend-mode: multiply; 
    min-height: 100vh; 
    overflow-y: auto; /* Changed from hidden to allow main page scrolling */ 
} 
.stApp::before { 
    content: ""; 
    position: absolute; 
    top: 0; left: 0; right: 0; bottom: 0; 
    background: radial-gradient(1px 1px at 20px 30px, #ffffff, rgba(0,0,0,0)), 
                radial-gradient(2px 2px at 40px 70px, #ffffff, rgba(0,0,0,0)), 
                radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)); 
    background-repeat: repeat; 
    background-size: 350px 350px; 
    animation: starrySky 50s linear infinite; 
    opacity: 0.8; 
    pointer-events: none; 
    z-index: 0; 
} 
@keyframes starrySky { 
    from { transform: translateY(0px); } 
    to { transform: translateY(-350px); } 
} 
h1 { 
    color: #FFBE46; 
    text-align: center; 
    font-family: Helvetica; 
    margin-bottom: 2rem !important; 
} 
/* SCI-FI SPACE THEION BUTTON */ 
.stButton>button { 
    background: linear-gradient(135deg, #111936 0%, #060b19 100%) !important; 
    color: #FFBE46 !important; 
    font-weight: bold !important; 
    font-size: 24px !important; 
    padding: 12px 0px !important; 
    border-radius: 8px !important; 
    border: 2px solid #FFBE46 !important; 
    letter-spacing: 2px !important; 
    text-shadow: 0px 0px 8px rgba(255, 190, 70, 0.6) !important; 
    transition: all 0.4s ease-in-out !important; 
} 
.stButton>button:hover { 
    background: linear-gradient(135deg, #1b2735 0%, #111936 100%) !important; 
    color: #ffffff !important; 
    border-color: #ffffff !important; 
    box-shadow: 0px 0px 25px rgba(255, 190, 70, 0.8), 0px 0px 10px rgba(255, 255, 255, 0.5) !important; 
    transform: translateY(-2px) scale(1.02); 
} 
/* COSMIC STREAMLIT TABLE HOOK */ 
[data-testid="stTable"] { 
    background: rgba(17, 25, 54, 0.5) !important; 
    border: 2px solid #00d2ff !important; 
    border-radius: 12px !important; 
    padding: 15px !important; 
    box-shadow: 0px 0px 15px rgba(0, 210, 255, 0.4) !important; 
} 
[data-testid="stTable"] table th { 
    color: #FFBE46 !important; 
    background-color: rgba(6, 11, 25, 0.8) !important; 
} 
[data-testid="stTable"] table td { 
    color: #ffffff !important; 
} 
/* 🌌 FIXED SCROLLING PANEL (REMOVED FIXED POSITIONING) 🌌 */ 
[data-element-key="fixed_panel"], .st-key-fixed_panel, div[data-element-key="fixed_panel"] { 
    position: relative !important; /* Flows normally inside its container track */ 
    width: 100% !important; /* Adapts completely to the column width */ 
    margin-top: 0px !important; 
    padding: 25px !important; 
    background: rgba(14, 18, 36, 0.95) !important; 
    border: 2px solid #ff4b4b !important; 
    border-radius: 16px !important; 
    box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.5), inset 0px 0px 15px rgba(255, 75, 75, 0.2) !important; 
} 
/* Typography overrides for internal content blocks */ 
[data-element-key="fixed_panel"] h2, .st-key-fixed_panel h2 { 
    color: #ff4b4b !important; 
    text-shadow: 0px 0px 10px rgba(255, 75, 75, 0.6); 
    margin-top: 0px !important; 
} 
[data-element-key="fixed_panel"] [data-testid="stWidgetLabel"] p, .st-key-fixed_panel [data-testid="stWidgetLabel"] p { 
    color: #FFBE46 !important; 
    font-weight: bold !important; 
} 
[data-element-key="fixed_panel"] p, .st-key-fixed_panel p { 
    color: #ffffff !important; 
} 
.dashboard-main-content { 
    padding-right: 15px; 
} 

/* 🔙 TARGETED BACK BUTTON LENGTH OVERRIDE */ 
div.element-container:has(button[key="back_btn"]), 
.st-key-back_btn, 
.st-key-back_btn > button {
    width: 200px !important;  /* Change 350px to whatever width you want */
    max-width: 100% !important;
}
</style> """, unsafe_allow_html=True)



if 'go' not in st.session_state:
    st.session_state.go = False

if not st.session_state.go:
    st.title("AeroTrack Prime ☄️")
    st.markdown("### Welcome aboard!")
    st.info("""

**What does this dashboard do?**
- **NASA Feed Table**: A clean, updating table that shows the real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's **actual** satellites
- **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!
- **Impact Zone Assessment**: Predicts landing and damage of the asteroid using Machine Leaning
- **Automated Report Generator**: A text ffile that details all information of an asteroid
"""

    )
    
    # Centered GO Button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("GO", use_container_width=True):
            st.session_state.go = True
            st.rerun()
else:
    
    st.markdown(
    """
    <div style="position: absolute; top: -60px; left: 0px; color: #F8FAFC; font-family: Helvetica; font-size: 24px; font-weight: bold; letter-spacing: 1px; white-space: nowrap; z-index: 999999;
        text-shadow: 0 0 6px rgba(0, 210, 255, 0.6);">
        🚀 AeroTrack-Prime
    </div>
    """, 
    unsafe_allow_html=True
)
    # Setup Data

    API_KEY = st.secrets["nasa_key"]
    today = date.today()
    next_days = today + timedelta(days=3)
    collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)
    asteroid_data = collect_asteroid_data.get_table()

    main, side = st.columns([5, 3])
    
    with main:
        st.markdown('<div class="dashboard-main-content">', unsafe_allow_html=True)
        st.table(asteroid_data)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Back", key="back_btn"): 
            st.session_state.go = False
            st.rerun()
        
    with side:

        maximum_threat = collect_asteroid_data.maximun_potential_threat()
        with st.container(key="fixed_panel"):
            st.header("Maximum Potential Threat") 
            st.write("This is the total potential kinetic energy of the asteroid")

            st.write(f"Name: {maximum_threat["Name"]}")
            st.write(f"Energy: {maximum_threat["Energy"]} megatons")
            st.write(f"Size: {maximum_threat["Size"]}")
            st.write(f"Speed: {maximum_threat["Speed"]}")
