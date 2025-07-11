import streamlit as st
import pandas as pd
import plotly.express as px
import random
from math import radians, cos, sin, asin, sqrt

# ---------------- Session Init ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.show_login = False
    st.session_state.show_register = False
# ---------------- Predefined Users & Businesses ----------------
users = [{"username": f"user{i}", "password": "123", "role": "User", "extra": f"EV Model {i}"} for i in range(1, 11)]
businesses = [{"username": f"biz{i}", "password": "123", "role": "Business", "extra": f"Biz {i}"} for i in range(1, 11)]
predefined_accounts = users + businesses

def landing_page():
    st.title("⚡ Welcome to ChargeSmart")
    st.markdown("#### Smart Charging Platform for EV India")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.show_login = True
            st.session_state.show_register = False
    with col2:
        if st.button("📝 Register"):
            st.session_state.show_register = True
            st.session_state.show_login = False

    if st.session_state.show_login:
        login_form()
    elif st.session_state.show_register:
        register_form()

def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    role = st.radio("Login as", ["User", "Business"], key="login_role")

    if st.button("Login Now"):
        matched = next((user for user in predefined_accounts if user["username"] == username and user["password"] == password and user["role"] == role), None)
        if matched:
            st.session_state.logged_in = True
            st.session_state.username = matched["username"]
            st.session_state.role = matched["role"]
            st.success("✅ Login successful! Redirecting...")
            st.rerun()  # ✅ Safely rerun to re-render with login
        else:
            st.error("❌ Invalid credentials")

def register_form():
    st.subheader("📝 Registration (Disabled in Demo)")
    st.info("Use demo accounts:\n\n- user1 to user10 / 123\n- biz1 to biz10 / 123")
# ---------------- Utility Function ----------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))
# ---------------- Sample Station Data ----------------
def get_sample_stations(user_type="user"):
    station_data = []
    for i in range(15):
        station_data.append({
            "Station": f"Station {i+1}",
            "Avg_Wait": random.randint(5, 30),
            "Available_Slots": random.randint(0, 5),
            "Charger_Type": random.choice(["CCS2", "Type2", "Bharat DC", "CHAdeMO"]),
            "lat": 13.08 + random.uniform(-0.03, 0.03),
            "lon": 80.27 + random.uniform(-0.03, 0.03),
        })
    return pd.DataFrame(station_data)
def user_dashboard():
    st.title("🔌 Smart EV Recommendation Dashboard")
    st.button("🚪 Logout", on_click=logout)

    # Simulated User Info
    battery_percent = 60
    total_range = 200  # km
    current_range = battery_percent / 100 * total_range
    green_limit = current_range * 0.66
    yellow_limit = current_range * 0.85
    user_lat, user_lon = 13.08, 80.27
    user_plug_type = "CCS2"

    st.markdown(f"""
    🔋 **Battery:** {battery_percent}%  
    🛣️ **Range Left:** {int(current_range)} km  
    🔌 **Charger Type:** {user_plug_type}
    """)

    df = get_sample_stations()
    df["Distance"] = df.apply(lambda row: haversine(user_lat, user_lon, row["lat"], row["lon"]), axis=1)

    def get_zone(row):
        if row["Distance"] > yellow_limit:
            return "Red"
        elif row["Distance"] <= green_limit and row["Available_Slots"] > 0 and row["Charger_Type"] == user_plug_type and row["Avg_Wait"] <= 30:
            return "Green"
        elif row["Distance"] <= yellow_limit and row["Available_Slots"] > 0 and row["Charger_Type"] == user_plug_type and row["Avg_Wait"] <= 30:
            return "Yellow"
        return "Red"

    df["Zone"] = df.apply(get_zone, axis=1)

    st.subheader("📍 Nearby Charging Stations (Recommended)")
    st.map(df[df["Zone"] != "Red"].rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("⬇️ Select a Station", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    wait_df = pd.DataFrame({
        "Time Slot": ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM"],
        "Wait Time": [selected["Avg_Wait"] + random.randint(-2, 4) for _ in range(5)]
    })
    st.subheader(f"📊 Wait Time Forecast: {clicked}")
    fig = px.line(wait_df, x="Time Slot", y="Wait Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
📍 **Distance:** {selected['Distance']:.1f} km  
🔌 **Charger Type:** {selected['Charger_Type']}  
🟢 **Zone:** {selected['Zone']}  
🅿️ **Available Slots:** {selected['Available_Slots']}  
⏳ **Current Wait:** {selected['Avg_Wait']} mins
    """)

    st.subheader("🕒 Book a Time Slot")
    slot = st.selectbox("Choose a time slot", ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM"])
    if st.button("✅ Book Now"):
        st.success(f"Booked **{clicked}** at **{slot}**!")

    st.subheader("🗺️ Google Maps Navigation")
    maps_url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{selected['lat']},{selected['lon']}"
    st.markdown(f"[📍 Get Directions]({maps_url})", unsafe_allow_html=True)
def business_dashboard():
    st.title("🏢 Business Charging Station Dashboard")
    st.button("🚪 Logout", on_click=logout)

    # Simulate 15 charging stations owned by the logged-in business
    df = get_sample_stations("business")

    st.subheader("📍 Map of Your Charging Stations")
    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("🔧 View Analytics For:", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    # Avg. charging time throughout the day (bar chart)
    charge_df = pd.DataFrame({
        "Hour": [f"{i}-{i+2}" for i in range(8, 20, 2)],
        "Avg Charging Time (min)": [selected["Avg_Wait"] + random.randint(-2, 4) for _ in range(6)]
    })

    st.subheader(f"📈 Avg. Charging Time – {clicked}")
    fig = px.bar(charge_df, x="Hour", y="Avg Charging Time (min)", color="Avg Charging Time (min)", height=350)
    st.plotly_chart(fig, use_container_width=True)

    # Station Info Summary
    st.info(f"""
📍 **Station:** {selected['Station']}  
🔌 **Charger Type:** {selected['Charger_Type']}  
🅿️ **Available Slots:** {selected['Available_Slots']}  
⏳ **Avg Wait Time:** {selected['Avg_Wait']} mins  
🛠️ **Maintenance Package:** Enabled  
📶 **IoT Monitoring:** Active
    """)

    st.subheader("🛠️ Maintenance & IoT Insights Package")
    st.markdown("""
- ✅ Daily IoT health checks for all ports  
- 🔁 Predictive alerts for port degradation  
- 📅 Auto-scheduling of technician visits (every 15 days)  
- 📊 Monthly energy consumption reports  
- 📉 Efficiency & wait-time analysis for each station  
""")
# ---------------- App Routing Logic ----------------

if st.session_state.get("logged_in"):
    if st.session_state.role == "User":
        user_dashboard()
    elif st.session_state.role == "Business":
        business_dashboard()
else:
    landing_page()

