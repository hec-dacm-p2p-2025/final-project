import os, sys, json, time
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from multi_fetch import p2p_fetch
from clean_standardize import clean_and_standardize
from save_raw import save_raw
from snapshot_and_master import update_processed_data

from paths_binance import (
    DATA_RAW_BINANCE,
    DATA_PROCESSED_BINANCE,
    HISTORICAL_FIAT_DIR,
    DAILY_SNAP_DIR,
    MASTER_PATH
)


def update_binance():

    METADATA_DIR = os.path.join(DATA_PROCESSED_BINANCE, "metadata")

    for d in [
        DATA_RAW_BINANCE,
        DATA_PROCESSED_BINANCE,
        METADATA_DIR,
        HISTORICAL_FIAT_DIR,
        DAILY_SNAP_DIR
    ]:
        os.makedirs(d, exist_ok=True)

    run_file = os.path.join(METADATA_DIR, "run_counter.json")

    if os.path.exists(run_file):
        with open(run_file, "r") as f:
            run_index = json.load(f) + 1
    else:
        run_index = 1

    with open(run_file, "w") as f:
        json.dump(run_index, f)

    print(f"Current run index: {run_index}")

    fiats = ["USD", "EUR", "GBP", "JPY", "CNY", "MXN", "ARS", "BOB"]

    raw_dfs = []
    for fiat in fiats:
        df_raw = p2p_fetch("USDT", fiat, run_index, pages=2, delay=0.5)
        print(f"[{fiat}] {len(df_raw)} raw rows")
        raw_dfs.append(df_raw)

    p2p_all_raw = pd.concat(raw_dfs, ignore_index=True)
    p2p_all_raw = p2p_all_raw.drop(columns=["run_index"], errors="ignore")
    save_raw(p2p_all_raw, run_index)

    clean_dfs = [clean_and_standardize(df) for df in raw_dfs]
    p2p_all_clean = pd.concat(clean_dfs, ignore_index=True).drop_duplicates()

    if p2p_all_clean.empty:
        raise ValueError("Pipeline stopped: no data scraped.")

    tmp_by_fiat_clean = {fiat: clean_dfs[i] for i, fiat in enumerate(fiats)}

    update_processed_data(p2p_all_clean, tmp_by_fiat_clean)

    if not os.path.exists(MASTER_PATH):
        raise RuntimeError("Pipeline failed: master dataset not created.")

    print("Binance update completed.")

    return p2p_all_clean
