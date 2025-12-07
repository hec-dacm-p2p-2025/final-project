import pandas as pd

def extract_official_rates(df):
    """
    Produces a standardized DataFrame:
    - currency
    - official_exchange_rate

    Rules:
    - For EUR, GBP, CNY, JPY, MXN, ARS → use tipo_cambio_me
    - For BOB → take tipo_cambio_bs from USD.VENTA row
    """

    target_fx = ["EUR", "GBP", "CNY", "JPY", "MXN", "ARS"]
    df = df.copy()

    # Extract BOB from USD.VENTA
    usd_to_bob = df.loc[df["currency"] == "USD.VENTA", "tipo_cambio_bs"].iloc[0]

    bob_row = pd.DataFrame([{
        "currency": "BOB",
        "official_exchange_rate": usd_to_bob
    }])

    # Foreign FX using tipo_cambio_me
    fx = df[df["currency"].isin(target_fx)][["currency", "tipo_cambio_me"]]
    fx = fx.rename(columns={"tipo_cambio_me": "official_exchange_rate"})

    out = pd.concat([fx, bob_row], ignore_index=True)

    # Convert to numeric and round with consistent dtype
    out["official_exchange_rate"] = pd.to_numeric(out["official_exchange_rate"], errors="coerce")
    out["official_exchange_rate"] = out["official_exchange_rate"].round(2)

    return out.sort_values("currency").reset_index(drop=True)