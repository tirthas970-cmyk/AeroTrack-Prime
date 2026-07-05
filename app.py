import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData 
from TrajectoryEngine import MockAsteroidEngine

st.set_page_config(layout="wide")


# Setup Data
API_KEY = st.secrets["nasa_key"]
today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)

# The aesthetic of the dashboard
st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
    background-blend-mode: multiply;
    min-height: 100vh;
    overflow-y: auto;
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
    margin-bottom: 1.5rem !important;
}

/* 🛸 SCI-FI SPACE THEME BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #111936 0%, #060b19 100%) !important;
    color: #FFBE46 !important;
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 6px 0px !important;
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

/* 🌌 COSMIC STREAMLIT TABLE HOOK */
[data-testid="stTable"] {
    background: rgba(17, 25, 54, 0.5) !important;
    border: 2px solid #00d2ff !important;
    border-radius: 12px !important;
    padding: 12px !important;
    box-shadow: 0px 0px 15px rgba(0, 210, 255, 0.4) !important;
}

[data-testid="stTable"] table th {
    color: #FFBE46 !important;
    background-color: rgba(6, 11, 25, 0.8) !important;
    padding: 6px 10px !important;
}

[data-testid="stTable"] table td {
    color: #ffffff !important;
    padding: 6px 10px !important;
    font-size: 14px !important;
}

/* 🔴 THREAT DETECTED PANEL */
[data-element-key="threat_panel"], .st-key-threat_panel, div[data-element-key="threat_panel"] {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    min-height: 100% !important;
    padding: 22px !important;
    background: rgba(14, 18, 36, 0.95) !important;
    border: 2px solid #ff4b4b !important;
    border-radius: 16px !important;
    box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.5), inset 0px 0px 15px rgba(255, 75, 75, 0.2) !important;
}

[data-element-key="threat_panel"] h2, .st-key-threat_panel h2 {
    font-size: 1.95rem !important;
    color: #ff4b4b !important;
    text-shadow: 0px 0px 10px rgba(255, 75, 75, 0.6);
    margin-top: 0px !important;
    margin-bottom: 4px !important;
}

/* 🟢 DEEP SPACE CLEAR PANEL */
[data-element-key="clear_panel"], .st-key-clear_panel, div[data-element-key="clear_panel"] {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    min-height: 100% !important;
    padding: 22px !important;
    background: rgba(14, 18, 36, 0.95) !important;
    border: 2px solid #00ff66 !important;
    border-radius: 16px !important;
    box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.5), inset 0px 0px 15px rgba(0, 255, 102, 0.2) !important;
}

[data-element-key="clear_panel"] h2, .st-key-clear_panel h2 {
    font-size: 1.95rem !important;
    color: #00ff66 !important;
    text-shadow: 0px 0px 10px rgba(0, 255, 102, 0.6);
    margin-top: 0px !important;
    margin-bottom: 4px !important;
}

/* 🔮 PURPLE GLOWING SIMULATION PANEL */
[data-element-key="sim_container"], .st-key-sim_container, div[data-element-key="sim_container"] {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    min-height: 100% !important;
    padding: 22px !important;
    background: rgba(14, 18, 36, 0.95) !important;
    border: 2px solid #a855f7 !important;
    border-radius: 16px !important;
    box-shadow: 0px 0px 20px rgba(168, 85, 247, 0.6), inset 0px 0px 15px rgba(168, 85, 247, 0.2) !important;
}

/* Formats parent inner vertical space block */
[data-element-key="threat_panel"] > div, 
[data-element-key="clear_panel"] > div,
[data-element-key="sim_container"] > div {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    justify-content: space-between !important;
}

/* Fix spacing gaps for layout lines */
[data-element-key="threat_panel"] hr, 
[data-element-key="clear_panel"] hr,
[data-element-key="sim_container"] hr {
    margin: 12px 0 !important;
}

/* ⚡ METRICS FORMATTING */
[data-testid="stMetric"] {
    padding: 0px !important;
}

[data-testid="stMetricLabel"] p {
    font-size: 0.9rem !important;
}

[data-testid="stMetricValue"] div {
    font-size: 2.1rem !important;
    font-weight: bold !important;
}

/* Summary text description sizes */
[data-element-key="threat_panel"] p, .st-key-threat_panel p, 
[data-element-key="clear_panel"] p, .st-key-clear_panel p,
[data-element-key="sim_container"] p, .st-key-sim_container p {
    font-size: 18.5px !important;
    line-height: 2.0 !important;
    margin-bottom: 15px !important;
}

/* Shared typography overrides */
[data-element-key="threat_panel"] [data-testid="stWidgetLabel"] p, .st-key-threat_panel [data-testid="stWidgetLabel"] p, 
[data-element-key="clear_panel"] [data-testid="stWidgetLabel"] p, .st-key-clear_panel [data-testid="stWidgetLabel"] p {
    color: #FFBE46 !important;
    font-weight: bold !important;
}

/* 🌌 NEON BLUE SLIDER SKIN FOR SIMULATION PANEL */
[data-element-key="sim_container"] [data-testid="stSlider"] [role="slider"] {
    background-color: #00d2ff !important;
    box-shadow: 0px 0px 10px #00d2ff, 0px 0px 5px #00d2ff !important;
    border: 2px solid #ffffff !important;
}

[data-element-key="sim_container"] [data-testid="stSlider"] div[data-wcs-data-testid="stSliderTrack"] div {
    background: linear-gradient(90deg, #0055ff 0%, #00d2ff 100%) !important;
}

[data-element-key="sim_container"] [data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
    color: #00d2ff !important;
    text-shadow: 0px 0px 8px rgba(0, 210, 255, 0.5) !important;
    font-weight: bold !important;
}

[data-element-key="sim_container"] [data-testid="stSlider"] div {
    color: #00d2ff !important;
}

.dashboard-main-content {
    padding-right: 15px;
}

/* 🔙 TARGETED NAVIGATION BUTTON WIDTH OVERRIDES */
div.element-container:has(button[key="back_btn"]), .st-key-back_btn, .st-key-back_btn > button, 
div.element-container:has(button[key="next_btn"]), .st-key-next_btn, .st-key-next_btn > button {
    width: 200px !important;
    max-width: 90% !important;
    margin-top: 10px !important;
}
            
/* 🔷 NEON BLUE GLOWING SIMULATION PATH PANEL */
[data-element-key="sim_path_panel"], .st-key-sim_path_panel, div[data-element-key="sim_path_panel"] {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    min-height: 100% !important;
    padding: 22px !important;
    background: rgba(14, 18, 36, 0.95) !important;
    border: 2px solid #00d2ff !important; /* Cyber neon blue */
    border-radius: 16px !important;
    box-shadow: 0px 0px 20px rgba(0, 210, 255, 0.6), inset 0px 0px 15px rgba(0, 210, 255, 0.2) !important;
}

/* Match inner spacing behavior with your other panels */
[data-element-key="sim_path_panel"] > div {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
    justify-content: space-between !important;
}
</style>
""", unsafe_allow_html=True)


if 'go' not in st.session_state:
    st.session_state.go = False

if 'next' not in st.session_state:
    st.session_state.next = False

#welcome screen 
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
elif st.session_state.next:

    st.markdown(
    """
    <div style="position: absolute; top: -60px; left: 0px; color: #F8FAFC; font-family: Helvetica; font-size: 24px; font-weight: bold; letter-spacing: 1px; white-space: nowrap; z-index: 999999;
        text-shadow: 0 0 6px rgba(0, 210, 255, 0.6);">
        🚀 AeroTrack-Prime
    </div>
    """, 
    unsafe_allow_html=True
)
    
    slide_panel, sim_path, other_panel = st.columns([1, .7, 2])

    with slide_panel:
        with st.container(key="sim_container"):

            Asteroid_Angle = st.slider("Asteroid Angle (°)", min_value=-90, max_value=90, value=0, help="Degrees relative to Earth. 0° is a direct head-on shot.")
            Velocity = st.slider("Velocity (m/s)",  min_value=15000, max_value=30000, value=22000,    help="Speed in meters per second (m/s). 22,000 m/s is roughly 49,000 mph.")
            Radius = st.slider("Radius (meters)",  min_value=15, max_value=1000, value=200, help="Asteroid radius in meters. A 1,000m radius is a 2-kilometer wide asteroid.")

            asteroid_simulation = MockAsteroidEngine(angle=Asteroid_Angle, speed=Velocity, radius=Radius)

            with sim_path:
                # Wrap everything inside this column in the new neon blue panel
                with st.container(key="sim_path_panel"):
                    if st.button("Simulate Path"):
                        asteroid_path = asteroid_simulation.calculate_path()
                        if asteroid_path == "hit":
                            st.error("ASTEROID HITS EARTH!")
                            st.markdown(f"Estimated closest approach distance: {asteroid_simulation.closest_aproach_dist} meters")
                        elif asteroid_path == "miss":
                            st.warning("MISS! Asteroid flew past Earth!")
                            st.markdown(f"Estimated closest approach distance: {asteroid_simulation.closest_aproach_dist} meters")
                        elif asteroid_path == "Lost":
                            st.success("Lost in space! Flew directly away")
                        else:
                            st.info("Simulation Timeout: Asteroid entered a stable orbit or calculations timed out")
                            
   
    if st.button("Back to terminal"):
        st.session_state.next = False
        st.rerun()

#table + panel
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

    asteroid_data = collect_asteroid_data.get_table()

    # 1. CLEAN SIDE-BY-SIDE COLUMN LAYOUT
    # Generates two clean container pillars (60% table area, 40% threat display)
    main_col, side_col = st.columns([3, 2])    
    with main_col:
        # Use st.container to inject custom class styling safely without raw HTML layout leaks
        with st.container():
            st.table(asteroid_data)

    # Right side content
    with side_col:
        maximum_threat = collect_asteroid_data.maximun_potential_threat()
        
        panel_key = "threat_panel" 
        if maximum_threat:
            panel_key = "threat_panel"
        else:
            panel_key = "clear_panel"

        with st.container(key=panel_key):
            # High-impact Header with warning icon
            
            if maximum_threat:
                st.markdown("### ⚠️ CRITICAL THREAT DETECTED")

                st.caption("Maximum Potential Kinetic Energy Impact Analysis")
                st.divider()
                
                st.markdown(f"## **{maximum_threat['Name'].upper()}**")
                
                # Dynamic Threat Level Badge based on Megatons
                energy = maximum_threat['Energy']
                if energy > 1000:
                    st.error("🚨 THREAT LEVEL: PLANETARY DEVASTATION")
                elif energy > 50:
                    st.warning("🟠 THREAT LEVEL: REGIONAL EXTINCTION")
                else:
                    st.info("🟡 THREAT LEVEL: METROPOLITAN IMPACT")
                    
                st.write("") 
                
                # Sub-metrics nested neatly within the right column container
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.metric(label="⚡ POTENTIAL ENERGY", value=f"{energy:,.2f} MT")
                    st.metric(label="📏 DIAMETER", value=f"{round(maximum_threat['Size'], 3)} meters")
                with m_col2:
                    st.metric(label="🚀 VELOCITY", value=f"{round(maximum_threat['Speed'], 3)} mph")
                    
                st.divider()
                if energy > 50:
                    tsar_bomba_equiv = int(energy / 50) 
                
                else:
                    tsar_bomba_equiv = 1
                st.markdown(f"Estimated destructive yield is equivalent to detonating *{tsar_bomba_equiv:,} Tsar Bomba(s)*, the most powerful and destructive nuclear weapom ever,  simultaneously.")
            else:
                st.success("🌌 Deep space scans clear. No immediate threats detected.")
            
            
    st.write("") 
    back_btn, next_btn = st.columns([2.5, .75])
    with back_btn:
        if st.button("Back", key="back_btn"):
            st.session_state.go = False
            st.rerun()
    with next_btn:
        if st.button("Next", key="next_btn"):
            st.session_state.next = True
            st.rerun()
            
            