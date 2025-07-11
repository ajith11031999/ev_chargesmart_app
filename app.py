import streamlit as st
from utils.helpers import init_db
from utils.auth import logout_user, login_user, register_user
from utils.helpers import DB_NAME
import sqlite3

# ---------- INIT SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.show_login = False
    st.session_state.show_register = False

# ---------- LOGOUT BUTTON ----------
def show_logout():
    if st.session_state.get("logged_in"):
        st.button("🚪 Logout", on_click=logout_user, key="logout")

# ---------- CSS ----------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("assets/style.css")

# ---------- INIT DB ----------
init_db()

# ---------- REDIRECT AFTER LOGIN ----------
if st.session_state.logged_in:
    if st.session_state.role == "User":
        st.switch_page("pages/user_dashboard.py")
    elif st.session_state.role == "Business":
        st.switch_page("pages/business_dashboard.py")

# ---------- HOMEPAGE UI ----------
st.title("⚡ ChargeSmart - AI-powered EV Optimization")
st.markdown("""
Welcome to **ChargeSmart**, your smart mobility partner for EV charging and battery swapping.
We provide:
- 📍 Real-time Charging Station Recommendations  
- 🔋 Battery Compatibility Matching  
- 📈 Wait Time Forecasting  
- 🤝 Smart IoT Maintenance Support for Businesses  
""")
st.image("assets/banner.jpg", use_container_width=True)

# ---------- BUTTONS ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("🔑 Login"):
        st.session_state.show_login = True
        st.session_state.show_register = False
with col2:
    if st.button("📝 Register"):
        st.session_state.show_register = True
        st.session_state.show_login = False

# ---------- LOGIN FORM ----------
if st.session_state.get("show_login"):
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    role = st.radio("Login as", ["User", "Business"], horizontal=True)

    if st.button("Login", key="login_btn"):
        if login_user(username, password, role):
            st.success("✅ Logged in successfully")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

# ---------- REGISTER FORM ----------
if st.session_state.get("show_register"):
    st.subheader("Register")
    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    extra = st.text_input("Your EV model or Business Name")
    role = st.radio("Register as", ["User", "Business"], horizontal=True)

    if st.button("Register", key="register_btn"):
        if register_user(username, password, role, extra):
            st.success("✅ Registered! Please login.")
            st.session_state.show_register = False
            st.session_state.show_login = True
        else:
            st.error("⚠️ Username already exists.")

# ---------- LOGOUT ----------
show_logout()
