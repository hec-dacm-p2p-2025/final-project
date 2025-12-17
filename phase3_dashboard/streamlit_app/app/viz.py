import altair as alt
import pandas as pd

# ------------------------------------------------------------------------------
def overview_spreads_chart(df: pd.DataFrame) -> alt.Chart:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()  # midnight

    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "yearmonthdate(date):T",
                title="Date",
                axis=alt.Axis(format="%b %d")  # e.g., Dec 07
            ),
            y=alt.Y("spread_pct:Q", title="Spread (%)"),
            color=alt.Color("currency:N", title="Currency"),
            tooltip=[
                alt.Tooltip("yearmonthdate(date):T", title="Date"),
                "currency:N",
                alt.Tooltip("spread_pct:Q", title="Spread (%)", format=".2f"),
            ],
        )
        .properties(height=400, 
                    width="container",
                    title="Daily P2P Spread (%) by Currency"
                    )
    )

# ------------------------------------------------------------------------------
def intraday_mean_over_range(df: pd.DataFrame, start_d, end_d) -> pd.DataFrame:
    """
    Input expected columns:
      date, hour, avg_buy_price, avg_sell_price
    Output:
      hour, mean_buy_price, mean_sell_price
    """
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce").astype("Int64")
    df["avg_buy_price"] = pd.to_numeric(df["avg_buy_price"], errors="coerce")
    df["avg_sell_price"] = pd.to_numeric(df["avg_sell_price"], errors="coerce")

    df = df.dropna(subset=["date", "hour", "avg_buy_price", "avg_sell_price"])
    df["hour"] = df["hour"].astype(int)

    df = df[(df["date"] >= start_d) & (df["date"] <= end_d)].copy()

    return (
        df.groupby("hour", as_index=False)[["avg_buy_price", "avg_sell_price"]]
          .mean()
          .rename(columns={
              "avg_buy_price": "mean_buy_price",
              "avg_sell_price": "mean_sell_price",
          })
          .sort_values("hour")
    )

def intraday_profile_chart(df_long: pd.DataFrame) -> alt.Chart:
    df_long = df_long.copy()
    df_long["hour"] = pd.to_numeric(df_long["hour"], errors="coerce")
    df_long["price"] = pd.to_numeric(df_long["price"], errors="coerce")

    ymin, ymax = df_long["price"].min(), df_long["price"].max()
    pad = (ymax - ymin) * 0.05 if pd.notna(ymin) and pd.notna(ymax) and ymax > ymin else 0.01

    return (
        alt.Chart(df_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("hour:Q", 
                    title="Hour of Day",
                    axis=alt.Axis(titlePadding=18, tickMinStep=1, values=list(range(24))),
                    scale=alt.Scale(domain=[0, 23], nice=False, clamp=True),
                    ),
            y=alt.Y(
                "price:Q",
                title="Average Price",
                scale=alt.Scale(domain=[ymin - pad, ymax + pad], nice=False)
            ),
            color=alt.Color(
                "side:N",
                title="",
                legend=alt.Legend(orient="top", direction="horizontal")
            ),
            tooltip=[
                "hour", "side", alt.Tooltip("price:Q", format=".2f")],
        )
        .properties(height=400,
                    title="Hourly BUY/SELL prices by Currency",
                    padding={"bottom": 35},
                    )
    )

# ------------------------------------------------------------------------------
def official_premium_chart(prem: pd.DataFrame, metric: str = "premium_pct") -> alt.Chart:
    prem = prem.copy()
    prem = prem.drop(columns=[c for c in ["Unnamed: 0"] if c in prem.columns])

    prem["date"] = pd.to_datetime(prem["date"]).dt.normalize()

    for c in ["p2p_avg_price", "official_exchange_rate", "premium_abs", "premium_pct"]:
        if c in prem.columns:
            prem[c] = pd.to_numeric(prem[c], errors="coerce")

    # Metric-specific labels
    metric_title = "Premium (%)" if metric == "premium_pct" else "Premium (abs)"
    y_title = "Percentage difference" if metric == "premium_pct" else "Absolute difference"

    ymin, ymax = prem[metric].min(), prem[metric].max()
    pad = (ymax - ymin) * 0.05 if pd.notna(ymin) and pd.notna(ymax) and ymax > ymin else 0.01

    return (
        alt.Chart(prem)
        .mark_line()
        .encode(
            x=alt.X("yearmonthdate(date):T", title="Date", axis=alt.Axis(format="%b %d")),
            y=alt.Y(
                f"{metric}:Q",
                title=y_title,
                scale=alt.Scale(domain=[ymin - pad, ymax + pad], nice=False),
            ),
            tooltip=[
                alt.Tooltip("yearmonthdate(date):T", title="Date"),
                alt.Tooltip("premium_abs:Q", title="Premium (abs)", format=".2f"),
                alt.Tooltip("premium_pct:Q", title="Premium (%)", format=".2f"),
                alt.Tooltip("p2p_avg_price:Q", title="P2P average price", format=".2f"),
                alt.Tooltip("official_exchange_rate:Q", title="Official rate", format=".2f"),
            ],
        )
        .properties(
            height=400,
            title=f"P2P vs Official Exchange Rate ({metric_title})",
            width="container",
        )
    )

# ------------------------------------------------------------------------------
def order_imbalance_heatmap(df: pd.DataFrame) -> alt.Chart:
    df = df.copy()

    # Clean columns + types
    df = df.drop(columns=[c for c in ["Unnamed: 0"] if c in df.columns])
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["hour"] = df["hour"].astype(int)
    df["imbalance"] = pd.to_numeric(df["imbalance"], errors="coerce")

    return (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("yearmonthdate(date):T", title="Date", axis=alt.Axis(format="%b %d")),
            y=alt.Y("hour:O", title="Hour", sort="ascending"),
            color=alt.Color(
                "imbalance:Q",
                title="Imbalance",
                scale=alt.Scale(domainMid=0),  # centers color around 0 (balanced)
            ),
            tooltip=[
                alt.Tooltip("yearmonthdate(date):T", title="Date"),
                alt.Tooltip("hour:O", title="Hour"),
                alt.Tooltip("imbalance:Q", title="Imbalance", format=".3f"),
                alt.Tooltip("buy_volume:Q", title="Buy Volume", format=",.0f"),
                alt.Tooltip("sell_volume:Q", title="Sell Volume", format=",.0f"),
            ],
        )
        .properties(height=420, title="Order Imbalance per Hour and Day")
    )

# ------------------------------------------------------------------------------
def p2p_spread_heatmap(df: pd.DataFrame, metric: str = "spread_pct") -> alt.Chart:
    df = df.copy()
    df = df.drop(columns=[c for c in ["Unnamed: 0"] if c in df.columns])

    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["hour"] = df["hour"].astype(int)

    for c in ["avg_buy_price", "avg_sell_price", "spread_abs", "spread_pct"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    metric_title = "Spread (%)" if metric == "spread_pct" else "Spread (abs)"

    return (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("yearmonthdate(date):T", title="Date", axis=alt.Axis(format="%b %d")),
            y=alt.Y("hour:O", title="Hour", sort="ascending"),
            color=alt.Color(f"{metric}:Q", title=metric_title),
            tooltip=[
                alt.Tooltip("yearmonthdate(date):T", title="Date"),
                alt.Tooltip("hour:O", title="Hour"),
                alt.Tooltip("avg_buy_price:Q", title="Avg Buy", format=".2f"),
                alt.Tooltip("avg_sell_price:Q", title="Avg Sell", format=".2f"),
                alt.Tooltip("spread_abs:Q", title="Spread (abs)", format=".2f"),
                alt.Tooltip("spread_pct:Q", title="Spread (%)", format=".2f"),
                alt.Tooltip("currency:N", title="Currency"),
            ],
        )
        .properties(height=420, title=f"P2P Spread per Hour and day ({metric_title})")
    )

# ------------------------------------------------------------------------------
def price_volatility_chart(df: pd.DataFrame, window: int = 7) -> alt.Chart:
    df = df.copy()
    df = df.drop(columns=[c for c in ["Unnamed: 0"] if c in df.columns])

    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df = df.sort_values(["currency", "date"])

    # If volatility is missing / mostly NaN, compute rolling vol from log_return
    if "volatility" not in df.columns or df["volatility"].isna().all():
        df["log_return"] = pd.to_numeric(df.get("log_return"), errors="coerce")
        df["volatility"] = (
            df.groupby("currency")["log_return"]
              .rolling(window=window, min_periods=window)
              .std()
              .reset_index(level=0, drop=True)
        )

    df["volatility"] = pd.to_numeric(df["volatility"], errors="coerce")

    return (
        alt.Chart(df.dropna(subset=["volatility"]))
        .mark_line()
        .encode(
            x=alt.X("yearmonthdate(date):T", title="Date", axis=alt.Axis(format="%b %d")),
            y=alt.Y("volatility:Q", title=f"Volatility (rolling {window}d)", scale=alt.Scale(zero=False)),
            color=alt.Color("currency:N", title="Currency"),
            tooltip=[
                alt.Tooltip("yearmonthdate(date):T", title="Date"),
                "currency:N",
                alt.Tooltip("volatility:Q", title="Volatility", format=".6f"),
                alt.Tooltip("mid_price:Q", title="Mid Price", format=".2f"),
                alt.Tooltip("log_return:Q", title="Log Return", format=".6f"),
            ],
        )
        .properties(height=400, title="Daily Price Volatility by Currency")
    )


# ------------------------------------------------------------------------------
def top_advertisers_volume_chart(df_top: pd.DataFrame, currency: str) -> alt.Chart:
    base = alt.Chart(df_top).encode(
        y=alt.Y("merchant_name:N", sort="-x", title="Advertiser")
    )
    return (
        base.mark_bar()
        .encode(
            x=alt.X("total_volume:Q", title="Total Volume"),
            tooltip=[
                alt.Tooltip("merchant_name:N", title="Advertiser"),
                alt.Tooltip("total_volume:Q", title="Total Volume", format=".2f"),
                alt.Tooltip("total_ads:Q", title="Number of Ads"),
                alt.Tooltip("avg_finish_rate:Q", title="Avg. Finish Rate", format=".2%"),
                alt.Tooltip("avg_positive_rate:Q", title="Avg. Positive Rate", format=".2%"),
            ],
        )
        .properties(title=f"Top Advertisers by Total Volume – {currency}", height=300)
    )

# ------------------------------------------------------------------------------
def top_advertisers_ads_chart(df_top: pd.DataFrame, currency: str) -> alt.Chart:
    base = alt.Chart(df_top).encode(
        y=alt.Y("merchant_name:N", sort="-x", title="Advertiser")
    )
    return (
        base.mark_bar()
        .encode(
            x=alt.X("total_ads:Q", title="Number of Ads"),
            tooltip=[
                alt.Tooltip("merchant_name:N", title="Advertiser"),
                alt.Tooltip("total_ads:Q", title="Number of ads"),
                alt.Tooltip("total_volume:Q", title="Total volume", format=".2f"),
                alt.Tooltip("avg_finish_rate:Q", title="Avg. finish rate", format=".2%"),
                alt.Tooltip("avg_positive_rate:Q", title="Avg. positive rate", format=".2%"),
            ],
        )
        .properties(title=f"Top Advertisers by Number of Ads – {currency}", height=300)
    )