
import streamlit as st

car_data = {
    "Tata Nexon": "CCS2",
    "MG ZS EV": "CCS2",
    "Hyundai Kona": "CCS2",
    "Mahindra e2o": "Type2",
    "BYD e6": "Type2"
}

def show_user_dashboard():
    st.title("🚗 User Dashboard")
    username = st.session_state.get("username")
    car = st.session_state.get("extra", "Tata Nexon")
    charger = car_data.get(car, "CCS2")
    st.info(f"Welcome {username}, your car: **{car}**, Plug Type: **{charger}**")
    st.success("Map, Booking & Charging Recommendation Features Coming Soon!")
