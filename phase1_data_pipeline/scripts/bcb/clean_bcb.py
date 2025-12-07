import pandas as pd

def clean_bcb_table(df):
    df = df.copy()

    # Fix numeric columns
    for col in ["tipo_cambio_bs", "tipo_cambio_me"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.replace(" ", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fix datetime formats (NO columns added)
    if "scrape_datetime" in df.columns:
        df["scrape_datetime"] = pd.to_datetime(df["scrape_datetime"], errors="coerce")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    # Fix time if exists (keep HH:MM)
    if "time" in df.columns:
        df["time"] = (
            pd.to_datetime(df["time"], errors="coerce")
            .dt.strftime("%H:%M")
        )

    # Convert year / month / day to integers
    for col in ["year", "month", "day"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Normalize year-month label
    if "year_month" in df.columns:
        df["year_month"] = (
            pd.to_datetime(df["year_month"], errors="coerce")
            .dt.strftime("%Y-%m")
        )

    return df