import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData 
from TrajectoryEngine import MockAsteroidEngine
from Markdown import Markdown
st.set_page_config(layout="wide")


# Setup Data
API_KEY = st.secrets["nasa_key"]
today = date.today()
next_days = today + timedelta(days=3)

collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days)

# The aesthetic of the dashboard
markdown = Markdown()
markdown.markdown()

if 'go' not in st.session_state:
    st.session_state.go = False

if 'next' not in st.session_state:
    st.session_state.next = False

if "clicked_row_idx" not in st.session_state:
    st.session_state.clicked_row_idx = None

if "selected_name" not in st.session_state:
    st.session_state.selected_name = None

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
                            st.metric(label="⚡ POTENTIAL ENERGY", value=f"{asteroid_simulation.calculate_potential_energy():,.2f} MT")
                            st.markdown(f"Estimated closest approach distance: {asteroid_simulation.closest_aproach_dist} meters")
                        elif asteroid_path == "miss":
                            st.warning("MISS! Asteroid flew past Earth!")
                            st.markdown(f"Estimated closest approach distance: {asteroid_simulation.closest_aproach_dist} meters")
                            st.metric(label="⚡ POTENTIAL ENERGY", value=f"{asteroid_simulation.calculate_potential_energy():,.2f} MT")
                        elif asteroid_path == "Lost":
                            st.success("Lost in space! Flew directly away")
                            st.metric(label="⚡ POTENTIAL ENERGY", value=f"{asteroid_simulation.calculate_potential_energy():,.2f} MT")
                        else:
                            st.info("Simulation Timeout: Asteroid entered a stable orbit or calculations timed out")
            
            with other_panel:
                with open("report.txt", "r") as file:
                    file_contents = file.read()
                
                st.code(file_contents)
   
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

    st.markdown(""" 
    <style> 
    .stTable tbody tr { cursor: pointer; transition: background-color 0.2s ease; } 
    .stTable tbody tr:hover { background-color: rgba(0, 210, 255, 0.15) !important; } 
    </style> 
    """, unsafe_allow_html=True) 

    # Run JavaScript globally so it can easily see across all layout columns 
    st.components.v1.html(""" 
    <script> 
    setTimeout(() => { 
        const tableRows = window.parent.document.querySelectorAll('.stTable tbody tr'); 
        tableRows.forEach((row, index) => { 
            row.addEventListener('click', () => { 
                const url = new URL(window.parent.location.href); 
                url.searchParams.set('selected_row', index); 
                window.parent.location.href = url.href; 
            }); 
        }); 
    }, 500); // Increased slightly to 500ms to guarantee DOM is fully interactive
    </script> 
    """, height=0) 

    # 3. Capture the URL click event immediately 
    query_params = st.query_params 

    if "selected_row" in query_params: 
        clicked_index = int(query_params["selected_row"]) 
        
        # Extract name and save to memory permanently 
        clicked_asteroid_name = asteroid_data.at[clicked_index, "Name"] 
        st.session_state.selected_name = clicked_asteroid_name 
        
        # Generate the text file right here on click 
        collect_asteroid_data.text_file(clicked_asteroid_name)
        
        # 🟢 CRITICAL FIX 2: Clear the parameter immediately after reading it!
        # This cleans up your browser URL and prevents a broken refresh loop.
        st.query_params.clear()
        st.rerun()

    with main_col: 
        with st.container(): 
            st.table(asteroid_data) 

    # 5. Display the report using the persistent session state 
    # This ensures it stays on screen even after query_params disappear 
    if st.session_state.selected_name is not None: 
        with side_col: 
            st.markdown(f"### 📊 Report for **{st.session_state.selected_name}**") 
            try: 
                with open("report.txt", "r") as file: 
                    file_contents = file.read() 
                st.code(file_contents) 
            except FileNotFoundError: 
                st.error("The file 'report.txt' was not found.")

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
            
            