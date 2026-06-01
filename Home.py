
import streamlit as st
import streamlit_authenticator as sauth
import os
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="LearnX | FUOYE AI-LMS", page_icon="🎓", layout="wide")

# --- CUSTOM BEAUTIFICATION (CSS) ---
st.markdown("""
    <style>
    /* Main background and font */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: white;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #38bdf8 !important;
    }

    /* Welcome Header */
    .welcome-text {
        font-size: 45px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0px;
    }
    .by-text {
        font-size: 20px;
        color: #64748b;
        margin-top: -10px;
    }
    .name-highlight {
        color: #3b82f6;
        font-weight: 700;
    }

    /* Course Cards */
    .course-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 15px;
    }

    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f5f9;
        color: #475569;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e2e8f0;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Database & Environment Setup (FINAL FIX)
# ==========================================
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY2")

# Directly import from the internal source file where the engine lives
from deta.main import Deta as DirectDeta

# Initialize securely
deta = DirectDeta(DETA_KEY)
db = deta.Base("learnX_main_db")

def insert_user(username, name, password):
    return db.put({"key": username, "name": name, "password": password})

def fetch_all_users():
    try:
        res = db.fetch()
        return res.items if res.items else []
    except Exception:
        # Presentation Fallback
        return [{
            "key": "admin", 
            "name": "Ige Aminat Ayobami", 
            "password": sauth.Hasher.hash("1234")
        }]

# 3. Data Processing & Authentication
users = fetch_all_users()
credentials = {
    "usernames": {
        user["key"]: {
            "name": user["name"],
            "password": user["password"],
            "logged_in": False 
        } for user in users
    }
}

authenticator = sauth.Authenticate(
    credentials=credentials,
    cookie_name="learnx_cookie",
    key="learnx_secure_project_key_lagos_2026_defense_access_security", 
    cookie_expiry_days=30
)

# 4. Sidebar: Registration & Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
    st.title("LearnX Portal")
    st.divider()
    
    st.subheader("New Student?")
    reg_name = st.text_input("Full Name", placeholder="e.g. John Doe")
    reg_user = st.text_input("Username", placeholder="e.g. jdoe24")
    reg_pass = st.text_input("Password", type='password')
    reg_conf = st.text_input("Confirm", type='password')

    if st.button("✨ Create Account", use_container_width=True):
        if reg_pass != reg_conf:
            st.error("Passwords mismatch")
        elif not reg_name or not reg_user:
            st.warning("Please fill all fields")
        else:
            try:
                insert_user(reg_user, reg_name, sauth.Hasher.hash(reg_pass))
                st.success("Account Ready! Log in on the right.")
                st.balloons()
            except:
                st.error("Cloud Error. Use Offline Mode.")

# 5. Main Login Logic
if not st.session_state.get("authentication_status"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #1e293b;'>🎓 Student Login</h1>", unsafe_allow_html=True)
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Username or Password")
        elif st.session_state["authentication_status"] is None:
            st.info("Welcome back! Please enter your credentials to access your courses.")

# 6. Authenticated Dashboard (The screen after login)
if st.session_state["authentication_status"]:
    with st.sidebar:
        st.divider()
        authenticator.logout("🚪 Logout", "sidebar")

    # --- ENHANCED HERO HEADER ---
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); 
                    padding: 40px; border-radius: 25px; text-align: center; 
                    box-shadow: 0 15px 30px rgba(0,0,0,0.2); border: 2px solid #3b82f6;">
            <h1 style="color: white; font-size: 55px; font-weight: 900; margin-bottom: 5px; 
                       text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">
                WELCOME TO FUOYE LearnX
            </h1>
            <div style="background-color: rgba(255, 255, 255, 0.1); display: inline-block; 
                        padding: 15px 40px; border-radius: 100px; border: 3px solid #fbbf24; margin-top: 20px;">
                <p style="color: #cbd5e1; font-size: 16px; margin: 0; font-weight: 600; text-transform: uppercase;">
                    Final Year Project By:
                </p>
                <p style="color: #fbbf24; font-size: 32px; margin: 0; font-weight: 800; 
                          text-transform: uppercase; letter-spacing: 2px;">
                    {st.session_state['name']}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Content Layout
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("### 📚 Available Course Modules")
        
        # Course Cards (Revised HTML for guaranteed visibility)
        st.markdown("""
            <div style="display: flex; flex-direction: column; gap: 15px;">
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; 
                            border-left: 10px solid #fbbf24; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h3 style="color: #1e3a8a; margin: 0;">CSC 423: Expert Systems</h3>
                    <p style="color: #475569; margin: 5px 0 0 0;">Focuses on Inference Engines, Knowledge Bases, and AI logic systems.</p>
                </div>
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; 
                            border-left: 10px solid #3b82f6; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h3 style="color: #1e3a8a; margin: 0;">CSC 425: Modelling and Simulation</h3>
                    <p style="color: #475569; margin: 5px 0 0 0;">Explores performance analytics, regression models, and system validation.</p>
                </div>
                <div style="background: #ffffff; padding: 25px; border-radius: 15px; 
                            border-left: 10px solid #6366f1; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h3 style="color: #1e3a8a; margin: 0;">GNS 425: Law of Contract</h3>
                    <p style="color: #475569; margin: 5px 0 0 0;">Legal frameworks for computing and software engineering professional practice.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_side:
        st.success("📝 **Quick Instructions**\n1. Select a course from the sidebar.\n2. Study the preparatory materials.\n3. Take the **Diagnostic Quiz**.\n4. Review your AI-generated Performance Summary.")
        
        st.info("💡 **Expert Diagnosis**\nThe system identifies your strongest domains and highlights areas requiring focused revision via pie chart analytics.")

# 7. Fixed Footer
st.markdown(f"""
    <div style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0f172a; 
                color: white; text-align: center; padding: 15px; font-weight: 600; font-size: 14px; 
                border-top: 4px solid #fbbf24; z-index: 100;">
        FUOYE COMPUTER SCIENCE PROJECT &copy; 2026 | RESEARCH BY IGE AMINAT AYABAMI
    </div>
""", unsafe_allow_html=True)
