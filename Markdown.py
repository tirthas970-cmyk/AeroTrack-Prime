import streamlit as st

class Markdown:

    def markdown(self):
        markdown_stuff = st.markdown("""
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
    padding: 6px 20px !important; /* 👈 Changed from 0px to 20px to widen the border */
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
            
/* 🔷 FORCE CENTER THE SIMULATE PATH BUTTON AND CONTENT IN THE CYAN PANEL */
[data-element-key="sim_path_panel"] div[data-testid="stVerticalBlockBorderWrapper"] > div > div > div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;   /* Centers contents vertically */
    align-items: center !important;       /* Centers contents horizontally */
    height: 100% !important;
    min-height: 100% !important;
    text-align: center !important;        /* Falls back to text alignment centering */
}

[data-element-key="sim_path_panel"] div.stButton {
    display: flex !important;
    justify-content: center !important;   /* Extra insurance to explicitly center the button asset */
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
        
        return markdown_stuff
