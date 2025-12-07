# save_bcb.py

import os
from datetime import datetime
import pandas as pd

from .paths_bcb import DATA_RAW_BCB, DATA_PROCESSED_BCB


def save_bcb_raw(df_raw, table_date):
    if df_raw is None or df_raw.empty:
        print("BCB raw not saved: empty DataFrame.")
        return

    os.makedirs(DATA_RAW_BCB, exist_ok=True)

    if hasattr(table_date, "strftime"):
        table_date_str = table_date.strftime("%d-%m-%Y")
    else:
        table_date_str = str(table_date)

    run_ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "-")
    filename = f"run_{run_ts}_TABLE-{table_date_str}_bcb.parquet"
    path = os.path.join(DATA_RAW_BCB, filename)

    df_raw.to_parquet(path, index=False)
    print("BCB RAW saved:", path)


def save_bcb_processed(df_clean):
    os.makedirs(DATA_PROCESSED_BCB, exist_ok=True)
    path = os.path.join(DATA_PROCESSED_BCB, "bcb_today.parquet")
    df_clean.to_parquet(path, index=False)
    print("Today file updated")