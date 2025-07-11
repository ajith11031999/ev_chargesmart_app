import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Session init ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.show_login = False
    st.session_state.show_register = False

# --- User data storage (temporary demo) ---
if "users" not in st.session_state:
    st.session_state.users = []

# --- Sample EV charging stations ---
def get_sample_stations():
    return pd.DataFrame({
        "Station": [f"EV Station {i+1}" for i in range(15)],
        "Avg_Wait": [random.randint(5, 30) for _ in range(15)],
        "Available_Slots": [random.randint(0, 4) for _ in range(15)],
        "Charger_Type": random.choices(["CCS2", "Type2", "Bharat DC", "CHAdeMO"], k=15),
        "lat": [13.08 + random.uniform(-0.03, 0.03) for _ in range(15)],
        "lon": [80.27 + random.uniform(-0.03, 0.03) for _ in range(15)],
    })

# --- Logout function ---
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.show_login = False
    st.session_state.show_register = False

# --- Home / Landing Page ---
def landing_page():
    st.title("⚡ ChargeSmart - AI EV Optimization")
    st.markdown("""
    Smart recommendations. Real-time maps. Intelligent wait time forecasting.

    **Services we offer:**
    - 📍 Location-aware station finder
    - ⏳ Dynamic wait time graphs
    - 🔌 Charger compatibility filters
    - 📊 Business analytics & maintenance packages
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

# --- Login Form ---
def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    role = st.radio("Login as", ["User", "Business"])

    if st.button("Login"):
        for user in st.session_state.users:
            if user["username"] == username and user["password"] == password and user["role"] == role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.success("✅ Logged in!")
                st.experimental_rerun()
        st.error("❌ Invalid credentials")

# --- Register Form ---
def register_form():
    st.subheader("📝 Register")
    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    role = st.radio("Register as", ["User", "Business"])
    extra = st.text_input("EV Model or Business Name")

    if st.button("Register"):
        st.session_state.users.append({
            "username": username,
            "password": password,
            "role": role,
            "extra": extra
        })
        st.success("✅ Registered! Please login.")
        st.session_state.show_register = False
        st.session_state.show_login = True

# --- User Dashboard ---
def user_dashboard():
    st.title("🚗 User Dashboard")
    st.button("Logout", on_click=logout)
    df = get_sample_stations()

    st.subheader("📍 Charging Stations Map")
    selected = st.selectbox("🔘 Simulate Click: Select Station", df["Station"])
    selected_data = df[df["Station"] == selected].iloc[0]

    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    st.subheader(f"📊 Wait Time at {selected_data['Station']}")
    wait_df = pd.DataFrame({
        "Time Slot": ["8-10AM", "10-12PM", "12-2PM", "2-4PM", "4-6PM", "6-8PM"],
        "Wait Time": [selected_data["Avg_Wait"] + random.randint(-3, 3) for _ in range(6)]
    })
    fig = px.line(wait_df, x="Time Slot", y="Wait Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"""
    🔌 **Charger Type:** {selected_data['Charger_Type']}
    ⏳ **Estimated Wait:** {selected_data['Avg_Wait']} mins  
    🅿️ **Available Slots:** {selected_data['Available_Slots']}
    """)

# --- Business Dashboard ---
def business_dashboard():
    st.title("🏢 Business Dashboard")
    st.button("Logout", on_click=logout)
    df = get_sample_stations()

    st.subheader("📍 Your Stations Map")
    selected = st.selectbox("🔘 Simulate Click: Select Station", df["Station"])
    selected_data = df[df["Station"] == selected].iloc[0]

    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    st.subheader(f"📊 Avg Charging Time - {selected_data['Station']}")
    charge_df = pd.DataFrame({
        "Hour": [f"{i}-{i+2}h" for i in range(8, 20, 2)],
        "Charging Time": [selected_data["Avg_Wait"] + random.randint(-5, 5) for _ in range(6)]
    })
    fig = px.bar(charge_df, x="Hour", y="Charging Time", color="Charging Time")
    st.plotly_chart(fig, use_container_width=True)

    st.success(f"""
    ⚙️ **Avg Charge Duration:** {selected_data['Avg_Wait']} mins  
    ⏱️ **Wait Time:** {selected_data['Avg_Wait'] + 10} mins  
    📦 **Maintenance Package:** Enabled  
    """)

# --- MAIN ROUTING ---
if st.session_state.logged_in:
    if st.session_state.role == "User":
        user_dashboard()
    elif st.session_state.role == "Business":
        business_dashboard()
else:
    landing_page()
    if st.session_state.show_login:
        login_form()
    if st.session_state.show_register:
        register_form()
