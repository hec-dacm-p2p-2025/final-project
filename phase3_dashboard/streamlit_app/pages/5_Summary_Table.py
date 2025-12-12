import streamlit as st
from app.layout import render_summary_table

st.set_page_config(page_title="Summary table", layout="wide")
render_summary_table()
