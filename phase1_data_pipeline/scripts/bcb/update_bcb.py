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
    print("BCB STEP 1: entering update_bcb()")

    # Extract date from website
    print("BCB STEP 2: calling get_bcb_date()")
    extracted_date = get_bcb_date()
    print("BCB STEP 3: extracted_date =", extracted_date)

    # Load metadata date
    print("BCB STEP 4: loading metadata")
    metadata_date = _load_metadata_date()
    print("BCB STEP 5: metadata_date =", metadata_date)

    # If date could not be extracted
    if extracted_date is None:
        print("BCB STEP 6: extracted_date is None")

        print("BCB STEP 7: calling scrape_bcb_official_rates()")
        df_raw = scrape_bcb_official_rates()
        print("BCB STEP 8: df_raw shape =", df_raw.shape)

        fallback_date = pd.Timestamp.utcnow().strftime("%Y-%m-%d")
        print("BCB STEP 9: fallback_date =", fallback_date)

        save_bcb_raw(df_raw, fallback_date)
        print("BCB STEP 10: raw file saved")

        df_clean = clean_bcb_table(df_raw)
        print("BCB STEP 11: df_clean shape =", df_clean.shape)

        df_fx = extract_official_rates(df_clean)
        print("BCB STEP 12: df_fx shape =", df_fx.shape)

        df_fx.insert(0, "date", fallback_date)
        _add_date_fields(df_fx)
        df_fx = _order_columns(df_fx)

        save_bcb_processed(df_fx)
        print("BCB STEP 13: processed file saved")

        _update_master(df_fx)
        print("BCB STEP 14: master updated")

        return df_fx

    # If already updated
    if metadata_date == extracted_date:
        print(f"BCB STEP 15: already updated for {extracted_date}")
        return None

    # Normal execution
    print("BCB STEP 16: scraping raw table")
    df_raw = scrape_bcb_official_rates()
    print("BCB STEP 17: df_raw shape =", df_raw.shape)

    save_bcb_raw(df_raw, extracted_date)
    print("BCB STEP 18: raw file saved")

    print("BCB STEP 19: cleaning table")
    df_clean = clean_bcb_table(df_raw)
    print("BCB STEP 20: df_clean shape =", df_clean.shape)

    print("BCB STEP 21: extracting fx values")
    df_fx = extract_official_rates(df_clean)
    print("BCB STEP 22: df_fx shape =", df_fx.shape)

    df_fx.insert(0, "date", extracted_date)
    _add_date_fields(df_fx)
    df_fx = _order_columns(df_fx)

    print("BCB STEP 23: saving processed file")
    save_bcb_processed(df_fx)
    print("BCB STEP 24: processed file saved")

    _write_metadata_date(extracted_date)
    print("BCB STEP 25: metadata updated")

    print("BCB STEP 26: updating master dataset")
    _update_master(df_fx)
    print("BCB STEP 27: master updated")

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
        print("Master created")
        return

    try:
        master = pd.read_parquet(MASTER_PATH)
    except:
        master = pd.DataFrame()

    new_date = df_fx["date"].iloc[0]
    master = master[master["date"] != new_date]

    updated = pd.concat([master, df_fx], ignore_index=True)
    updated.to_parquet(MASTER_PATH, index=False)

    print("Master updated")