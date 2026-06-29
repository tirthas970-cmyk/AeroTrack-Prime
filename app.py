import streamlit as st 
from datetime import timedelta, date 
from asteroidData import CollectAsteroidData 

# This must always run before any other rendering commands
st.set_page_config(layout="wide")

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
        margin-bottom: 2rem !important;
    } 
    
    /* 🪐 SCI-FI SPACE THEME BUTTON 🪐 */ 
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
    .stButton>button:active { 
        transform: translateY(1px) scale(0.98); 
    } 
    
    /* 🌌 FIXED: DIRECT COSMIC STREAMLIT TABLE HOOK 🌌 */ 
    [data-testid="stTable"] { 
        background: rgba(17, 25, 54, 0.5) !important; 
        border: 2px solid #00d2ff !important; 
        border-radius: 12px !important; 
        padding: 15px !important; 
        box-shadow: 0px 0px 15px rgba(0, 210, 255, 0.4), inset 0px 0px 15px rgba(0, 210, 255, 0.15) !important; 
        transition: box-shadow 0.4s ease-in-out !important; 
        max-width: 100% !important; 
        overflow-x: auto !important; 
    } 
    [data-testid="stTable"]:hover { 
        box-shadow: 0px 0px 25px rgba(0, 210, 255, 0.7), inset 0px 0px 20px rgba(0, 210, 255, 0.3) !important; 
    } 
    [data-testid="stTable"] table th { 
        color: #FFBE46 !important; 
        background-color: rgba(6, 11, 25, 0.8) !important; 
    } 
    [data-testid="stTable"] table td { 
        color: #ffffff !important; 
        background-color: transparent !important; 
    } 
    
    /* 🛠️ CONSTRAIN LEFT COLUMN (5/8 SIZE TRACKS) 🛠️ */ 
    [data-testid="stColumn"]:nth-of-type(1) { 
        max-width: 58% !important; 
    }

    /* 🚨 FIXED GLOWING RED SIDE PANEL CONTAINER (3/8 SIZE TRACKS) 🚨 */ 
    [data-testid="stColumn"]:nth-of-type(2) { 
        position: fixed !important; 
        top: 135px !important;               
        right: 4.5rem !important;        
        width: 33.5% !important;             
        height: 72vh !important; 
        overflow-y: auto !important; 
        padding: 25px !important; 
        background: rgba(14, 18, 36, 0.9) !important; 
        border: 2px solid #ff4b4b !important; 
        border-radius: 16px !important; 
        box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.5), inset 0px 0px 15px rgba(255, 75, 75, 0.2) !important; 
        transition: box-shadow 0.4s ease-in-out, transform 0.4s ease-in-out !important; 
        z-index: 9999 !important; 
    } 
    [data-testid="stColumn"]:nth-of-type(2):hover { 
        box-shadow: 0px 0px 35px rgba(255, 75, 75, 0.8), inset 0px 0px 25px rgba(255, 75, 75, 0.4) !important; 
    } 
    
    /* 🛠️ HIGH VISIBILITY INNER TYPOGRAPHY OVERRIDES 🛠️ */ 
    [data-testid="stColumn"]:nth-of-type(2) h2 { 
        color: #ff4b4b !important; 
        text-shadow: 0px 0px 10px rgba(255, 75, 75, 0.6); 
        margin-top: 0px !important; 
    } 
    [data-testid="stColumn"]:nth-of-type(2) p { 
        color: #ffffff !important; 
    } 
    
    /* 🪐 RADIO LABELS & WIDGET LAYERS 🪐 */ 
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stWidgetLabel"] p { 
        color: #FFBE46 !important; 
        font-weight: bold !important; 
    } 
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stMarkdownContainer"] p { 
        color: #ffffff !important; 
        font-size: 16px !important; 
    } 
    
    /* Glowing custom indicators for active radio choices */ 
    [data-testid="stColumn"]:nth-of-type(2) [role="radiogroup"] [data-checked="true"] > div { 
        background-color: #ff4b4b !important; 
        border-color: #ff4b4b !important; 
        box-shadow: 0px 0px 8px #ff4b4b !important; 
    }
    
    /* 🛠️ OVERRIDE: Isolates the scrolling tracks for main content container */ 
    .dashboard-main-content { 
        max-height: 75vh; 
        overflow-y: auto; 
        padding-right: 15px; 
    } 
</style> 
""", unsafe_allow_html=True)




st.title("AeroTrack Prime ☄️") 

if "go" not in st.session_state: 
    st.session_state.go = False 

if st.session_state.go == False: 
    st.markdown("### Welcome aboard! ") 
    st.info(""" 
    **What does this dashboard do?** 
    - **NASA Feed Table**: A clean, updating table that shows the real names, speeds, and sizes of every asteroid passing Earth today, pulled live from NASA's **actual** satellites 
    - **Trajectory Modifier**: Slide bars where you can manually change an asteroid's variables, and see if your mock asteroid hits or misses Earth! 
    - **Impact Zone Assessment**: Predicts landing and damage of the asteroid using Machine Learning 
    - **Automated Report Generator**: A text file that details all information of an asteroid 
    """) 
    col1, col2, col3 = st.columns([10, 5, 10]) 
    with col2: 
        if st.button("GO", use_container_width=True): 
            st.session_state.go = True 
            st.rerun() 
else: 
    API_KEY = st.secrets["nasa_key"] 
    today = date.today() 
    next_days = today + timedelta(days=3) 
    
    collect_asteroid_data = CollectAsteroidData(API_KEY, today, next_days) 
    asteroid_data = collect_asteroid_data.get_table() 
    asteroid_hazardous_status = collect_asteroid_data.get_critical_hazardous_status() 
    print(asteroid_hazardous_status) 
    
    # 🛠️ FIXED LAYOUT TRACKS: Explicit 5 to 3 sizing ratio applied to Python columns
    main, side = st.columns([5, 3]) 
    
    with main: 
        st.markdown('<div class="dashboard-main-content">', unsafe_allow_html=True) 
        st.table(asteroid_data) 
        st.markdown('</div>', unsafe_allow_html=True) 
        
    with side: 
        st.header("Fixed Panel") 
        st.write("This section will never scroll or collapse.") 
        
        user_choice = st.radio("Choose Category:", ["Overview", "Analytics", "Settings"]) 
        st.button("Apply Changes") 
