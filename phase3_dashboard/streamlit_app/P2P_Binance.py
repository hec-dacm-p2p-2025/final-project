from pathlib import Path
import sys
import streamlit as st

# Ensure `import app...` works regardless of where you run streamlit from
STREAMLIT_DIR = Path(__file__).resolve().parent
if str(STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(STREAMLIT_DIR))

st.set_page_config(page_title="Binance P2P Market Dashboard", layout="wide")

st.title("Binance P2P Market Dashboard")
st.caption("Interactive exploration of spreads, premiums and market microstructure.")

st.markdown(
    """
This interactive dashborads has for purpose to allow users to explore the Binance P2P market from various angle - from spread dydnamics to top advertisers per currency.

Use the **pages** in the left sidebar to navigate:

- Spread overview  
- Intraday profile  
- Official premium  
- Top advertisers  
- Summary table
"""
)