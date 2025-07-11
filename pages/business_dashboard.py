import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 🔒 Auth check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "Business":
    st.warning("🚫 Unauthorized access. Please log in.")
    st.stop()

st.title("📊 Business Dashboard")

# --- Simulated registered stations
stations = pd.DataFrame({
    "Station": [f"MyStation {i+1}" for i in range(15)],
    "Avg_Wait": [random.randint(5, 35) for _ in range(15)],
    "Charge_Time": [random.randint(15, 45) for _ in range(15)],
    "lat": [13.08 + random.uniform(-0.03, 0.03) for _ in range(15)],
    "lon": [80.27 + random.uniform(-0.03, 0.03) for _ in range(15)],
})

# Map
st.subheader("🗺️ Your Station Locations")
selected_station = st.map(stations.rename(columns={"lat": "latitude", "lon": "longitude"}), use_container_width=True)

# Simulated click via dropdown for now
clicked_station = st.selectbox("⬇️ Simulated click: Choose a station", stations["Station"])
selected_data = stations[stations["Station"] == clicked_station].iloc[0]

# Graph
st.subheader(f"📈 Avg Charging Time - {selected_data['Station']}")
graph_data = pd.DataFrame({
    "Hour": [f"{i}h" for i in range(8, 21, 2)],
    "Charging Time": [selected_data["Charge_Time"] + random.randint(-5, 5) for _ in range(7)]
})

fig = px.bar(graph_data, x="Hour", y="Charging Time", color="Charging Time", title="Average Charging Duration by Hour")
st.plotly_chart(fig, use_container_width=True)

# Info
st.success(f"""
**Station:** {selected_data['Station']}  
**Avg Wait Time:** {selected_data['Avg_Wait']} mins  
**Avg Charge Duration:** {selected_data['Charge_Time']} mins  
""")

st.markdown("📦 **Maintenance Package**: Active  \n🛠️ Monthly servicing scheduled  \n📊 IoT Monitoring Enabled")
