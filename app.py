import streamlit as st
from utils.helpers import init_db
from pages.home import show_home
from pages.user_dashboard import show_user_dashboard
from pages.business_dashboard import show_business_dashboard

st.set_page_config(page_title="⚡ ChargeSmart", layout="wide")
init_db()

# Top Nav
def navbar():
    st.markdown("""
        <style>
        .navbar {
            background-color: #3f51b5;
            padding: 0.6rem 1rem;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            color: white;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            margin-right: 20px;
        }
        .navbar a:hover {
            text-decoration: underline;
        }
        </style>
        <div class='navbar'>
            <div><strong>⚡ ChargeSmart</strong></div>
            <div>
                <a href='/?page=home'>Home</a>
                <a href='/?page=user'>User</a>
                <a href='/?page=business'>Business</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

navbar()

# Routing
page = st.query_params.get("page", "home")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if page == "user":
    if st.session_state.get("logged_in") and st.session_state.get("role") == "User":
        show_user_dashboard()
    else:
        st.warning("🔐 Please login as User to access this page.")
        show_home()

elif page == "business":
    if st.session_state.get("logged_in") and st.session_state.get("role") == "Business":
        show_business_dashboard()
    else:
        st.warning("🔐 Please login as Business to access this page.")
        show_home()

else:
    show_home()
