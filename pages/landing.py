import streamlit as st
from utils.auth import login_user, register_user

def show_landing():
    st.markdown("<h1 style='text-align:center;'>⚡ ChargeSmart</h1>", unsafe_allow_html=True)
    
    # Banner or Animation
    st.image("https://cdn.dribbble.com/users/720472/screenshots/12226761/media/e7a7e91bfe25ebecf8a95f87940dd5fc.gif", use_column_width=True)
    
    # Service Highlights
    st.markdown("### 🚀 Why ChargeSmart?")
    st.markdown("""
    - 🔋 **AI-powered EV Charging Recommendations**
    - 🔌 **Charger-Type Compatibility Matching**
    - 📍 **Live Availability & Wait Time Insights**
    - 🧠 **Predictive Routing Based on Battery %**
    - 📊 **Business Dashboard for Analytics + Maintenance**
    """)

    st.divider()

    # Login and Register Forms Side by Side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔐 Login")
        login_user()

    with col2:
        st.subheader("📝 Register")
        register_user()

    st.info("👋 New here? Register to get started. Already have an account? Just log in.")
