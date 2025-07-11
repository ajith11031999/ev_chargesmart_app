
import streamlit as st
from utils.helpers import init_db
from pages.home import show_home
from pages.user_dashboard import show_user_dashboard
from pages.business_dashboard import show_business_dashboard

st.set_page_config(page_title="⚡ ChargeSmart AI", layout="wide")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_home()
else:
    if st.session_state["role"] == "User":
        show_user_dashboard()
    elif st.session_state["role"] == "Business":
        show_business_dashboard()
