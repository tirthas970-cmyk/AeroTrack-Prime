import streamlit as st
from datetime import timedelta, date
from asteroidData import CollectAsteroidData
from TrajectoryEngine import MockAsteroidEngine
from Markdown import Markdown
import streamlit.components.v1 as components

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
# Cache file text in state to prevent double-read glitches
if "cached_report" not in st.session_state:
    st.session_state.cached_report = ""

# welcome screen
if not st.session_state.go:
    st.title("AeroTrack Prime ☄️")
    st.markdown("### Welcome aboard!")
    st.info("""
    **What does this dashboard do?**
    - **NASA Feed Table**: A clean, updating table that shows the real names, speeds, and sizes of every asteroid passing Earth today, pulled live from Nasa's **actual** satellites
    - **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth!
    - **Impact Zone Assessment**: Predicts landing and damage of the asteroid using Machine Leaning
    - **Automated Report Generator**: A text file that details all information of an asteroid
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
        <div style="position: absolute; top: -60px; left: 0px; color: #F8FAFC; font-family: Helvetica; font-size: 24px; font-weight: bold; letter-spacing: 1px; white-space: nowrap; z-index: 999999; text-shadow: 0 0 6px rgba(0, 210, 255, 0.6);">
            🚀 AeroTrack-Prime
        </div>
        """,
        unsafe_allow_html=True
    )
    slide_panel, sim_path, other_panel = st.columns([1, .7, 2])
    with slide_panel:
        with st.container(key="sim_container"):
            Asteroid_Angle = st.slider("Asteroid Angle (°)", min_value=-90, max_value=90, value=0, help="Degrees relative to Earth. 0° is a direct head-on shot.")
            Velocity = st.slider("Velocity (m/s)", min_value=15000, max_value=30000, value=22000, help="Speed in meters per second (m/s). 22,000 m/s is roughly 49,000 mph.")
            Radius = st.slider("Radius (meters)", min_value=15, max_value=1000, value=200, help="Asteroid radius in meters. A 1,000m radius is a 2-kilometer wide asteroid.")
            asteroid_simulation = MockAsteroidEngine(angle=Asteroid_Angle, speed=Velocity, radius=Radius)
            
    with sim_path:
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
        # Pull from session state instead of direct raw files to match immediate updates
        if st.session_state.cached_report:
            st.code(st.session_state.cached_report)
        else:
            try:
                with open("report.txt", "r", encoding="utf-8") as file:
                    st.session_state.cached_report = file.read()
                st.code(st.session_state.cached_report)
            except FileNotFoundError:
                st.error("The file report.txt was not found.")
                
        if st.button("Back to terminal"):
            st.session_state.next = False
            st.rerun()

# table + panel
else:
    st.markdown(
        """
        <div style="position: absolute; top: -60px; left: 0px; color: #F8FAFC; font-family: Helvetica; font-size: 28px; font-weight: bold; letter-spacing: 1px; white-space: nowrap; z-index: 999999; text-shadow: 0 0 6px rgba(0, 210, 255, 0.6);">
            🚀 AeroTrack-Prime
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='text-align: center;'><h5>☄️Live Asteroid Data From NASA</h5></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 15px; color: #F8FAFC;'>To get a detailed assessment of an asteroid, click on the asteroid and then click <i>Detailed Report</i> on the right-hand panel</div>", unsafe_allow_html=True)
    st.write("") 
    
    asteroid_data = collect_asteroid_data.get_table()
    
    # 1. CLEAN SIDE-BY-SIDE COLUMN LAYOUT
    main_col, side_col = st.columns([3, 2])
    
    # Table Hover effects
    st.markdown("""
    <style>
    .stTable tbody tr {
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .stTable tbody tr:hover {
        background-color: rgba(0, 210, 255, 0.15) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 2. Render table inside main_col first
    with main_col:
        with st.container():
            st.table(asteroid_data)
            
    # 3. CRITICAL CSS FIX: Inject absolute suppression rules before rendering the buttons
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] > div:has(.hidden-btn-container),
        .hidden-btn-container,
        div[data-testid="stButton"]:has(button[key^="hid_btn_"]) {
            display: none !important;
            position: absolute !important;
            height: 0px !important;
            width: 0px !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Render buttons in a designated stealth container wrapper
    with st.container():
        st.markdown('<div class="hidden-btn-container">', unsafe_allow_html=True)
        for idx in range(len(asteroid_data)):
            if st.button(f"click_row_{idx}", key=f"hid_btn_{idx}"):
                clicked_asteroid_name = asteroid_data.iloc[idx]["Name"]
                st.session_state.selected_name = clicked_asteroid_name
                
                # --- THE CRITICAL TIMING FIX ---
                # 1. Write the file data to the disk
                collect_asteroid_data.text_file(clicked_asteroid_name)
                # 2. Force an immediate file read right here, BEFORE the rerun cuts off execution
                try:
                    with open("report.txt", "r", encoding="utf-8") as file:
                        st.session_state.cached_report = file.read()
                except FileNotFoundError:
                    st.session_state.cached_report = "Error generating report file."
                    
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 4. Inject Javascript tracker targeting parent scope components
    components.html(
        """
        <script>
        setTimeout(() => {
            const tableRows = window.parent.document.querySelectorAll('.stTable tbody tr');
            tableRows.forEach((row, index) => {
                if (!row.dataset.hasClick) {
                    row.dataset.hasClick = "true";
                    row.addEventListener('click', () => {
                        const buttons = window.parent.document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.innerText.trim() === `click_row_${index}`) {
                                btn.click();
                                break;
                            }
                        }
                    });
                }
            });
        }, 500);
        </script>
        """, 
        height=0
 