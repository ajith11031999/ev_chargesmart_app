import streamlit as st

def show_business_dashboard():
    st.title("🏭 Business Dashboard")
    st.success(f"Hello, {st.session_state.get('username')}!")
    st.write("Coming soon: Registered stations, wait time analytics, revenue trends.")
