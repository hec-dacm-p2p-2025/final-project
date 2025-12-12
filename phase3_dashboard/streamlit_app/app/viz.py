import altair as alt
import pandas as pd


def overview_spreads_chart(df: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("spread_pct:Q", title="Spread (%)"),
            color=alt.Color("currency:N", title="Currency"),
            tooltip=[
                "date:T",
                "currency:N",
                alt.Tooltip("spread_pct:Q", title="Spread (%)", format=".2f"),
            ],
        )
        .properties(height=400, title="Daily P2P spread (%) by currency")
    )


def intraday_profile_chart(df_long: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(df_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("hour:Q", title="Hour of day"),
            y=alt.Y("price:Q", title="Average price"),
            color=alt.Color("side:N", title=""),
            tooltip=["hour", "side", alt.Tooltip("price:Q", format=".2f")],
        )
        .properties(height=400)
    )


def official_premium_chart(prem: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(prem)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("premium_pct:Q", title="Official premium (%)"),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("premium_pct:Q", title="Official premium (%)", format=".2f"),
                alt.Tooltip("p2p_avg_price:Q", title="P2P average price", format=".2f"),
                alt.Tooltip("official_exchange_rate:Q", title="Official rate", format=".2f"),
            ],
        )
        .properties(height=400, width="container")
    )


def top_advertisers_volume_chart(df_top: pd.DataFrame, currency: str) -> alt.Chart:
    base = alt.Chart(df_top).encode(
        y=alt.Y("merchant_name:N", sort="-x", title="Advertiser")
    )
    return (
        base.mark_bar()
        .encode(
            x=alt.X("total_volume:Q", title="Total volume"),
            tooltip=[
                alt.Tooltip("merchant_name:N", title="Advertiser"),
                alt.Tooltip("total_volume:Q", title="Total volume", format=".2f"),
                alt.Tooltip("total_ads:Q", title="Number of ads"),
                alt.Tooltip("avg_finish_rate:Q", title="Avg. finish rate", format=".2%"),
                alt.Tooltip("avg_positive_rate:Q", title="Avg. positive rate", format=".2%"),
            ],
        )
        .properties(title=f"Top advertisers by total volume – {currency}", height=300)
    )


def top_advertisers_ads_chart(df_top: pd.DataFrame, currency: str) -> alt.Chart:
    base = alt.Chart(df_top).encode(
        y=alt.Y("merchant_name:N", sort="-x", title="Advertiser")
    )
    return (
        base.mark_bar()
        .encode(
            x=alt.X("total_ads:Q", title="Number of ads"),
            tooltip=[
                alt.Tooltip("merchant_name:N", title="Advertiser"),
                alt.Tooltip("total_ads:Q", title="Number of ads"),
                alt.Tooltip("total_volume:Q", title="Total volume", format=".2f"),
                alt.Tooltip("avg_finish_rate:Q", title="Avg. finish rate", format=".2%"),
                alt.Tooltip("avg_positive_rate:Q", title="Avg. positive rate", format=".2%"),
            ],
        )
        .properties(title=f"Top advertisers by number of ads – {currency}", height=300)
    )