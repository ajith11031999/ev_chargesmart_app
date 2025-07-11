import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 🔒 Auth check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "User":
    st.warning("🚫 Unauthorized access. Please log in.")
    st.stop()

st.title("🔌 Smart Charging Station Recommendations")

# --- Sample hardcoded 15 stations
stations = pd.DataFrame({
    "Station": [f"EV Point {i+1}" for i in range(15)],
    "Avg_Wait": [random.randint(5, 35) for _ in range(15)],
    "Available_Slots": [random.randint(0, 4) for _ in range(15)],
    "Charger_Type": random.choices(["CCS2", "Type2", "Bharat DC", "CHAdeMO"], k=15),
    "lat": [13.08 + random.uniform(-0.03, 0.03) for _ in range(15)],
    "lon": [80.27 + random.uniform(-0.03, 0.03) for _ in range(15)],
})

# Show map
st.subheader("📍 Nearby Stations")
selected_station = st.map(stations.rename(columns={"lat": "latitude", "lon": "longitude"}), use_container_width=True)

# Detect selected station by click (simulated for now)
if "selected_station" not in st.session_state:
    st.session_state.selected_station = 0

clicked_station = st.selectbox("⬇️ Simulated click: Choose a station", stations["Station"])
selected_data = stations[stations["Station"] == clicked_station].iloc[0]

st.subheader(f"📊 Avg Wait Time - {selected_data['Station']}")
wait_time_data = pd.DataFrame({
    "Time Slot": ["8AM-10AM", "10AM-12PM", "12PM-2PM", "2PM-4PM", "4PM-6PM", "6PM-8PM"],
    "Avg_Wait": [selected_data["Avg_Wait"] + random.randint(-3, 3) for _ in range(6)]
})

fig = px.line(wait_time_data, x="Time Slot", y="Avg_Wait", markers=True,
              title="Wait Time Throughout the Day", labels={"Avg_Wait": "Minutes"})
st.plotly_chart(fig, use_container_width=True)

# Additional Info
st.info(f"**Charger Type:** {selected_data['Charger_Type']}  \n**Available Slots:** {selected_data['Available_Slots']}  \n**Wait Time:** ~{selected_data['Avg_Wait']} mins")
