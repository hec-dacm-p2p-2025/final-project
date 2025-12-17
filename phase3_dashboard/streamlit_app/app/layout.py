import pandas as pd
import streamlit as st

from app import CURRENCIES
from app.data import (
    load_daily_fiat_comparison,
    load_intraday,
    load_official_premium,
    load_order_imbalance,
    load_spread_hour,
    load_price_volatility,
    load_top_advertisers,
    load_p2p_summary,
)
from app.viz import (
    overview_spreads_chart,
    intraday_profile_chart,
    official_premium_chart,
    order_imbalance_heatmap,
    p2p_spread_heatmap,
    price_volatility_chart,
    top_advertisers_ads_chart,
    top_advertisers_volume_chart,
    intraday_mean_over_range,
)

# ==============================================================================
# Cached helper functions (pure transforms)
# ==============================================================================

@st.cache_data
def _normalize_date_col(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()
    return df

@st.cache_data
def _filter_by_date(df: pd.DataFrame, start, end, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.normalize()
    return df[(df[date_col] >= start) & (df[date_col] <= end)].copy()

@st.cache_data
def _format_preview(df: pd.DataFrame, date_col: str = "date", currency_last: bool = True) -> pd.DataFrame:
    preview = df.copy()
    if date_col in preview.columns:
        preview[date_col] = pd.to_datetime(preview[date_col]).dt.date

    if currency_last and "currency" in preview.columns:
        preview = preview[[c for c in preview.columns if c != "currency"] + ["currency"]]

    return preview

@st.cache_data
def thousand_sep_config(df: pd.DataFrame) -> dict:
    cfg = {}
    for col in df.columns:
        s = pd.to_numeric(df[col], errors="coerce")
        if s.notna().sum() == 0:
            continue
        if (s.abs() >= 1000).any():
            cfg[col] = st.column_config.NumberColumn(format="localized")
    return cfg

@st.cache_data
def _intraday_to_long(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hour"] = df["hour"].astype(int)

    df_long = df.melt(
        id_vars="hour",
        value_vars=["mean_buy_price", "mean_sell_price"],
        var_name="side",
        value_name="price",
    )
    df_long["side"] = df_long["side"].map({"mean_buy_price": "Buy", "mean_sell_price": "Sell"})
    return df_long


# ==============================================================================
# Optional fragment wrapper to reduce unnecessary reruns
# ==============================================================================

try:
    _fragment = st.experimental_fragment  # available in newer streamlit
except Exception:
    _fragment = None

if _fragment:
    @_fragment
    def _show_chart(chart) -> None:
        st.altair_chart(chart, width='stretch')
else:
    def _show_chart(chart) -> None:
        st.altair_chart(chart, width='stretch')


# ==============================================================================
# Render functions
# ==============================================================================

def render_spread_overview() -> None:
    st.subheader("1. Spread Overview by Currency")
    st.markdown(
        """
        This view compares the **Daily P2P Spread** between Buy and Sell prices across currencies.
        A higher spread can indicate a less competitive or more segmented market.
        """
    )

    df = load_daily_fiat_comparison()
    if df.empty:
        st.info("No data to display.")
        return

    df = _normalize_date_col(df, "date")

    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.slider(
        "Select Date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="spread_overview_date_slider",
    )
    df = _filter_by_date(df, date_range[0], date_range[1], "date")

    all_currencies = sorted(df["currency"].dropna().unique())
    selected = st.multiselect(
        "Select currencies to display",
        options=all_currencies,
        default=all_currencies,
        key="spread_overview_currency_multiselect",
    )
    if not selected:
        st.info("Please select at least one currency.")
        return

    df = df[df["currency"].isin(selected)].copy()
    _show_chart(overview_spreads_chart(df))

    st.markdown("Preview of the underlying data:")
    preview = df.copy()
    preview["date"] = pd.to_datetime(preview["date"]).dt.date
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview.tail(20)), width='stretch', column_config=thousand_sep_config(preview))


def render_intraday_profile() -> None:
    st.subheader("2.1 Intraday Profile")
    st.markdown(
        """
        a. Select a **Currency**.

        b. Select a **Date** range.  
        
        We compute the **mean BUY/SELL price per hour** over that range and plot the intraday profile.
        """
    )

    currency = st.selectbox("Select Currency", CURRENCIES, key="intraday_currency_select")

    df = load_spread_hour(currency)
    if df.empty:
        st.info("No data to display.")
        return

    needed = {"date", "hour", "avg_buy_price", "avg_sell_price"}
    if not needed.issubset(df.columns):
        st.info("Unexpected intraday columns. Showing raw data.")
        st.dataframe(df.head(), width='stretch')
        return

    # Parse dates to get min/max for date picker
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["date"])
    min_d, max_d = df["date"].min(), df["date"].max()

    # Default: last 7 days available
    default_start = max(min_d, max_d - pd.Timedelta(days=6))

    start_d, end_d = st.date_input(
        "Select Date range",
        value=(default_start, max_d),
        min_value=min_d,
        max_value=max_d,
        key="intraday_date_range",
    )

    # Aggregate hourly curve over selected days
    df_hourly = intraday_mean_over_range(df, start_d, end_d)
    if df_hourly.empty:
        st.info("No observations in that date range.")
        return

    # Hour slider AFTER aggregation
    min_hour, max_hour = int(df_hourly["hour"].min()), int(df_hourly["hour"].max())
    hour_range = st.slider(
        "Select hour range",
        min_value=min_hour,
        max_value=max_hour,
        value=(min_hour, max_hour),
        key="intraday_hour_slider",
    )
    df_hourly = df_hourly[(df_hourly["hour"] >= hour_range[0]) & (df_hourly["hour"] <= hour_range[1])].copy()

    # Plot using your existing chart
    df_long = _intraday_to_long(df_hourly)
    chart = intraday_profile_chart(df_long).properties(
        width="container",
        title=f"{currency} — Hourly BUY/SELL mean prices ({start_d} → {end_d})"
    )
    _show_chart(chart)

    st.markdown("_Summary statistics (hourly curve):_")
    st.caption(
        f"**Buy** – min: {df_hourly['mean_buy_price'].min():.2f}, "
        f"mean: {df_hourly['mean_buy_price'].mean():.2f}, "
        f"max: {df_hourly['mean_buy_price'].max():.2f}"
    )
    st.caption(
        f"**Sell** – min: {df_hourly['mean_sell_price'].min():.2f}, "
        f"mean: {df_hourly['mean_sell_price'].mean():.2f}, "
        f"max: {df_hourly['mean_sell_price'].max():.2f}"
    )

    st.markdown("**Raw data (selected window)**")
    df_win = df[(df["date"] >= start_d) & (df["date"] <= end_d)].copy()
    preview = df_win.copy()
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview.tail(20)), width='stretch', height=220, column_config=thousand_sep_config(preview))


def render_official_premium() -> None:
    st.subheader("2.2 Official Premium")
    st.markdown("Difference between P2P rate and Official Exchange Rate (percentage or absolute).")

    currency = st.selectbox("Select Currency", CURRENCIES, key="premium_currency_select")
    cur = currency.upper()

    if cur == "USD":
        st.info(
            "USD is the reference currency, so the official premium is defined as 0%. "
            "No premium time series to display."
        )
        return

    prem = load_official_premium(cur)
    if prem.empty:
        st.warning(f"No official premium data available for {cur}.")
        return

    prem = _normalize_date_col(prem, "date")

    min_date, max_date = prem["date"].min(), prem["date"].max()
    date_range = st.slider(
        "Select Date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_official_premium_slider",
    )
    prem = _filter_by_date(prem, date_range[0], date_range[1], "date").sort_values("date")

    metric_label = st.radio(
        "Metric",
        options=["Premium (%)", "Premium (absolute)"],
        horizontal=True,
        key="official_premium_metric",
    )
    metric = "premium_pct" if metric_label == "Premium (%)" else "premium_abs"

    _show_chart(official_premium_chart(prem, metric=metric))

    st.markdown("Preview of Official Premium data:")
    preview = prem.copy()
    preview["date"] = pd.to_datetime(preview["date"]).dt.date
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview.tail(20)), width='stretch', column_config=thousand_sep_config(preview))


def render_order_imbalance() -> None:
    st.subheader("2.3 Order Imbalance")

    currency = st.selectbox("Select Currency", CURRENCIES, key="order_imbalance_select")

    df_imbalance = load_order_imbalance(currency)
    if df_imbalance.empty:
        st.info("No data to display for this currency.")
        return

    df_imbalance = _normalize_date_col(df_imbalance, "date")

    min_date, max_date = df_imbalance["date"].min(), df_imbalance["date"].max()
    date_range = st.slider(
        "Select Date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_order_imbalance_slider",
    )
    df_imbalance = _filter_by_date(df_imbalance, date_range[0], date_range[1], "date")

    _show_chart(order_imbalance_heatmap(df_imbalance))

    st.markdown("Preview of the underlying data:")
    preview = df_imbalance.copy()
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview).tail(20), width='stretch', column_config=thousand_sep_config(preview))


def render_spread_heatmap() -> None:
    st.subheader("2.4 P2P Spread (hour × day)")

    currency = st.selectbox("Select Currency", CURRENCIES, key="p2p_spread_select")

    df_spread = load_spread_hour(currency)
    if df_spread.empty:
        st.info("No data to display for this currency.")
        return

    df_spread = _normalize_date_col(df_spread, "date")

    min_date, max_date = df_spread["date"].min(), df_spread["date"].max()
    date_range = st.slider(
        "Select Date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_spread_heatmap_slider",
    )
    df_spread = _filter_by_date(df_spread, date_range[0], date_range[1], "date")

    metric_label = st.radio(
        "Metric",
        options=["Spread (%)", "Spread (absolute)"],
        horizontal=True,
        key="spread_heatmap_metric",
    )
    metric = "spread_pct" if metric_label == "Spread (%)" else "spread_abs"

    _show_chart(p2p_spread_heatmap(df_spread, metric=metric))

    st.markdown("Preview of the underlying data:")
    preview = df_spread.copy()
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview).tail(20), width='stretch', column_config=thousand_sep_config(preview))


def render_price_volatility() -> None:
    st.subheader("2.5 Price Volatility (7 days window).")

    currency = st.selectbox("Select Currency", CURRENCIES, key="price_volatility_select")

    df_volatility = load_price_volatility(currency)
    if df_volatility.empty:
        st.info("No volatility data to display for this currency.")
        return

    df_volatility = _normalize_date_col(df_volatility, "date")

    min_date, max_date = df_volatility["date"].min(), df_volatility["date"].max()
    date_range = st.slider(
        "Select Data range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_price_volatility_slider",
    )
    df_volatility = _filter_by_date(df_volatility, date_range[0], date_range[1], "date")

    _show_chart(price_volatility_chart(df_volatility))

    st.markdown("Preview of volatility data:")
    preview = df_volatility.copy()
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview).tail(20), width='stretch', column_config=thousand_sep_config(preview))


def render_top_advertisers() -> None:
    st.subheader("2.6 Top Advertisers")
    st.markdown("Highlights the largest P2P advertisers by advertised amount.")

    currency = st.selectbox("Select Currency", CURRENCIES, key="top_ads_currency_select")

    df_ads = load_top_advertisers(currency)
    if df_ads.empty:
        st.info("No advertiser data available for this currency.")
        return

    df_ads = df_ads.drop(
        columns=[col for col in df_ads.columns if col.lower().startswith("unnamed")],
        errors="ignore",
    )

    required_cols = {"merchant_name", "ads_count", "total_volume"}
    if not required_cols.issubset(df_ads.columns):
        st.info("Expected columns not found. Showing raw data instead.")
        st.dataframe(df_ads.head(50), width='stretch')
        return

    df_agg = (
        df_ads.groupby("merchant_name", as_index=False)
        .agg(
            total_volume=("total_volume", "sum"),
            total_ads=("ads_count", "sum"),
            avg_finish_rate=("avg_finish_rate", "mean"),
            avg_positive_rate=("avg_positive_rate", "mean"),
        )
    )
    df_top = df_agg.sort_values("total_volume", ascending=False).tail(20)

    metric = st.radio(
        "Metric",
        ["Total volume", "Number of ads"],
        horizontal=True,
        key="top_ads_metric",
    )

    if metric == "Total volume":
        _show_chart(top_advertisers_volume_chart(df_top, currency))
    else:
        _show_chart(top_advertisers_ads_chart(df_top, currency))

    st.markdown("Full advertiser table (first rows):")
    preview = df_ads.copy()
    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)
    st.dataframe(_format_preview(preview.tail(20)), width='stretch', column_config=thousand_sep_config(preview))


def render_summary_table() -> None:
    st.subheader("3. P2P Summary Table")

    df = load_p2p_summary().copy()
    st.markdown("**High-level summary of P2P prices and spreads**")

    if df.empty:
        st.info("No data to display.")
        return

    df = _normalize_date_col(df, "date")

    # Currency selector
    if "currency" in df.columns:
        all_currencies = sorted(df["currency"].dropna().unique())
        selected = st.multiselect(
            "Select currencies",
            options=all_currencies,
            default=all_currencies,
            key="summary_currency_multiselect",
        )
        if not selected:
            st.info("Please select at least one currency.")
            return
        df = df[df["currency"].isin(selected)].copy()

    # Date range selector
    if "date" in df.columns:
        min_date, max_date = df["date"].min(), df["date"].max()
        date_range = st.slider(
            "Select Date range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            key="summary_date_slider",
        )
        df = _filter_by_date(df, date_range[0], date_range[1], "date")

    preview = _format_preview(df).tail(50).copy()

    num_cols = preview.select_dtypes(include="number").columns
    preview[num_cols] = preview[num_cols].round(2)

    st.dataframe(preview, width="stretch", column_config=thousand_sep_config(preview))
