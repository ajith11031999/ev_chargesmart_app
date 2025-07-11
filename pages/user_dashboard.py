import streamlit as st

def show_user_dashboard():
    st.title("🚘 User Dashboard")
    st.success(f"Welcome, {st.session_state.get('username')}!")
    st.write("Coming soon: Map with recommendations, dynamic graphs, and booking logic.")
