from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st


# ----------------------------------------------------
# Export paths
# ----------------------------------------------------
# .../phase3_dashboard/streamlit_app/app/__init__.py
APP_DIR = Path(__file__).resolve().parent              # streamlit_app/app
STREAMLIT_APP_DIR = APP_DIR.parent                     # streamlit_app
PROJECT_ROOT = STREAMLIT_APP_DIR.parent                # phase3_dashboard
EXPORTS_DIR = PROJECT_ROOT / "exports"

PATH_DAILY_FIAT = EXPORTS_DIR / "daily_fiat_comparison"
PATH_INTRADAY = EXPORTS_DIR / "intraday_profile_by_currency"
PATH_PREMIUM = EXPORTS_DIR / "official_premium_by_currency"
PATH_ORDER_IMB = EXPORTS_DIR / "order_imbalance_by_currency"
PATH_P2P_DAY = EXPORTS_DIR / "p2p_spread_by_currency" / "day"
PATH_P2P_HOUR = EXPORTS_DIR / "p2p_spread_by_currency" / "hour"
PATH_VOL = EXPORTS_DIR / "price_volatility_by_currency"
PATH_TOP_ADS = EXPORTS_DIR / "top_advertisers_by_currency"
PATH_P2P_SUMMARY = EXPORTS_DIR / "p2p_summary.csv"

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "MXN", "ARS", "BOB"]


def _read_csv(path: Path, parse_date_cols: list[str] | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    if parse_date_cols:
        for col in parse_date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
    return df


@st.cache_data
def load_daily_fiat_comparison() -> pd.DataFrame:
    path = PATH_DAILY_FIAT / "fiat_comparison.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_intraday(currency: str) -> pd.DataFrame:
    path = PATH_INTRADAY / f"{currency}_intraday_profile.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path)


@st.cache_data
def load_spread_day(currency: str) -> pd.DataFrame:
    path = PATH_P2P_DAY / f"{currency}_p2p_spread.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_spread_hour(currency: str) -> pd.DataFrame:
    path = PATH_P2P_HOUR / f"{currency}_p2p_spread.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_official_premium(currency: str) -> pd.DataFrame:
    path = PATH_PREMIUM / f"{currency}_official_premium.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_price_volatility(currency: str) -> pd.DataFrame:
    path = PATH_VOL / f"{currency}_price_volatility.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_order_imbalance(currency: str) -> pd.DataFrame:
    path = PATH_ORDER_IMB / f"{currency}_order_imbalance.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_top_advertisers(currency: str) -> pd.DataFrame:
    path = PATH_TOP_ADS / f"{currency}_top_advertisers.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(path, parse_date_cols=["date"])


@st.cache_data
def load_p2p_summary() -> pd.DataFrame:
    return _read_csv(PATH_P2P_SUMMARY, parse_date_cols=["date"])
