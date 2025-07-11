import streamlit as st
import sqlite3

DB_NAME = "chargesmart.db"

def login_user():
    role = st.radio("Login As", ["User", "Business"], key="login_role")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        table = "users" if role == "User" else "business"
        cursor.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")


def register_user():
    role = st.radio("Register As", ["User", "Business"], key="register_role")
    username = st.text_input("New Username", key="reg_user")
    password = st.text_input("New Password", type="password", key="reg_pass")
    
    # Extra field for car model (User) or company name (Business)
    extra_label = "Car Model (e.g., Tata Nexon)" if role == "User" else "Station Name or Company"
    extra_info = st.text_input(extra_label, key="reg_extra")

    if st.button("Register", key="reg_btn"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        table = "users" if role == "User" else "business"

        # Check if username already exists
        cursor.execute(f"SELECT * FROM {table} WHERE username=?", (username,))
        if cursor.fetchone():
            st.error("⚠️ Username already exists. Try another one.")
            conn.close()
            return

        cursor.execute(f"INSERT INTO {table} (username, password, extra) VALUES (?, ?, ?)", (username, password, extra_info))
        conn.commit()
        conn.close()

        st.success("🎉 Registration successful! You can now log in.")
def logout_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
