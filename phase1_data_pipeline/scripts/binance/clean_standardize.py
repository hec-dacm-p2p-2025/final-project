import pandas as pd

def clean_and_standardize(df):
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Numeric fields
    for col in ["min_amount", "max_amount"]:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
                .replace({"None": None, "nan": None, "", None})
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    numeric_fields = ["price", "min_amount", "max_amount",
                      "finish_rate", "positive_rate"]
    for col in numeric_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # String normalization
    for col in ["merchant_id", "merchant_name", "payment_methods"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["side", "asset", "fiat"]:
        if col in df.columns:
            df[col] = df[col].astype(str).upper().str.strip()

    # FORMAT FIXES (NO NEW COLUMNS)
    # timestamp_scraped → timestamp
    if "timestamp_scraped" in df.columns:
        df["timestamp_scraped"] = pd.to_datetime(df["timestamp_scraped"], errors="coerce")

    # date → DATE
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    # time → HH:MM (keep string but normalized)
    if "time" in df.columns:
        df["time"] = (
            pd.to_datetime(df["time"], errors="coerce")
            .dt.strftime("%H:%M")
        )

    # year/month/day → INTEGER
    for col in ["year", "month", "day"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # year_month → YYYY-MM
    if "year_month" in df.columns:
        df["year_month"] = (
            pd.to_datetime(df["year_month"], errors="coerce")
            .dt.strftime("%Y-%m")
        )

    df = df.drop_duplicates()

    expected_order = [
        "run_index",
        "timestamp_scraped",
        "date",
        "time",
        "year",
        "month",
        "day",
        "year_month",
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