# clean_standardize.py

import pandas as pd


def clean_and_standardize(df):
    """
    Cleans and standardizes scraped P2P data.
    Ensures numeric conversions, basic normalization of string fields,
    safe timestamp formatting, duplicate removal, and a stable column order.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Robust cleaning for amount fields
    for col in ["min_amount", "max_amount"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            df[col] = df[col].replace(
                {"None": None, "nan": None, "": None, "[]": None, "{}": None}
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    numeric_fields = ["price", "min_amount", "max_amount",
                      "finish_rate", "positive_rate"]
    for col in numeric_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "merchant_id" in df.columns:
        df["merchant_id"] = df["merchant_id"].astype(str).str.strip()

    if "merchant_name" in df.columns:
        df["merchant_name"] = df["merchant_name"].astype(str).str.strip()

    if "payment_methods" in df.columns:
        df["payment_methods"] = df["payment_methods"].astype(str).str.strip()

    for col in ["side", "asset", "fiat"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper().str.strip()

    if "timestamp_scraped" in df.columns:
        df["timestamp_scraped"] = (
            pd.to_datetime(df["timestamp_scraped"], errors="coerce")
              .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        )

    df = df.drop_duplicates()

    expected_order = [
        "run_index",
        "timestamp_scraped",
        "side",
        "price",
        "asset",
        "fiat",
        "min_amount",
        "max_amount",
        "merchant_id",
        "merchant_name",
        "finish_rate",
        "positive_rate",
        "payment_methods"
    ]

    cols_present = [c for c in expected_order if c in df.columns]
    df = df[cols_present]

    return df