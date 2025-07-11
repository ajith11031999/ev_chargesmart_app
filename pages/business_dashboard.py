
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def show_business_dashboard():
    st.title("🏢 Business Dashboard")
    biz_user = st.session_state.get("username")
    conn = sqlite3.connect("charge_smart.db")
    df = pd.read_sql_query("SELECT name, revenue FROM stations WHERE owner=?", conn, params=(biz_user,))
    conn.close()
    if not df.empty:
        st.write("🔋 Registered Stations")
        st.dataframe(df)
        fig = px.bar(df, x="name", y="revenue", title="Revenue by Station", text="revenue")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No stations found for this business user.")
