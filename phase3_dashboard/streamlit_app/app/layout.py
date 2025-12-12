import pandas as pd
import streamlit as st

from app import CURRENCIES
from app.data import (
    load_daily_fiat_comparison,
    load_intraday,
    load_official_premium,
    load_p2p_summary,
    load_top_advertisers,
)
from app.viz import (
    overview_spreads_chart,
    intraday_profile_chart,
    official_premium_chart,
    top_advertisers_ads_chart,
    top_advertisers_volume_chart,
)


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
    st.dataframe(df.head(30), use_container_width=True)


def render_intraday_profile() -> None:
    st.subheader("2. Intraday profile")
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

    ""
    
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


def render_official_premium() -> None:
    st.subheader("3. Official premium")
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

    prem = prem.sort_values("date").copy()
    st.altair_chart(official_premium_chart(prem), use_container_width=True)

    st.markdown("Preview of official premium data:")
    cols = ["date", "currency", "p2p_avg_price", "official_exchange_rate", "premium_abs", "premium_pct"]
    st.dataframe(prem[cols].head(), use_container_width=True)


def render_top_advertisers() -> None:
    st.subheader("4. Top advertisers")
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


def render_summary_table() -> None:
    st.subheader("5. P2P summary table")
    df = load_p2p_summary()
    st.markdown("**High-level summary of P2P prices and spreads**")
    st.dataframe(df.head(50), use_container_width=True)
