# snapshot_and_master.py

import os
from datetime import datetime

import pandas as pd

from .paths_binance import (
    DATA_PROCESSED_BINANCE,
    HISTORICAL_FIAT_DIR,
    DAILY_SNAP_DIR,
    MASTER_PATH,
)


def add_time_columns(df):
    if "timestamp_scraped" not in df.columns:
        raise ValueError("timestamp_scraped is missing in the DataFrame")

    ts = pd.to_datetime(df["timestamp_scraped"], errors="coerce")

    df["scrape_datetime"] = ts.dt.strftime("%Y-%m-%d %H:%M")
    df["date"] = ts.dt.strftime("%Y-%m-%d")
    df["time"] = ts.dt.strftime("%H:%M")
    df["year"] = ts.dt.year
    df["month"] = ts.dt.month
    df["day"] = ts.dt.day
    df["year_month"] = ts.dt.strftime("%Y-%m")

    return df


def enforce_column_order(df):
    final_cols = [
        "run_index",
        "scrape_datetime",
        "date",
        "time",
        "year",
        "month",
        "day",
        "year_month",
        "currency",
        "side",
        "price",
        "min_amount",
        "max_amount",
        "merchant_name",
        "finish_rate",
        "positive_rate",
    ]

    existing = [c for c in final_cols if c in df.columns]
    return df[existing]


def update_processed_data(p2p_all, tmp_by_fiat):
    os.makedirs(DATA_PROCESSED_BINANCE, exist_ok=True)
    os.makedirs(HISTORICAL_FIAT_DIR, exist_ok=True)
    os.makedirs(DAILY_SNAP_DIR, exist_ok=True)

    p2p_all = p2p_all.copy()
    p2p_all = add_time_columns(p2p_all)

    if "fiat" in p2p_all.columns:
        p2p_all["currency"] = p2p_all["fiat"]

    p2p_all = enforce_column_order(p2p_all)

    today = datetime.utcnow().date()
    daily_path = os.path.join(DAILY_SNAP_DIR, f"daily_snapshot_{today}.parquet")

    if os.path.exists(daily_path):
        old = pd.read_parquet(daily_path)
        daily = pd.concat([old, p2p_all], ignore_index=True).drop_duplicates()
    else:
        daily = p2p_all.copy()

    daily.to_parquet(daily_path, index=False)
    print("Daily snapshot updated")

    if os.path.exists(MASTER_PATH):
        old = pd.read_parquet(MASTER_PATH)
        master = pd.concat([old, p2p_all], ignore_index=True).drop_duplicates()
    else:
        master = p2p_all.copy()

    master.to_parquet(MASTER_PATH, index=False)
    print("Master updated")

    for fiat, df_local in tmp_by_fiat.items():
        if df_local is None or df_local.empty:
            continue

        df_local = df_local.copy()
        df_local = add_time_columns(df_local)

        if "fiat" in df_local.columns:
            df_local["currency"] = df_local["fiat"]

        df_local = enforce_column_order(df_local)

        fiat_path = os.path.join(HISTORICAL_FIAT_DIR, f"{fiat}.parquet")

        if os.path.exists(fiat_path):
            old = pd.read_parquet(fiat_path)
            new = pd.concat([old, df_local], ignore_index=True).drop_duplicates()
        else:
            new = df_local.copy()

        new.to_parquet(fiat_path, index=False)

    print("Historical by currency updated")
