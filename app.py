
import streamlit as st
from utils.helpers import init_db
from auth import show_login_ui

st.set_page_config(page_title="ChargeSmart", layout="wide")
init_db()
show_login_ui()
