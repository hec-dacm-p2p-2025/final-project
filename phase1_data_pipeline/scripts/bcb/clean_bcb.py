import pandas as pd

def clean_bcb_table(df):
    """
    Cleans numeric fields and normalizes the raw BCB table.
    """

    df = df.copy()

    for col in ["tipo_cambio_bs", "tipo_cambio_me"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df