from pathlib import Path
import sys
import streamlit as st

# Ensure `import app...` works regardless of where you run streamlit from
STREAMLIT_DIR = Path(__file__).resolve().parent
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

st.set_page_config(page_title="Binance P2P Analytics", layout="wide")

# --- Logo ---
logo_path = STREAMLIT_DIR / "pictures" / "Binance+Logo.png"
st.image(str(logo_path), width=220)

st.title("P2P Analytics")
st.caption("Interactive exploration of spreads, premiums and market microstructure.")

st.markdown(
    """
This interactive dashboard has for purpose to allow users to explore the Binance P2P market from various angles, from Spread Dynamics to Top Advertisers per Currency.

Use the **pages** in the left sidebar to navigate:

- Spread Overview
- Insights by Currency  
    - Intraday Profile by Currency
    - Official Premium by Currency
    - Order Imbalance by Currency
    - P2P Spread by Currency
    - Price Volatility by Currency
    - Top Advertisers by Currency
- Summary table
"""
)