import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Dummy EV Profile for Logged-In User ---
car_model = "Tata Nexon EV"
plug_type = "CCS2"
battery_percent = 60
range_left = 120  # in km

# --- Zone Thresholds ---
green_limit = 80
yellow_limit = 100

# --- Sample Charging Stations (Hardcoded) ---
stations = [
    {"id": 1, "name": "GreenCharge - Anna Nagar", "distance": 45, "plug": "CCS2", "available": 2, "wait_times": [5, 10, 15], "amenities": "WiFi, Food"},
    {"id": 2, "name": "EVExpress - T Nagar", "distance": 85, "plug": "Type2", "available": 0, "wait_times": [25, 30, 35], "amenities": "Restroom, Drinks"},
    {"id": 3, "name": "Charge+ Go - Velachery", "distance": 95, "plug": "CCS2", "available": 1, "wait_times": [10, 12, 9], "amenities": "Shaded Parking"},
    {"id": 4, "name": "PlugPoint - Nungambakkam", "distance": 110, "plug": "CCS2", "available": 0, "wait_times": [40, 45, 50], "amenities": "Cafe, Lounge"},
    {"id": 5, "name": "RapidVolt - OMR", "distance": 60, "plug": "CCS2", "available": 3, "wait_times": [8, 12, 6], "amenities": "Shopping Mall"},
    {"id": 6, "name": "SwapXpress - Tambaram", "distance": 100, "plug": "CCS2", "available": 0, "wait_times": [28, 35, 30], "amenities": "Battery Swap"},
    {"id": 7, "name": "EVStation - Perungudi", "distance": 70, "plug": "Type2", "available": 1, "wait_times": [15, 18, 20], "amenities": "24x7 Access"},
    # Add more if you wish
]

# --- Station Logic: Zone Coloring ---
def get_zone(station):
    if station["distance"] <= green_limit and station["available"] > 0 and station["plug"] == plug_type:
        return "🟢 Green"
    elif station["distance"] <= yellow_limit and station["available"] > 0 and station["plug"] == plug_type:
        return "🟡 Yellow"
    return "🔴 Red"

for station in stations:
    station["zone"] = get_zone(station)

# --- UI Starts ---
st.title("🔋 EV User Dashboard")
st.markdown(f"Hello **{st.session_state.get('username', 'User')}**! You drive a `{car_model}` with `{plug_type}` port. Battery is at **{battery_percent}%**, range left: **{range_left} km**.")

# --- Display Map and Table of Stations ---
st.subheader("📍 Recommended Charging Stations")

station_df = pd.DataFrame(stations)
station_df["Zone"] = station_df["zone"]
station_df["Wait Time (avg)"] = station_df["wait_times"].apply(lambda x: sum(x)//len(x))
station_df_display = station_df[["name", "distance", "plug", "available", "Zone", "amenities"]]
st.dataframe(station_df_display, use_container_width=True)

# --- Clickable Station Selection ---
st.subheader("📊 Station Details")
station_names = [s["name"] for s in stations]
selected_name = st.selectbox("Select a Station", station_names)

selected = next(s for s in stations if s["name"] == selected_name)

# --- Dynamic Wait Time Graph ---
wait_df = pd.DataFrame({
    "Time Slot": ["9:00", "10:00", "11:00"],
    "Wait Time (mins)": selected["wait_times"]
})

fig = px.bar(wait_df, x="Time Slot", y="Wait Time (mins)",
             color="Wait Time (mins)", color_continuous_scale="Plasma", title=f"Average Wait Time for {selected_name}")
st.plotly_chart(fig, use_container_width=True)

# --- Wait Time and Distance ---
st.success(f"🕒 Estimated Wait Time: **{sum(selected['wait_times']) // 3} minutes**")
st.info(f"📏 Distance from you: **{selected['distance']} km**")

# --- Booking Slot Option ---
st.subheader("📆 Book This Station")
slot = st.selectbox("Choose a Time Slot", ["9:00", "10:00", "11:00"])
if st.button("Confirm Booking"):
    st.success(f"✅ Booking Confirmed at {selected_name} for {slot}!")
