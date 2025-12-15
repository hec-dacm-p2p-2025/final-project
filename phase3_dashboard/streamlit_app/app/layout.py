import pandas as pd
import streamlit as st

from app import CURRENCIES
from app.data import (
    load_daily_fiat_comparison,
    load_intraday,
    load_official_premium,
    load_order_imbalance,
    load_spread_day,
    load_spread_hour,
    load_price_volatility,
    load_top_advertisers,
    load_p2p_summary,
)
from app.viz import (
    overview_spreads_chart,
    intraday_profile_chart,
    official_premium_absolute_chart,
    official_premium_percentage_chart,
    order_imbalance_heatmap,
    p2p_spread_heatmap,
    price_volatility_chart,
    top_advertisers_ads_chart,
    top_advertisers_volume_chart,
)

# ------------------------------------------------------------------------------
def render_spread_overview() -> None:
    st.subheader("1. Spread overview by currency")
    st.markdown(
        """
        This view compares the **daily P2P spread** between buy and sell prices across currencies.
        A higher spread can indicate a less competitive or more segmented market.
        """
    )

    df = load_daily_fiat_comparison()
    if df.empty:
        st.info("No data to display.")
        return

    min_date, max_date = df["date"].min(), df["date"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="spread_overview_date_slider",
    )
    mask = (df["date"] >= date_range[0]) & (df["date"] <= date_range[1])
    df = df.loc[mask].copy()

    all_currencies = sorted(df["currency"].unique())
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
    st.altair_chart(overview_spreads_chart(df), use_container_width=True)

    st.markdown("Preview of the underlying data:")
    preview = df.copy()
    preview["date"] = pd.to_datetime(preview["date"]).dt.date
    cols = ["date", "avg_buy_price", "avg_sell_price", "spread_abs", "spread_pct", "currency"]
    preview = preview[cols]
    st.dataframe(preview.head(30), use_container_width=True)

# ------------------------------------------------------------------------------
def render_intraday_profile() -> None:
    st.subheader("2.1 Intraday profile")
    st.markdown(
        """
        Average BUY and SELL prices by hour of day for the selected currency.
        Helps spot intraday patterns in pricing and spreads.
        """
    )

    currency = st.selectbox("Select currency", CURRENCIES, key="intraday_currency_select")

    df = load_intraday(currency).copy()
    needed = {"hour", "mean_buy_price", "mean_sell_price"}
    if not needed.issubset(df.columns):
        st.info("Unexpected intraday columns. Showing raw data.")
        st.dataframe(df.head(), use_container_width=True)
        return
    
    df["hour"] = df["hour"].astype(int)
    
    min_hour, max_hour = int(df["hour"].min()), int(df["hour"].max())

    hour_range = st.slider(
        "Select hour range",
        min_value=min_hour,
        max_value=max_hour,
        value=(min_hour, max_hour),
        key="intraday_hour_slider",
    )

    mask = (df["hour"] >= hour_range[0]) & (df["hour"] <= hour_range[1])
    df = df.loc[mask].copy()


    df_long = df.melt(
        id_vars="hour",
        value_vars=["mean_buy_price", "mean_sell_price"],
        var_name="side",
        value_name="price",
    )
    df_long["side"] = df_long["side"].map(
        {"mean_buy_price": "Buy", "mean_sell_price": "Sell"}
    )

    st.altair_chart(intraday_profile_chart(df_long), use_container_width=True)
    
    st.markdown("_Summary statistics:_")
    st.caption(
        f"**Buy price** – min: {df['mean_buy_price'].min():.2f}, "
        f"mean: {df['mean_buy_price'].mean():.2f}, "
        f"max: {df['mean_buy_price'].max():.2f}"
    )
    st.caption(
        f"**Sell price** – min: {df['mean_sell_price'].min():.2f}, "
        f"mean: {df['mean_sell_price'].mean():.2f}, "
        f"max: {df['mean_sell_price'].max():.2f}"
    )

    st.markdown("**Raw intraday data**")
    st.dataframe(df, use_container_width=True, height=220)

# ------------------------------------------------------------------------------
def render_official_premium() -> None:
    st.subheader("2.2 Official premium")
    st.markdown(
        """
        Percentage difference between P2P rate and official exchange rate.
        """
    )

    currency = st.selectbox("Select currency", CURRENCIES, key="premium_currency_select")
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
    
    min_date, max_date = prem["date"].min(), prem["date"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_official_premium_slider",
    )
    mask = (prem["date"] >= date_range[0]) & (prem["date"] <= date_range[1])
    prem = prem.loc[mask].copy()

    prem = prem.sort_values("date").copy()
    st.altair_chart(official_premium_absolute_chart(prem), use_container_width=True)
    st.altair_chart(official_premium_percentage_chart(prem), use_container_width=True)


    st.markdown("Preview of official premium data:")
    preview = prem.copy()
    preview["date"] = pd.to_datetime(preview["date"]).dt.date
    cols = ["date", "p2p_avg_price", "official_exchange_rate", "premium_abs", "premium_pct", "currency"]
    preview = preview[cols]
    st.dataframe(preview.head(), use_container_width=True)

# ------------------------------------------------------------------------------
def render_order_imbalance() -> None:
    st.subheader("2.3 Order imbalance")

    currency = st.selectbox("Select currency", CURRENCIES, key="order_imbalance_select")

    df_imbalance = load_order_imbalance(currency)
    if df_imbalance.empty:
        st.info("No advertiser data available for this currency.")
        return
    
    min_date, max_date = df_imbalance["date"].min(), df_imbalance["date"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_order_imbalance_slider",
    )
    mask = (df_imbalance["date"] >= date_range[0]) & (df_imbalance["date"] <= date_range[1])
    df_imbalance = df_imbalance.loc[mask].copy()

    st.altair_chart(order_imbalance_heatmap(df_imbalance), use_container_width=True)

    st.markdown("Preview of the underlying data:")
    preview = df_imbalance.copy()
    if "date" in preview.columns:
        preview["date"] = pd.to_datetime(preview["date"]).dt.date

    if "currency" in preview.columns:
        cols = [c for c in preview.columns if c != "currency"] + ["currency"]
        preview = preview[cols]
    st.dataframe(preview.head(50), use_container_width=True)

# ------------------------------------------------------------------------------
def render_spread_heatmap() -> None:
    st.subheader("2.4 P2P spread")

    currency = st.selectbox("Select currency", CURRENCIES, key="p2p_spread_select")

    df_spread = load_spread_hour(currency)
    if df_spread.empty:
        st.info("No advertiser data available for this currency.")
        return
    
    min_date, max_date = df_spread["date"].min(), df_spread["date"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_spread_heatmap_slider",
    )
    mask = (df_spread["date"] >= date_range[0]) & (df_spread["date"] <= date_range[1])
    df_spread = df_spread.loc[mask].copy()

    metric_label = st.radio(
        "Metric",
        options=["Spread (%)", "Spread (absolute)"],
        horizontal=True,
        key="spread_heatmap_metric",
    )
    metric = "spread_pct" if metric_label == "Spread (%)" else "spread_abs"

    st.altair_chart(p2p_spread_heatmap(df_spread, metric=metric), use_container_width=True)

    st.markdown("Preview of the underlying data:")
    preview = df_spread.copy()
    if "date" in preview.columns:
        preview["date"] = pd.to_datetime(preview["date"]).dt.date

    if "currency" in preview.columns:
        cols = [c for c in preview.columns if c != "currency"] + ["currency"]
        preview = preview[cols]
    st.dataframe(preview.head(50), use_container_width=True)


# ------------------------------------------------------------------------------
def render_price_volatility() -> None:
    st.subheader("2.5 Price volatility with a 7 day rolling window")

    currency = st.selectbox("Select currency", CURRENCIES, key="price_volatility_select")

    df_volatility = load_price_volatility(currency)
    if df_volatility.empty:
        st.info("No data to display.")
        return

    df_volatility["date"] = pd.to_datetime(df_volatility["date"]).dt.normalize()

    min_date, max_date = df_volatility["date"].min(), df_volatility["date"].max()
    date_range = st.slider(
        "Select date range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        key="render_price_volatility_slider",
    )
    mask = (df_volatility["date"] >= date_range[0]) & (df_volatility["date"] <= date_range[1])
    df_volatility = df_volatility.loc[mask].copy()

    st.altair_chart(price_volatility_chart(df_volatility), use_container_width=True)

    st.markdown("Preview of volatility data:")
    preview = df_volatility.copy()
    if "date" in preview.columns:
        preview["date"] = pd.to_datetime(preview["date"]).dt.date

    if "currency" in preview.columns:
        cols = [c for c in preview.columns if c != "currency"] + ["currency"]
        preview = preview[cols]
    st.dataframe(preview.head(50), use_container_width=True)


# ------------------------------------------------------------------------------
def render_top_advertisers() -> None:
    st.subheader("2.6 Top advertisers")
    st.markdown(
        """
        Highlights the largest P2P advertisers by advertised amount.
        """
    )

    currency = st.selectbox("Select currency", CURRENCIES, key="top_ads_currency_select")

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
        st.dataframe(df_ads.head(50), use_container_width=True)
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
    df_top = df_agg.sort_values("total_volume", ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(top_advertisers_volume_chart(df_top, currency), use_container_width=True)
    with col2:
        st.altair_chart(top_advertisers_ads_chart(df_top, currency), use_container_width=True)

    st.markdown("Full advertiser table (first rows):")
    st.dataframe(df_ads.head(50), use_container_width=True)

# ------------------------------------------------------------------------------
def render_summary_table() -> None:
    st.subheader("3. P2P summary table")

    df = load_p2p_summary().copy()
    st.markdown("**High-level summary of P2P prices and spreads**")

    if df.empty:
        st.info("No data to display.")
        return

    # --- Clean date + remove hours
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    # --- Currency selector
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

    # --- Date range selector
    if "date" in df.columns:
        min_date, max_date = df["date"].min(), df["date"].max()
        date_range = st.slider(
            "Select date range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            key="summary_date_slider",
        )
        df = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])].copy()

    # --- Preview formatting: date as date only, currency last
    preview = df.copy()
    if "date" in preview.columns:
        preview["date"] = pd.to_datetime(preview["date"]).dt.date

    if "currency" in preview.columns:
        cols = [c for c in preview.columns if c != "currency"] + ["currency"]
        preview = preview[cols]

    st.dataframe(preview.head(50), use_container_width=True)
