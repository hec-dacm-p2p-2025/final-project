# phase3_dashboard/data_extraction.py

from pathlib import Path
import pandas as pd

from p2p_analytics import (
    fiat_comparison,
    intraday_profile,
    p2p_spread,
    official_premium,
    order_imbalance,
    p2p_summary,
    price_volatility,
    top_advertisers,
)

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

EXPORTS = SCRIPT_DIR / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

# IMPORTANT: your installed p2p_analytics expects root == phase1_data_pipeline/data/processed
PHASE1_ROOT = REPO_ROOT / "phase1_data_pipeline" / "data" / "processed"

MASTER = PHASE1_ROOT / "binance" / "p2p_master.parquet"
print("[path] PHASE1_ROOT =", PHASE1_ROOT)
print("[path] EXPORTS     =", EXPORTS)
print("[path] MASTER      =", MASTER)

if not MASTER.exists():
    raise FileNotFoundError(f"Missing file: {MASTER}")


def save_csv(df: pd.DataFrame, rel_path: str) -> None:
    out = EXPORTS / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"[saved] {out}")


CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "MXN", "ARS", "BOB"]

# Daily Fiat Comparison
daily_fiat_comparison = fiat_comparison(currencies=CURRENCIES, root=PHASE1_ROOT)
save_csv(daily_fiat_comparison, "daily_fiat_comparison/fiat_comparison.csv")

# Intraday Profile
for ccy in CURRENCIES:
    df = intraday_profile(currency=ccy, root=PHASE1_ROOT)
    save_csv(df, f"intraday_profile_by_currency/{ccy}_intraday_profile.csv")

# P2P Spread
for ccy in CURRENCIES:
    df = p2p_spread(currency=ccy, by="hour", root=PHASE1_ROOT)
    save_csv(df, f"p2p_spread_by_currency/{ccy}_p2p_spread.csv")

# Premium vs Official
for ccy in CURRENCIES:
    df = official_premium(currency=ccy, by="day", root=PHASE1_ROOT)
    save_csv(df, f"official_premium_by_currency/{ccy}_official_premium.csv")

# Order imbalance
for ccy in CURRENCIES:
    df = order_imbalance(currency=ccy, by="hour", root=PHASE1_ROOT)
    save_csv(df, f"order_imbalance_by_currency/{ccy}_order_imbalance.csv")

# Volatility
for ccy in CURRENCIES:
    df = price_volatility(currency=ccy, by="day", window=7, root=PHASE1_ROOT)
    save_csv(df, f"price_volatility_by_currency/{ccy}_price_volatility.csv")

# Top advertisers
for ccy in CURRENCIES:
    df = top_advertisers(currency=ccy, root=PHASE1_ROOT)
    save_csv(df, f"top_advertisers_by_currency/{ccy}_top_advertisers.csv")

# Summary (fix)
summary_df = p2p_summary(currencies=CURRENCIES, root=PHASE1_ROOT)
save_csv(summary_df, "p2p_summary.csv")