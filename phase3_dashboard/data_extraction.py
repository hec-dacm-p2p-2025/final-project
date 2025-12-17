from pathlib import Path
import time
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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

EXPORTS = SCRIPT_DIR / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

PHASE1_ROOT = REPO_ROOT / "phase1_data_pipeline" / "data" / "processed"
MASTER = PHASE1_ROOT / "binance" / "p2p_master.parquet"

if not MASTER.exists():
    raise FileNotFoundError(f"Missing file: {MASTER}")

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "MXN", "ARS", "BOB"]

_start = time.time()
_files = 0


def save_csv(df: pd.DataFrame, rel_path: str) -> None:
    global _files
    out = EXPORTS / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    _files += 1

daily = fiat_comparison(currencies=CURRENCIES, root=PHASE1_ROOT)
save_csv(daily, "daily_fiat_comparison/fiat_comparison.csv")

for ccy in CURRENCIES:
    df = intraday_profile(currency=ccy, root=PHASE1_ROOT)
    save_csv(df, f"intraday_profile_by_currency/{ccy}_intraday_profile.csv")

for ccy in CURRENCIES:
    df = p2p_spread(currency=ccy, by="hour", root=PHASE1_ROOT)
    save_csv(df, f"p2p_spread_by_currency/{ccy}_p2p_spread.csv")

for ccy in CURRENCIES:
    df = official_premium(currency=ccy, by="day", root=PHASE1_ROOT)
    save_csv(df, f"official_premium_by_currency/{ccy}_official_premium.csv")

for ccy in CURRENCIES:
    df = order_imbalance(currency=ccy, by="hour", root=PHASE1_ROOT)
    save_csv(df, f"order_imbalance_by_currency/{ccy}_order_imbalance.csv")

for ccy in CURRENCIES:
    df = price_volatility(currency=ccy, by="day", window=7, root=PHASE1_ROOT)
    save_csv(df, f"price_volatility_by_currency/{ccy}_price_volatility.csv")

for ccy in CURRENCIES:
    df = top_advertisers(currency=ccy, root=PHASE1_ROOT)
    save_csv(df, f"top_advertisers_by_currency/{ccy}_top_advertisers.csv")

summary = p2p_summary(currencies=CURRENCIES, root=PHASE1_ROOT)
save_csv(summary, "p2p_summary.csv")

runtime = time.time() - _start

print("=== Phase 3 Extraction completed ===")
print(f"[Phase3] CSV exports updated ({_files} files) — ready for Streamlit consumption.")
print(f"[Phase3] Runtime: {runtime:.2f} seconds")