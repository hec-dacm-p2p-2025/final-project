# multi_fetch.py

import time
import pandas as pd
from base_scraper import p2p_query, p2p_to_df


def p2p_fetch(asset, fiat, run_index, pages=2, delay=0.5):
    """
    Fetches BUY and SELL data for a given asset and fiat currency.
    Iterates through multiple pages, applies rate-limit delays,
    and combines all results into a single DataFrame.
    """

    sides = ["BUY", "SELL"]
    all_rows = []

    for side in sides:
        for page in range(1, pages + 1):

            # Query API for given side and page
            json_response = p2p_query(asset, fiat, side, page=page)

            # Convert JSON into DataFrame; empty if no valid data
            df = p2p_to_df(json_response, side)

            # Respect Binance rate limits
            time.sleep(delay)

            # Skip empty results
            if df.empty:
                continue

            # Attach run_index (final name used across the pipeline)
            df["run_index"] = run_index

            # Add partial result to list
            all_rows.append(df)

    # If no data collected, return empty DataFrame
    if len(all_rows) == 0:
        return pd.DataFrame()

    # Combine all DataFrames into one
    final_df = pd.concat(all_rows, ignore_index=True).drop_duplicates()

    return final_df