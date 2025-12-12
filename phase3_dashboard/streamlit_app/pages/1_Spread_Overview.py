import streamlit as st
from app.layout import render_spread_overview

st.set_page_config(page_title="Spread overview", layout="wide")
render_spread_overview()