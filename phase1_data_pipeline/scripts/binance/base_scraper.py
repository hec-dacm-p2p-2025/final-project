# base_scraper.py

import requests
import pandas as pd
from datetime import datetime
import time


def safe_request(url, payload, max_retries=3, delay=2):
    """
    Sends a POST request with retry attempts.
    Returns the JSON response or None if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                return None


def extract_amount(value):
    """
    Normalizes Binance amount fields into a clean string or None.
    Handles cases where value may be:
    - a string ("1000", "1,200.00")
    - a number (100 or 100.0)
    - a dict {"amount": "100"}
    - a list ["100"]
    - None or empty
    Always returns something that can be safely converted to float later.
    """

    if value is None:
        return None

    # Case: {"amount": "..."}
    if isinstance(value, dict):
        value = value.get("amount")

    # Case: ["100"]
    if isinstance(value, list) and len(value) > 0:
        value = value[0]

    # Convert everything to string
    value = str(value)

    # Remove commas and spaces
    value = value.replace(",", "").strip()

    # Remove invalid representations
    if value in ["", "None", "nan", "{}", "[]"]:
        return None

    return value


def p2p_query(asset="USDT", fiat="USD", side="BUY", page=1, rows=20):
    """
    Prepares the Binance P2P API request and calls safe_request().
    Returns JSON or None.
    """

    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    payload = {
        "page": page,
        "rows": rows,
        "asset": asset,
        "tradeType": side.upper(),
        "fiat": fiat.upper()
    }

    return safe_request(url, payload)


def p2p_to_df(json_data, side):
    """
    Converts Binance P2P JSON data into a pandas DataFrame.
    Ensures mandatory fields exist and extracts values safely.
    """

    if json_data is None:
        return pd.DataFrame()

    entries = json_data.get("data", [])
    if not isinstance(entries, list) or len(entries) == 0:
        return pd.DataFrame()

    timestamp_value = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    rows = []

    for item in entries:

        adv = item.get("adv")
        advertiser = item.get("advertiser")

        if adv is None or advertiser is None:
            continue

        # Validate and convert price
        try:
            price_value = float(adv.get("price"))
        except Exception:
            continue

        # Payment methods
        trade_methods = adv.get("tradeMethods", [])
        if isinstance(trade_methods, list):
            payment_list = [m.get("identifier", "") for m in trade_methods]
        else:
            payment_list = []

        # Extract normalized min and max amounts
        min_amt = extract_amount(adv.get("minSingleTransAmount"))
        max_amt = extract_amount(adv.get("maxSingleTransAmount"))

        rows.append({
            "timestamp_scraped": timestamp_value,
            "side": side,
            "price": price_value,
            "asset": adv.get("asset"),
            "fiat": adv.get("fiatUnit"),
            "min_amount": min_amt,
            "max_amount": max_amt,
            "merchant_id": advertiser.get("userNo"),
            "merchant_name": advertiser.get("nickName"),
            "finish_rate": advertiser.get("monthFinishRate"),
            "positive_rate": advertiser.get("positiveRate"),
            "payment_methods": ",".join(payment_list)
        })

    return pd.DataFrame(rows)