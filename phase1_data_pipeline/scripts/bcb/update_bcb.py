import os
import json
import pandas as pd

from .scrape_bcb import scrape_bcb_official_rates, get_bcb_date
from .clean_bcb import clean_bcb_table
from .extract_bcb import extract_official_rates
from .save_bcb import save_bcb_raw, save_bcb_processed
from .paths_bcb import DATA_PROCESSED_BCB, METADATA_BCB


MASTER_PATH = os.path.join(DATA_PROCESSED_BCB, "bcb_master.parquet")


def update_bcb():

    extracted_date = get_bcb_date()
    metadata_date = _load_metadata_date()

    if extracted_date is not None and metadata_date == extracted_date:
        print("[BCB] skip (already updated)")
        return None

    df_raw = scrape_bcb_official_rates()
    date_value = extracted_date or pd.Timestamp.utcnow().strftime("%Y-%m-%d")

    save_bcb_raw(df_raw, date_value)
    print("[BCB] RAW saved")

    df_clean = clean_bcb_table(df_raw)
    df_fx = extract_official_rates(df_clean)

    df_fx.insert(0, "date", date_value)
    _add_date_fields(df_fx)
    df_fx = _order_columns(df_fx)

    save_bcb_processed(df_fx)
    print("[BCB] today updated")

    if extracted_date is not None:
        _write_metadata_date(extracted_date)

    _update_master(df_fx)
    print("[BCB] master updated")

    return df_fx


def _add_date_fields(df_fx):
    df_fx["year"] = df_fx["date"].str.slice(0, 4)
    df_fx["month"] = df_fx["date"].str.slice(5, 7)
    df_fx["day"] = df_fx["date"].str.slice(8, 10)
    df_fx["year_month"] = df_fx["date"].str.slice(0, 7)


def _order_columns(df_fx):
    desired = [
        "date",
        "year",
        "month",
        "day",
        "year_month",
        "currency",
        "official_exchange_rate",
    ]
    existing = [c for c in desired if c in df_fx.columns]
    return df_fx[existing]


def _load_metadata_date():
    if not os.path.exists(METADATA_BCB):
        return None
    try:
        with open(METADATA_BCB, "r", encoding="utf-8") as f:
            meta = json.load(f)
            return meta.get("last_date")
    except:
        return None


def _write_metadata_date(date_value):
    os.makedirs(os.path.dirname(METADATA_BCB), exist_ok=True)
    with open(METADATA_BCB, "w", encoding="utf-8") as f:
        json.dump({"last_date": date_value}, f)


def _update_master(df_fx):
    if not os.path.exists(MASTER_PATH):
        df_fx.to_parquet(MASTER_PATH, index=False)
        print("[BCB] master created")
        return

    try:
        master = pd.read_parquet(MASTER_PATH)
    except:
        master = pd.DataFrame()

    new_date = df_fx["date"].iloc[0]
    master = master[master["date"] != new_date]

    updated = pd.concat([master, df_fx], ignore_index=True)
    updated.to_parquet(MASTER_PATH, index=False)

    print("[BCB] master updated")