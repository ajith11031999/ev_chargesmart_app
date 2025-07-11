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

# ---------------- Logout Function ----------------
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# ---------------- Landing Page ----------------
def landing_page():
    st.title("⚡ Welcome to ChargeSmart")
    st.markdown("#### Accelerating India's EV future with smart infrastructure")

    # Show buttons unless one of the forms is active
    if not st.session_state.get("show_login") and not st.session_state.get("show_register"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Login"):
                st.session_state.show_login = True
                st.experimental_rerun()
        with col2:
            if st.button("📝 Register"):
                st.session_state.show_register = True
                st.experimental_rerun()

    # Show login or register form
    elif st.session_state.get("show_login"):
        login_form()
    elif st.session_state.get("show_register"):
        register_form()

# ---------------- Login Form ----------------
def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    role = st.radio("Login as", ["User", "Business"], key="login_role")

    if st.button("Login Now"):
        for user in predefined_accounts:
            if user["username"] == username and user["password"] == password and user["role"] == role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.show_login = False
                st.session_state.show_register = False
                st.success("✅ Login successful!")
                st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

# ---------------- Register Form ----------------
def register_form():
    st.subheader("\ud83d\udcdd Registration (Disabled for demo)")
    st.info("Use predefined demo users:\n- Username: user1 to user10\n- Password: 123\n\nBusiness logins:\n- biz1 to biz10")

# ---------------- Utility ----------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))

# ---------------- User Dashboard ----------------
def user_dashboard():
    st.title("\ud83d\udd0c Smart EV Recommendation Dashboard")
    st.button("\ud83d\udeaa Logout", on_click=logout)

    battery_percent = 60
    total_range = 200
    current_range = battery_percent / 100 * total_range
    green_limit = current_range * 0.66
    yellow_limit = current_range * 0.85
    user_lat, user_lon = 13.08, 80.27
    user_plug_type = "CCS2"

    st.markdown(f"""
    \ud83d\udd0b **Battery:** {battery_percent}%  
    \ud83d\udeb3\ufe0f **Estimated Range:** {int(current_range)} km  
    \ud83d\udd0c **Plug Type:** {user_plug_type}
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
    st.subheader("\ud83d\udccd Charging Stations (Color-coded)")
    st.map(df[df["Zone"] != "Red"].rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("\u2b07\ufe0f Simulate Station Click", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    wait_df = pd.DataFrame({
        "Time Slot": ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM"],
        "Wait Time": [selected["Avg_Wait"] + random.randint(-2, 4) for _ in range(5)]
    })
    st.subheader(f"\ud83d\udcca Wait Time Prediction: {clicked}")
    fig = px.line(wait_df, x="Time Slot", y="Wait Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
\ud83d\udccd **Distance:** {selected['Distance']:.1f} km  
\ud83d\udd0c **Charger Type:** {selected['Charger_Type']}  
\ud83d\udfe2 **Zone Status:** {selected['Zone']}  
\ud83c\udd7f\ufe0f **Available Slots:** {selected['Available_Slots']}  
\u23f3 **Current Wait Time:** {selected['Avg_Wait']} min
    """)

    st.subheader("\ud83d\udd52 Book a Time Slot")
    slot = st.selectbox("Select a time slot to book", ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM"])
    if st.button("\u2705 Confirm Booking"):
        st.success(f"Booked **{clicked}** at **{slot}**!")

    st.subheader("\ud83d\uddfc Navigate to Station")
    google_maps_url = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{selected['lat']},{selected['lon']}"
    st.markdown(f"[\ud83d\udccd Click here for directions]({google_maps_url})", unsafe_allow_html=True)

# ---------------- Business Dashboard ----------------
def business_dashboard():
    st.title("\ud83c\udfe2 Business Charging Station Dashboard")
    st.button("\ud83d\udeaa Logout", on_click=logout)

    df = get_sample_stations("business")
    st.subheader("\ud83d\udccd Your Registered Charging Stations")
    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("\ud83d\udd27 View station analytics:", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    charge_df = pd.DataFrame({
        "Hour": [f"{i}-{i+2}" for i in range(8, 20, 2)],
        "Avg Charging Time (min)": [selected["Avg_Wait"] + random.randint(-2, 4) for _ in range(6)]
    })
    st.subheader(f"\ud83d\udcc8 Avg. Charging Duration – {clicked}")
    fig = px.bar(charge_df, x="Hour", y="Avg Charging Time (min)", color="Avg Charging Time (min)", height=350)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
\ud83d\udccd **Station:** {selected['Station']}  
\ud83d\udd0c **Charger Type:** {selected['Charger_Type']}  
\ud83c\udd7f\ufe0f **Available Slots:** {selected['Available_Slots']}  
\u23f3 **Avg Wait Time:** {selected['Avg_Wait']} mins  
\ud83d\udee0\ufe0f **Maintenance Package:** Enabled  
\ud83d\udcf6 **IoT Monitoring:** Active
    """)

    st.subheader("\ud83d\udee0\ufe0f Maintenance Insights")
    st.markdown("""
- \u2705 Daily IoT status monitoring  
- \ud83d\udd04 Predictive maintenance alerts  
- \ud83d\uddd3\ufe0f Technician visit every 15 days  
- \ud83d\udcca Monthly energy report  
- \u2699\ufe0f Station usage analytics
    """)

# ---------------- Routing Logic ----------------
if not st.session_state.get("logged_in"):
    landing_page()
elif st.session_state.role == "User":
    user_dashboard()
elif st.session_state.role == "Business":
    business_dashboard()

