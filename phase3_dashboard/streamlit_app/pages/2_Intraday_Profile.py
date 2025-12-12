import streamlit as st
from app.layout import render_intraday_profile

st.set_page_config(page_title="Intraday profile", layout="wide")
render_intraday_profile()
