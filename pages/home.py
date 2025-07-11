
import streamlit as st
from utils.auth import login_user, register_user

def show_home():
    st.markdown("<h1 style='text-align:center;'>⚡ Welcome to ChargeSmart</h1>", unsafe_allow_html=True)
    st.image("https://cdn.dribbble.com/users/720472/screenshots/12226761/media/e7a7e91bfe25ebecf8a95f87940dd5fc.gif", use_column_width=True)
    st.markdown("### Revolutionizing Electric Vehicle Charging Infrastructure")
    st.write("🚘 Intelligent routing | 🔌 Plug-type matching | 🔋 Real-time availability | 📊 Predictive wait times | 🤝 IoT-based optimization")
    st.markdown("### Join Us:")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔐 Login")
        login_user()
    with col2:
        st.subheader("📝 Register")
        register_user()
