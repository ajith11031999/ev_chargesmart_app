from utils.auth import logout_user
import streamlit as st
from utils.helpers import init_db
from pages.landing import show_landing
from pages.user_dashboard import show_user_dashboard
from pages.business_dashboard import show_business_dashboard

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Set up Streamlit page settings
st.set_page_config(page_title="ChargeSmart", layout="wide")
init_db()  # Initialize database (only creates if not present)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Routing based on login status and user role
if st.session_state.logged_in:
    role = st.session_state.get("role")
    if role == "User":
        show_user_dashboard()
    elif role == "Business":
        show_business_dashboard()
    else:
        st.error("Unknown role. Please log out and try again.")
else:
    show_landing()
# Add logout button in top-right corner
if st.session_state.get("logged_in"):
    st.sidebar.button("🚪 Logout", on_click=lambda: logout_user())
