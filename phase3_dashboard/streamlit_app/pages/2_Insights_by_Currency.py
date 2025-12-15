import streamlit as st
from app.layout import (
    render_intraday_profile,
    render_official_premium,
    render_order_imbalance,
    render_spread_heatmap,
    render_price_volatility,
    render_top_advertisers,
    )

st.set_page_config(page_title="P2P Market Insights by Currency", layout="wide")

st.title("2. P2P Market Insights by Currency")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["1) Intraday profile", "2) P2P vs Official Premium", "3) Order imbalance", "4) P2P spread", "5) Price volatility with a 7 day rolling window","6) Top Advertisers by ads and volume"]
)

with tab1:
    render_intraday_profile()

with tab2:
    render_official_premium()

with tab3:
    render_order_imbalance()

with tab4:
    render_spread_heatmap()

with tab5:
    render_price_volatility()
    
with tab6:
    render_top_advertisers()