import streamlit as st
import sqlite3

def login_user():
    role = st.radio("Login As", ["User", "Business"], key="login_role")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login", key="login_btn"):
        conn = sqlite3.connect("chargesmart.db")
        cursor = conn.cursor()
        table = "users" if role == "User" else "business"
        cursor.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            st.session_state.logged_in = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success("Login successful!")
        else:
            st.error("Invalid credentials.")

def register_user():
    role = st.radio("Register As", ["User", "Business"], key="register_role")
    username = st.text_input("New Username", key="reg_user")
    password = st.text_input("New Password", type="password", key="reg_pass")
    extra = st.text_input("Car Model (User) or Station Name (Business)", key="reg_extra")
    if st.button("Register", key="reg_btn"):
        conn = sqlite3.connect("chargesmart.db")
        cursor = conn.cursor()
        table = "users" if role == "User" else "business"
        cursor.execute(f"INSERT INTO {table} (username, password, extra) VALUES (?, ?, ?)", (username, password, extra))
        conn.commit()
        conn.close()
        st.success("Registration complete. Please login.")
