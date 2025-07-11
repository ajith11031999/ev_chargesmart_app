import streamlit as st
from utils.helpers import init_db
from utils.auth import logout_user

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("assets/style.css")

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# Initialize DB
init_db()

# Redirect if logged in
if st.session_state.logged_in:
    if st.session_state.role == "User":
        st.switch_page("pages/user_dashboard.py")
    elif st.session_state.role == "Business":
        st.switch_page("pages/business_dashboard.py")
else:
    # Show landing page (login/registration)
    import landing
