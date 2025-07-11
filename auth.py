
import streamlit as st
import sqlite3
from pages.user_dashboard import show_user_dashboard
from pages.business_dashboard import show_business_dashboard

def show_login_ui():
    st.title("🔐 Welcome to ChargeSmart")
    login_type = st.radio("Login As", ["User", "Business"], horizontal=True)
    menu = ["Login", "Register"]
    choice = st.selectbox("Choose Action", menu)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if choice == "Register":
        extra = st.text_input("Car Model (User) / Station Name (Business)")
        if st.button("Register"):
            conn = sqlite3.connect("charge_smart.db")
            cursor = conn.cursor()
            table = "users" if login_type == "User" else "business"
            cursor.execute(f"INSERT INTO {table} (username, password, extra) VALUES (?, ?, ?)", (username, password, extra))
            conn.commit()
            st.success("Registered successfully!")
            conn.close()
    else:
        if st.button("Login"):
            conn = sqlite3.connect("charge_smart.db")
            cursor = conn.cursor()
            table = "users" if login_type == "User" else "business"
            cursor.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            if result:
                st.session_state["user_type"] = login_type
                st.session_state["username"] = username
                st.session_state["extra"] = result[3]
                st.success(f"Welcome, {username}")
                if login_type == "User":
                    show_user_dashboard()
                else:
                    show_business_dashboard()
            else:
                st.error("Invalid credentials")
