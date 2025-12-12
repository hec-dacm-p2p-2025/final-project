import streamlit as st
from app.layout import render_top_advertisers

st.set_page_config(page_title="Top advertisers", layout="wide")
render_top_advertisers()
