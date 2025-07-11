import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Logged in business
business_user = st.session_state.get("username", "Unknown")

# --- Simulated Charging Stations Registered by Business ---
stations = [
    {"id": 1, "name": "GreenCharge - Anna Nagar", "avg_wait": 10, "availability": 3, "type": "CCS2", "location": "Chennai"},
    {"id": 2, "name": "GreenCharge - T Nagar", "avg_wait": 28, "availability": 0, "type": "Type2", "location": "Chennai"},
    {"id": 3, "name": "GreenCharge - Nungambakkam", "avg_wait": 16, "availability": 1, "type": "CCS2", "location": "Chennai"},
    {"id": 4, "name": "GreenCharge - OMR", "avg_wait": 22, "availability": 2, "type": "Type2", "location": "Chennai"},
    {"id": 5, "name": "GreenCharge - Velachery", "avg_wait": 5, "availability": 4, "type": "CCS2", "location": "Chennai"},
    {"id": 6, "name": "GreenCharge - Tambaram", "avg_wait": 40, "availability": 0, "type": "CCS2", "location": "Chennai"},
]

# --- UI Starts ---
st.title("📊 Business Dashboard")
st.markdown(f"Welcome **{business_user}**. Here is your station performance overview.")

# --- Station Table ---
st.subheader("📍 Your Registered Charging Machines")
station_df = pd.DataFrame(stations)
station_df["Status"] = station_df["availability"].apply(lambda x: "🟢 Available" if x > 0 else "🔴 Full")
st.dataframe(station_df[["name", "type", "avg_wait", "availability", "Status"]], use_container_width=True)

# --- Dynamic Wait Time Graph ---
st.subheader("📈 Avg. Wait Time per Station")
fig = px.bar(station_df, x="name", y="avg_wait", color="avg_wait", title="Average Wait Time (mins)", color_continuous_scale="Turbo")
st.plotly_chart(fig, use_container_width=True)

# --- Maintenance Info ---
st.subheader("🧰 Scheduled Maintenance & IoT Services")
st.markdown("""
- 🔧 **Monthly Health Check** included
- 🛰️ **IoT Monitoring Kit** installed
- 📦 **Smart Analytics Plan** active
- 💬 Predictive maintenance alerts via dashboard

For assistance, contact: **support@chargesmart.in**
""")

# --- Location Display (simulated) ---
st.subheader("🗺️ Station Coverage")
locations = pd.DataFrame({
    "Station": [s["name"] for s in stations],
    "Latitude": [13.08 + random.uniform(-0.05, 0.05) for _ in stations],
    "Longitude": [80.27 + random.uniform(-0.05, 0.05) for _ in stations],
})
st.map(locations.rename(columns={"Latitude": "lat", "Longitude": "lon"}))
