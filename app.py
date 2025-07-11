import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration ---
st.set_page_config(layout="wide", page_title="EV Charge Finder")

# --- Hardcoded Data ---
# Charging Station Data (15-20 stations)
CHARGING_STATIONS = [
    {"id": "CS001", "name": "Green Charge Hub", "lat": 18.6161, "lon": 73.7681, "total_ports": 4, "free_ports": 2,
     "charger_types": ["CCS", "Type 2"], "amenities": ["Restroom", "Cafe"],
     "avg_wait_time_minutes": 15, "avg_charge_time_minutes": 45, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS002", "name": "Power Up Point", "lat": 18.6250, "lon": 73.7800, "total_ports": 6, "free_ports": 0,
     "charger_types": ["CHAdeMO", "Type 2"], "amenities": ["Shop"],
     "avg_wait_time_minutes": 30, "avg_charge_time_minutes": 60, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS003", "name": "Volt Valley Station", "lat": 18.6000, "lon": 73.7750, "total_ports": 3, "free_ports": 1,
     "charger_types": ["CCS"], "amenities": ["Restroom"],
     "avg_wait_time_minutes": 10, "avg_charge_time_minutes": 30, "business_id": "BIZ2"}, # Updated business_id
    {"id": "CS004", "name": "EcoCharge Plaza", "lat": 18.6300, "lon": 73.7950, "total_ports": 5, "free_ports": 3,
     "charger_types": ["Type 2"], "amenities": ["Food Court"],
     "avg_wait_time_minutes": 5, "avg_charge_time_minutes": 40, "business_id": "BIZ3"}, # Updated business_id
    {"id": "CS005", "name": "Rapid Charge Zone", "lat": 18.6050, "lon": 73.7600, "total_ports": 2, "free_ports": 0,
     "charger_types": ["CCS", "CHAdeMO"], "amenities": ["None"],
     "avg_wait_time_minutes": 45, "avg_charge_time_minutes": 75, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS006", "name": "City EV Point", "lat": 18.5900, "lon": 73.7880, "total_ports": 4, "free_ports": 2,
     "charger_types": ["Type 2"], "amenities": ["Park"],
     "avg_wait_time_minutes": 20, "avg_charge_time_minutes": 50, "business_id": "BIZ2"}, # Updated business_id
    {"id": "CS007", "name": "Highway Charge Stop", "lat": 18.6400, "lon": 73.8100, "total_ports": 8, "free_ports": 5,
     "charger_types": ["CCS", "CHAdeMO", "Type 2"], "amenities": ["Restaurant", "Restroom"],
     "avg_wait_time_minutes": 10, "avg_charge_time_minutes": 35, "business_id": "BIZ3"}, # Updated business_id
    {"id": "CS008", "name": "Tech Park Charger", "lat": 18.6100, "lon": 73.7700, "total_ports": 3, "free_ports": 1,
     "charger_types": ["CCS"], "amenities": ["Office Complex"],
     "avg_wait_time_minutes": 25, "avg_charge_time_minutes": 55, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS009", "name": "Riverside Charging", "lat": 18.5850, "lon": 73.7920, "total_ports": 5, "free_ports": 4,
     "charger_types": ["Type 2"], "amenities": ["Scenic View"],
     "avg_wait_time_minutes": 5, "avg_charge_time_minutes": 40, "business_id": "BIZ2"}, # Updated business_id
    {"id": "CS010", "name": "Mall EV Hub", "lat": 18.6200, "lon": 73.7850, "total_ports": 7, "free_ports": 3,
     "charger_types": ["CCS", "Type 2"], "amenities": ["Shopping Mall", "Food Court"],
     "avg_wait_time_minutes": 15, "avg_charge_time_minutes": 45, "business_id": "BIZ3"}, # Updated business_id
    {"id": "CS011", "name": "Industrial Zone Charge", "lat": 18.6350, "lon": 73.7550, "total_ports": 2, "free_ports": 1,
     "charger_types": ["CHAdeMO"], "amenities": ["None"],
     "avg_wait_time_minutes": 20, "avg_charge_time_minutes": 60, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS012", "name": "University EV Point", "lat": 18.5950, "lon": 73.7780, "total_ports": 3, "free_ports": 2,
     "charger_types": ["Type 2"], "amenities": ["Campus"],
     "avg_wait_time_minutes": 10, "avg_charge_time_minutes": 30, "business_id": "BIZ2"}, # Updated business_id
    {"id": "CS013", "name": "Residential Charger", "lat": 18.5700, "lon": 73.7900, "total_ports": 1, "free_ports": 1,
     "charger_types": ["Type 2"], "amenities": ["Residential Area"],
     "avg_wait_time_minutes": 0, "avg_charge_time_minutes": 120, "business_id": "BIZ3"}, # Updated business_id
    {"id": "CS014", "name": "Hotel EV Stop", "lat": 18.6080, "lon": 73.7650, "total_ports": 2, "free_ports": 0,
     "charger_types": ["CCS"], "amenities": ["Hotel", "Restaurant"],
     "avg_wait_time_minutes": 50, "avg_charge_time_minutes": 80, "business_id": "BIZ1"}, # Updated business_id
    {"id": "CS015", "name": "Parkside Charger", "lat": 18.6120, "lon": 73.7830, "total_ports": 3, "free_ports": 3,
     "charger_types": ["CHAdeMO", "Type 2"], "amenities": ["Park"],
     "avg_wait_time_minutes": 0, "avg_charge_time_minutes": 40, "business_id": "BIZ2"}, # Updated business_id
]

# User Car Data (hardcoded for demonstration)
USER_CARS = {
    "user123": {"charger_port_type": "CCS", "battery_percentage": 30, "range_left_km": 80},
    "user456": {"charger_port_type": "Type 2", "battery_percentage": 65, "range_left_km": 200},
}

# Business Machine Data (linking to stations)
BUSINESS_MACHINES = [
    {"machine_id": "M001", "station_id": "CS001", "package": "Premium", "last_maintenance": "2025-06-01", "next_maintenance": "2025-09-01"},
    {"machine_id": "M002", "station_id": "CS002", "package": "Premium", "last_maintenance": "2025-05-15", "next_maintenance": "2025-08-15"},
    {"machine_id": "M003", "station_id": "CS003", "package": "Basic", "last_maintenance": "2025-06-10", "next_maintenance": "2025-10-10"},
    {"machine_id": "M004", "station_id": "CS004", "package": "Standard", "last_maintenance": "2025-05-20", "next_maintenance": "2025-09-20"},
    {"machine_id": "M005", "station_id": "CS005", "package": "Premium", "last_maintenance": "2025-06-25", "next_maintenance": "2025-09-25"},
    {"machine_id": "M006", "station_id": "CS006", "package": "Basic", "last_maintenance": "2025-05-01", "next_maintenance": "2025-08-01"},
    {"machine_id": "M007", "station_id": "CS007", "package": "Standard", "last_maintenance": "2025-06-18", "next_maintenance": "2025-10-18"},
    {"machine_id": "M008", "station_id": "CS008", "package": "Premium", "last_maintenance": "2025-05-05", "next_maintenance": "2025-08-05"},
    {"machine_id": "M009", "station_id": "CS009", "package": "Basic", "last_maintenance": "2025-06-07", "next_maintenance": "2025-09-07"},
    {"machine_id": "M010", "station_id": "CS010", "package": "Standard", "last_maintenance": "2025-05-10", "next_maintenance": "2025-08-10"},
    {"machine_id": "M011", "station_id": "CS011", "package": "Premium", "last_maintenance": "2025-06-12", "next_maintenance": "2025-09-12"},
    {"machine_id": "M012", "station_id": "CS012", "package": "Basic", "last_maintenance": "2025-05-22", "next_maintenance": "2025-08-22"},
    {"machine_id": "M013", "station_id": "CS013", "package": "Standard", "last_maintenance": "2025-06-03", "next_maintenance": "2025-09-03"},
    {"machine_id": "M014", "station_id": "CS014", "package": "Premium", "last_maintenance": "2025-05-28", "next_maintenance": "2025-08-28"},
    {"machine_id": "M015", "station_id": "CS015", "package": "Basic", "last_maintenance": "2025-06-15", "next_maintenance": "2025-09-15"},
]


# User and Business Credentials
USER_CREDENTIALS = {"user123": "pass123", "user456": "pass456"}
BUSINESS_CREDENTIALS = {"bizadmin1": "bizpass1", "bizadmin2": "bizpass2", "bizadmin3": "bizpass3"}

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None # 'user' or 'business'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing' # 'landing', 'user_dashboard', 'business_dashboard'

# --- Helper Functions ---

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates using Haversine formula."""
    R = 6371  # Radius of Earth in kilometers
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

def recommend_stations(user_location, user_car_data, all_stations):
    """
    Recommends charging stations based on user's location, battery, and car type.
    Implements the three cases: immediate, mid-range, comfort.
    """
    user_lat, user_lon = user_location
    charger_port_type = user_car_data["charger_port_type"]
    battery_percentage = user_car_data["battery_percentage"]
    range_left_km = user_car_data["range_left_km"]

    recommended = []
    for station in all_stations:
        distance = calculate_distance(user_lat, user_lon, station["lat"], station["lon"])
        
        # Filter by charger type
        if charger_port_type not in station["charger_types"]:
            continue

        # Filter by reachability (within current range)
        if distance > range_left_km:
            continue

        # Add distance to station data
        station_with_distance = station.copy()
        station_with_distance["distance_km"] = round(distance, 2)
        
        recommended.append(station_with_distance)

    # Sort by distance
    recommended.sort(key=lambda x: x["distance_km"])

    # Apply zoning logic (implicit in filtering and sorting, but can be highlighted)
    immediate_need = [s for s in recommended if s["distance_km"] <= range_left_km * 0.3 and s["free_ports"] > 0] # Within 30% of range, must be free
    mid_range = [s for s in recommended if s["distance_km"] > range_left_km * 0.3 and s["distance_km"] <= range_left_km * 0.7 and s["free_ports"] > 0] # 30-70% of range, must be free
    comfort_zone = [s for s in recommended if s["distance_km"] > range_left_km * 0.7 and s["free_ports"] > 0] # 70-100% of range, must be free

    # Combine and prioritize: immediate, then mid-range, then comfort
    final_recommendations = []
    
    # Add immediate need stations first, prioritizing those with free ports
    for s in immediate_need:
        if s["free_ports"] > 0:
            final_recommendations.append(s)
    
    # Then add mid-range stations with free ports
    for s in mid_range:
        if s["free_ports"] > 0:
            final_recommendations.append(s)

    # Finally, add comfort zone stations with free ports
    for s in comfort_zone:
        if s["free_ports"] > 0:
            final_recommendations.append(s)

    # If no free stations are found, show occupied ones as secondary options
    if not final_recommendations:
        st.warning("No free stations found within your current range and charger type. Showing occupied stations as alternatives.")
        occupied_stations = [s for s in recommended if s["free_ports"] == 0]
        occupied_stations.sort(key=lambda x: x["distance_km"])
        final_recommendations.extend(occupied_stations)
    
    return final_recommendations

def display_map(stations_to_display, center_lat=18.6161, center_lon=73.7681, zoom_start=12):
    """Displays a Folium map with markers for charging stations."""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    for station in stations_to_display:
        status_color = "green" if station.get("free_ports", 0) > 0 else "red"
        status_text = f"{station.get('free_ports', 0)}/{station.get('total_ports', '?')} Free" if station.get("free_ports", 0) > 0 else "Occupied"
        
        popup_html = f"""
        <b>{station['name']}</b><br>
        Status: <span style="color:{status_color};"><b>{status_text}</b></span><br>
        Distance: {station.get('distance_km', 'N/A')} km<br>
        Charger Types: {', '.join(station['charger_types'])}<br>
        Amenities: {', '.join(station['amenities'])}<br>
        Avg. Wait Time: {station['avg_wait_time_minutes']} mins<br>
        Avg. Charge Time: {station['avg_charge_time_minutes']} mins
        """
        
        folium.Marker(
            location=[station["lat"], station["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=status_color, icon="bolt", prefix="fa")
        ).add_to(m)
    
    # Add user's current location if available
    if st.session_state.user_type == 'user' and st.session_state.username:
        user_car_data = USER_CARS.get(st.session_state.username)
        if user_car_data:
            # For simplicity, hardcode user location in Pimpri-Chinchwad
            user_lat, user_lon = 18.6161, 73.7681
            folium.Marker(
                location=[user_lat, user_lon],
                popup="Your Location",
                icon=folium.Icon(color="blue", icon="user", prefix="fa")
            ).add_to(m)

    folium_static(m, width=800, height=500)


# --- Page Functions ---

def landing_page():
    st.title("⚡ EV Charge Finder")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Find Your Next Charge!")
        st.write("""
        Welcome to EV Charge Finder, your ultimate companion for electric vehicle charging.
        We help you locate nearby charging stations, check real-time availability, and plan your charging stops efficiently.
        """)
        st.subheader("Our Services:")
        st.markdown("""
        * **Smart Recommendations:** Get personalized suggestions based on your car's battery, location, and charger type.
        * **Real-time Availability:** See which charging points are free or occupied to minimize waiting time.
        * **Zone-based Suggestions:** Recommendations tailored to your remaining range.
        * **Booking & Scheduling:** Reserve a slot in advance (for users).
        * **Maintenance & IoT Updates:** For charging station businesses, manage your machines and monitor performance.
        """)

    with col2:
        st.subheader("Join Us!")
        st.image("https://placehold.co/400x200/ADD8E6/000000?text=Interactive+EV+Content", caption="Driving towards a sustainable future!")
        st.markdown("""
        **Why Choose EV Charge Finder?**
        * Reduces range anxiety.
        * Optimizes charging time.
        * Supports EV infrastructure growth.
        * User-friendly interface.
        """)

    st.markdown("---")
    st.subheader("Login / Register")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login to your account")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        user_or_business = st.radio("Are you a?", ["User", "Business"], key="login_type")

        if st.button("Login", key="do_login"):
            if user_or_business == "User":
                if login_username in USER_CREDENTIALS and USER_CREDENTIALS[login_username] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'user'
                    st.session_state.username = login_username
                    st.session_state.current_page = 'user_dashboard'
                    st.experimental_rerun()
                else:
                    st.error("Invalid user credentials.")
            else: # Business
                if login_username in BUSINESS_CREDENTIALS and BUSINESS_CREDENTIALS[login_username] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'business'
                    st.session_state.username = login_username
                    st.session_state.current_page = 'business_dashboard'
                    st.experimental_rerun()
                else:
                    st.error("Invalid business credentials.")

    with register_tab:
        st.subheader("Register a new account")
        st.info("Registration is for demonstration purposes only. No data is stored.")
        reg_username = st.text_input("Choose Username", key="reg_username")
        reg_password = st.text_input("Choose Password", type="password", key="reg_password")
        reg_user_type = st.radio("Register as:", ["User", "Business"], key="reg_type")

        if st.button("Register", key="do_register"):
            if reg_user_type == "User":
                if reg_username in USER_CREDENTIALS:
                    st.error("Username already exists. Please choose another.")
                else:
                    # In a real app, you'd store this securely in a DB
                    # For this demo, we just simulate success
                    st.success(f"User '{reg_username}' registered successfully! You can now log in.")
            else: # Business
                if reg_username in BUSINESS_CREDENTIALS:
                    st.error("Username already exists. Please choose another.")
                else:
                    # Simulate success
                    st.success(f"Business '{reg_username}' registered successfully! You can now log in.")

def user_page():
    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.subheader("Your EV Charging Dashboard")

    user_car_data = USER_CARS.get(st.session_state.username)
    if not user_car_data:
        st.error("User car data not found. Please contact support.")
        return

    st.markdown("---")
    st.subheader("Your Vehicle Status:")
    st.write(f"**Charger Port Type:** {user_car_data['charger_port_type']}")
    st.write(f"**Current Battery Percentage:** {user_car_data['battery_percentage']}%")
    st.write(f"**Estimated Range Left:** {user_car_data['range_left_km']} km")
    st.markdown("---")

    st.subheader("Recommended Charging Stations Nearby:")

    # User's current location (hardcoded for demo, would be GPS in real app)
    user_current_location = (18.6161, 73.7681) # Pimpri-Chinchwad center

    # Get recommendations
    recommendations = recommend_stations(user_current_location, user_car_data, CHARGING_STATIONS)

    if not recommendations:
        st.info("No charging stations found matching your criteria and range.")
        return

    # Display recommendations in a table
    st.write("### Station List")
    rec_df = pd.DataFrame(recommendations)
    rec_df_display = rec_df[['name', 'distance_km', 'free_ports', 'total_ports', 'charger_types', 'amenities', 'avg_wait_time_minutes']]
    rec_df_display.columns = ['Station Name', 'Distance (km)', 'Free Ports', 'Total Ports', 'Charger Types', 'Amenities', 'Avg. Wait Time (min)']
    st.dataframe(rec_df_display, use_container_width=True)

    st.write("### Interactive Map")
    display_map(recommendations, center_lat=user_current_location[0], center_lon=user_current_location[1])

    st.markdown("---")
    st.subheader("Station Details & Booking")

    # Dropdown to select a station for details
    station_names = [s['name'] for s in recommendations]
    selected_station_name = st.selectbox("Select a station to view details and book:", station_names)

    if selected_station_name:
        selected_station = next((s for s in recommendations if s['name'] == selected_station_name), None)

        if selected_station:
            st.write(f"#### Details for {selected_station['name']}")
            
            col_graph, col_info = st.columns([2, 1])

            with col_graph:
                st.write("##### Average Wait Time Trend")
                # Dynamic graph for wait time (hardcoded data for demonstration)
                # Create some dummy data for the graph
                wait_time_data = {
                    "Time of Day": ["00-04", "04-08", "08-12", "12-16", "16-20", "20-24"],
                    "Avg. Wait Time (min)": [
                        max(0, selected_station['avg_wait_time_minutes'] - random.randint(5,10)),
                        max(0, selected_station['avg_wait_time_minutes'] - random.randint(0,5)),
                        selected_station['avg_wait_time_minutes'] + random.randint(5,15),
                        selected_station['avg_wait_time_minutes'] + random.randint(0,10),
                        selected_station['avg_wait_time_minutes'] + random.randint(10,20),
                        max(0, selected_station['avg_wait_time_minutes'] - random.randint(0,10))
                    ]
                }
                wait_time_df = pd.DataFrame(wait_time_data)
                st.line_chart(wait_time_df, x="Time of Day", y="Avg. Wait Time (min)")

            with col_info:
                st.write("##### Key Information")
                st.markdown(f"**Current Status:** {'🟢 FREE' if selected_station['free_ports'] > 0 else '🔴 OCCUPIED'}")
                st.markdown(f"**Free Ports:** {selected_station['free_ports']}/{selected_station['total_ports']}")
                st.markdown(f"**Estimated Wait Time:** {selected_station['avg_wait_time_minutes']} minutes")
                st.markdown(f"**Distance from you:** {selected_station['distance_km']} km")

                st.write("##### Book a Slot")
                if selected_station['free_ports'] > 0:
                    booking_time = st.time_input("Select booking time:", datetime.now().time())
                    booking_duration = st.slider("Select duration (hours):", 0.5, 4.0, 1.0, 0.5)
                    if st.button(f"Book Slot at {selected_station['name']}"):
                        st.success(f"Slot booked at {selected_station['name']} for {booking_duration} hours starting at {booking_time}!")
                        st.info("Note: This is a demo booking and does not reflect real-time changes.")
                else:
                    st.warning("This station is currently occupied. Booking is not available unless a slot frees up.")

def business_page():
    st.title(f"🏢 Welcome, {st.session_state.username}!")
    st.subheader("Your Charging Business Dashboard")

    # Filter stations owned by this business (hardcoded mapping)
    # The business_id in CHARGING_STATIONS should be "BIZ1", "BIZ2", "BIZ3"
    # to match the transformed username "bizadmin1" -> "BIZ1"
    current_biz_id = st.session_state.username.upper().replace("ADMIN", "") # e.g., 'BIZ1'
    biz_stations = [s for s in CHARGING_STATIONS if s.get("business_id") == current_biz_id]
    
    if not biz_stations:
        st.info("No charging stations registered under your business ID.")
        return

    st.markdown("---")
    st.subheader("Your Registered Charging Stations:")

    # Display map of their stations
    if biz_stations:
        # Calculate center for the business's stations
        center_lat = np.mean([s["lat"] for s in biz_stations])
        center_lon = np.mean([s["lon"] for s in biz_stations])
        display_map(biz_stations, center_lat=center_lat, center_lon=center_lon, zoom_start=11)
    else:
        st.info("No stations found for your business to display on the map.")

    st.markdown("---")
    st.subheader("Machine Performance & Maintenance:")

    # Get machines for this business
    biz_machines = [m for m in BUSINESS_MACHINES if m["station_id"] in [s["id"] for s in biz_stations]]

    if not biz_machines:
        st.info("No charging machines registered for your business.")
        return

    machine_names = [f"{m['machine_id']} ({next(s['name'] for s in CHARGING_STATIONS if s['id'] == m['station_id'])})" for m in biz_machines]
    selected_machine_display = st.selectbox("Select a machine to view details:", machine_names)

    if selected_machine_display:
        selected_machine_id = selected_machine_display.split(" ")[0]
        selected_machine = next((m for m in biz_machines if m['machine_id'] == selected_machine_id), None)
        
        if selected_machine:
            linked_station = next((s for s in CHARGING_STATIONS if s['id'] == selected_machine['station_id']), None)

            st.write(f"#### Details for Machine ID: {selected_machine['machine_id']}")
            st.write(f"**Located at:** {linked_station['name']}")
            st.write(f"**Package:** {selected_machine['package']} Package")
            st.write(f"**Last Maintenance:** {selected_machine['last_maintenance']}")
            st.write(f"**Next Scheduled Maintenance:** {selected_machine['next_maintenance']}")

            col_biz_graph, col_biz_info = st.columns([2, 1])

            with col_biz_graph:
                st.write("##### Average Charge Time Trend")
                # Dynamic graph for average charge time (hardcoded data)
                charge_time_data = {
                    "Hour of Day": list(range(24)),
                    "Avg. Charge Time (min)": [
                        max(20, linked_station['avg_charge_time_minutes'] + random.randint(-15, 10)) if 6 <= h < 22 else \
                        max(20, linked_station['avg_charge_time_minutes'] + random.randint(-10, 5))
                        for h in range(24)
                    ]
                }
                charge_time_df = pd.DataFrame(charge_time_data)
                st.line_chart(charge_time_df, x="Hour of Day", y="Avg. Charge Time (min)")

            with col_biz_info:
                st.write("##### IoT Updates & Metrics")
                st.markdown(f"**Current Avg. Wait Time (Station):** {linked_station['avg_wait_time_minutes']} minutes")
                st.markdown(f"**Avg. Time for One Charge (Machine):** {linked_station['avg_charge_time_minutes']} minutes")
                
                # Simulate a calculation for estimated daily usage / waiting time based on hardcoded data
                estimated_daily_charges = random.randint(10, 25) # Hardcoded for demo
                estimated_daily_wait_impact = estimated_daily_charges * linked_station['avg_wait_time_minutes'] / 60 # in hours
                st.markdown(f"**Estimated Daily Charges:** {estimated_daily_charges}")
                st.markdown(f"**Estimated Daily Wait Impact:** {round(estimated_daily_wait_impact, 1)} hours for users at this station.")
                st.markdown(f"**Current Port Status:** {linked_station['free_ports']}/{linked_station['total_ports']} Free")

# --- Main App Logic ---
def main():
    if not st.session_state.logged_in:
        landing_page()
    elif st.session_state.user_type == 'user':
        user_page()
    elif st.session_state.user_type == 'business':
        business_page()

    # Logout button (always visible after login)
    if st.session_state.logged_in:
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.username = None
            st.session_state.current_page = 'landing'
            st.experimental_rerun()

if __name__ == "__main__":
    main()
