import os, sys
from datetime import datetime
import pandas as pd

# Add current directory for local imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from paths_binance import DATA_RAW_BINANCE


def save_raw(df_raw, run_index):
    """Save raw Binance P2P data into data/raw/binance/"""
    
    if df_raw is None or df_raw.empty:
        print("Binance RAW not saved: empty DataFrame.")
        return

    os.makedirs(DATA_RAW_BINANCE, exist_ok=True)

    ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "-")
    filename = f"run_{run_index:04d}_{ts}Z_raw.parquet"
    path = os.path.join(DATA_RAW_BINANCE, filename)

    df_raw.to_parquet(path, index=False)
    print("Raw saved")