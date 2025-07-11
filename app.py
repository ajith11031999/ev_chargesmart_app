import streamlit as st
import pandas as pd
import plotly.express as px
import random

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
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.show_login = False
    st.session_state.show_register = False

# ---------------- Landing Page ----------------
def landing_page():
    st.title("⚡ ChargeSmart - Smart EV Charging Assistant")
    st.markdown("""
Welcome to **ChargeSmart**, your EV charging optimization platform.

💡 **What we offer:**
- 🚗 Real-time station recommendations based on your battery & car
- 📍 Location-based suggestions & maps
- 📈 Dynamic wait time graphs
- 🧰 Maintenance + analytics for charging station businesses
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.show_login = True
            st.session_state.show_register = False
    with col2:
        if st.button("📝 Register"):
            st.session_state.show_register = True
            st.session_state.show_login = False

# ---------------- Login Form ----------------
def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    role = st.radio("Login as", ["User", "Business"])

    if st.button("Login"):
        for user in predefined_accounts:
            if user["username"] == username and user["password"] == password and user["role"] == role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.success("✅ Login successful!")
                st.experimental_rerun()
        st.error("❌ Invalid credentials")

# ---------------- Register Form ----------------
def register_form():
    st.subheader("📝 Registration (Disabled for demo)")
    st.info("Use predefined demo users:\n- Username: user1 to user10\n- Password: 123\n\nBusiness logins:\n- biz1 to biz10")

# ---------------- User Dashboard ----------------
def user_dashboard():
    st.title("🔌 EV Charging Station Finder")
    st.button("🚪 Logout", on_click=logout)

    df = get_sample_stations()

    st.subheader("📍 Map of Nearby Charging Stations")
    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("⬇️ Simulate station click", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    wait_df = pd.DataFrame({
        "Time Slot": ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM"],
        "Wait Time": [selected["Avg_Wait"] + random.randint(-2, 4) for _ in range(5)]
    })

    st.subheader(f"📊 Predicted Wait Time: {clicked}")
    fig = px.line(wait_df, x="Time Slot", y="Wait Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
🔌 **Charger Type:** {selected['Charger_Type']}  
🅿️ **Available Slots:** {selected['Available_Slots']}  
⏱️ **Current Wait Time:** ~{selected['Avg_Wait']} min  
📍 **Distance Estimate:** ~{random.randint(2, 10)} km
""")

# ---------------- Business Dashboard ----------------
def business_dashboard():
    st.title("🏢 Business Analytics Dashboard")
    st.button("🚪 Logout", on_click=logout)

    df = get_sample_stations("business")

    st.subheader("📍 Your Registered Stations")
    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    clicked = st.selectbox("⬇️ Simulate station selection", df["Station"])
    selected = df[df["Station"] == clicked].iloc[0]

    charge_df = pd.DataFrame({
        "Hour
