import streamlit as st
from app.layout import render_official_premium

st.set_page_config(page_title="Official premium", layout="wide")
render_official_premium()
