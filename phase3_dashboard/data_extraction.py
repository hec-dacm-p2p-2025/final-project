from p2p_analytics import fiat_comparison, intraday_profile, p2p_spread, official_premium, order_imbalance, p2p_summary, price_volatility, top_advertisers
import pandas as pd
from pathlib import Path

PATH = "exports"
PHASE1_ROOT = Path("../phase1_data_pipeline/data/processed").resolve()

# Daily Fiat Comparison
daily_fiat_comparison = fiat_comparison(currencies=['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'MXN', 'ARS', 'BOB'], root=PHASE1_ROOT)
daily_fiat_comparison.to_csv(f"{PATH}/daily_fiat_comparison/fiat_comparison.csv")

# Intraday Profile
USD_intraday_profile = intraday_profile(currency="USD", root=PHASE1_ROOT)
USD_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/USD_intraday_profile.csv")

EUR_intraday_profile = intraday_profile(currency="EUR", root=PHASE1_ROOT)
EUR_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/EUR_intraday_profile.csv")

GBP_intraday_profile = intraday_profile(currency="GBP", root=PHASE1_ROOT)
GBP_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/GBP_intraday_profile.csv")

JPY_intraday_profile = intraday_profile(currency="JPY", root=PHASE1_ROOT)
JPY_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/JPY_intraday_profile.csv")

CNY_intraday_profile = intraday_profile(currency="CNY", root=PHASE1_ROOT)
CNY_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/CNY_intraday_profile.csv")

MXN_intraday_profile = intraday_profile(currency="MXN", root=PHASE1_ROOT)
MXN_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/MXN_intraday_profile.csv")

ARS_intraday_profile = intraday_profile(currency="ARS", root=PHASE1_ROOT)
ARS_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/ARS_intraday_profile.csv")

BOB_intraday_profile = intraday_profile(currency="BOB", root=PHASE1_ROOT)
BOB_intraday_profile.to_csv(f"{PATH}/intraday_profile_by_currency/BOB_intraday_profile.csv")

# P2P Spread
USD_p2p_spread = p2p_spread(currency="USD", by='hour', root=PHASE1_ROOT)
USD_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/USD_p2p_spread.csv")

EUR_p2p_spread = p2p_spread(currency="EUR", by='hour', root=PHASE1_ROOT)
EUR_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/EUR_p2p_spread.csv")

GBP_p2p_spread = p2p_spread(currency="GBP", by='hour', root=PHASE1_ROOT)
GBP_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/GBP_p2p_spread.csv")

JPY_p2p_spread = p2p_spread(currency="JPY", by='hour', root=PHASE1_ROOT)
JPY_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/JPY_p2p_spread.csv")

CNY_p2p_spread = p2p_spread(currency="CNY", by='hour', root=PHASE1_ROOT)
CNY_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/CNY_p2p_spread.csv")

MXN_p2p_spread = p2p_spread(currency="MXN", by='hour', root=PHASE1_ROOT)
MXN_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/MXN_p2p_spread.csv")

ARS_p2p_spread = p2p_spread(currency="ARS", by='hour', root=PHASE1_ROOT)
ARS_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/ARS_p2p_spread.csv")

BOB_p2p_spread = p2p_spread(currency="BOB", by='hour', root=PHASE1_ROOT)
BOB_p2p_spread.to_csv(f"{PATH}/p2p_spread_by_currency/BOB_p2p_spread.csv")

# Premium vs. Official Exchange Rate
USD_official_premium = official_premium(currency="USD", by='day', root=PHASE1_ROOT)
USD_official_premium.to_csv(f"{PATH}/official_premium_by_currency/USD_official_premium.csv") #yet no data

EUR_official_premium = official_premium(currency="EUR", by='day', root=PHASE1_ROOT)
EUR_official_premium.to_csv(f"{PATH}/official_premium_by_currency/EUR_official_premium.csv")

GBP_official_premium = official_premium(currency="GBP", by='day', root=PHASE1_ROOT)
GBP_official_premium.to_csv(f"{PATH}/official_premium_by_currency/GBP_official_premium.csv")

JPY_official_premium = official_premium(currency="JPY", by='day', root=PHASE1_ROOT)
JPY_official_premium.to_csv(f"{PATH}/official_premium_by_currency/JPY_official_premium.csv")

CNY_official_premium = official_premium(currency="CNY", by='day', root=PHASE1_ROOT)
CNY_official_premium.to_csv(f"{PATH}/official_premium_by_currency/CNY_official_premium.csv")

MXN_official_premium = official_premium(currency="MXN", by='day', root=PHASE1_ROOT)
MXN_official_premium.to_csv(f"{PATH}/official_premium_by_currency/MXN_official_premium.csv")

ARS_official_premium = official_premium(currency="ARS", by='day', root=PHASE1_ROOT)
ARS_official_premium.to_csv(f"{PATH}/official_premium_by_currency/ARS_official_premium.csv")

BOB_official_premium = official_premium(currency="BOB", by='day', root=PHASE1_ROOT)
BOB_official_premium.to_csv(f"{PATH}/official_premium_by_currency/BOB_official_premium.csv")

# Microstructure Indicators
USD_order_imbalance = order_imbalance(currency="USD", by='hour', root=PHASE1_ROOT)
USD_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/USD_order_imbalance.csv")

EUR_order_imbalance = order_imbalance(currency="EUR", by='hour', root=PHASE1_ROOT)
EUR_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/EUR_order_imbalance.csv")

GBP_order_imbalance = order_imbalance(currency="GBP", by='hour', root=PHASE1_ROOT)
GBP_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/GBP_order_imbalance.csv")

JPY_order_imbalance = order_imbalance(currency="JPY", by='hour', root=PHASE1_ROOT)
JPY_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/JPY_order_imbalance.csv")

CNY_order_imbalance = order_imbalance(currency="CNY", by='hour', root=PHASE1_ROOT)
CNY_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/CNY_order_imbalance.csv")

MXN_order_imbalance = order_imbalance(currency="MXN", by='hour', root=PHASE1_ROOT)
MXN_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/MXN_order_imbalance.csv")

ARS_order_imbalance = order_imbalance(currency="ARS", by='hour', root=PHASE1_ROOT)
ARS_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/ARS_order_imbalance.csv")

BOB_order_imbalance = order_imbalance(currency="BOB", by='hour', root=PHASE1_ROOT)
BOB_order_imbalance.to_csv(f"{PATH}/order_imbalance_by_currency/BOB_order_imbalance.csv")

# Volatility
USD_price_volatility = price_volatility(currency='USD', by='day', window=7, root=PHASE1_ROOT)
USD_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/USD_price_volatility.csv")


EUR_price_volatility = price_volatility(currency='EUR', by='day', window=7, root=PHASE1_ROOT)
EUR_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/EUR_price_volatility.csv")

GBP_price_volatility = price_volatility(currency='GBP', by='day', window=7, root=PHASE1_ROOT)
GBP_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/GBP_price_volatility.csv")

JPY_price_volatility = price_volatility(currency='JPY', by='day', window=7, root=PHASE1_ROOT)
JPY_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/JPY_price_volatility.csv")

CNY_price_volatility = price_volatility(currency='CNY', by='day', window=7, root=PHASE1_ROOT)
CNY_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/CNY_price_volatility.csv")

MXN_price_volatility = price_volatility(currency='MXN', by='day', window=7, root=PHASE1_ROOT)
MXN_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/MXN_price_volatility.csv")

ARS_price_volatility = price_volatility(currency='ARS', by='day', window=7, root=PHASE1_ROOT)
ARS_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/ARS_price_volatility.csv")

BOB_price_volatility = price_volatility(currency='BOB', by='day', window=7, root=PHASE1_ROOT)
BOB_price_volatility.to_csv(f"{PATH}/price_volatility_by_currency/BOB_price_volatility.csv")

# Top Advertisers
USD_top_advertisers = top_advertisers(currency='USD', root=PHASE1_ROOT)
USD_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/USD_top_advertisers.csv")

EUR_top_advertisers = top_advertisers(currency='EUR', root=PHASE1_ROOT)
EUR_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/EUR_top_advertisers.csv")

GBP_top_advertisers = top_advertisers(currency='GBP', root=PHASE1_ROOT)
GBP_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/GBP_top_advertisers.csv")

JPY_top_advertisers = top_advertisers(currency='JPY', root=PHASE1_ROOT)
JPY_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/JPY_top_advertisers.csv")

CNY_top_advertisers = top_advertisers(currency='CNY', root=PHASE1_ROOT)
CNY_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/CNY_top_advertisers.csv")

MXN_top_advertisers = top_advertisers(currency='MXN', root=PHASE1_ROOT)
MXN_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/MXN_top_advertisers.csv")

ARS_top_advertisers = top_advertisers(currency='ARS', root=PHASE1_ROOT)
ARS_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/ARS_top_advertisers.csv")

BOB_top_advertisers = top_advertisers(currency='BOB', root=PHASE1_ROOT)
BOB_top_advertisers.to_csv(f"{PATH}/top_advertisers_by_currency/BOB_top_advertisers.csv")

# Summary Statistics
currencies_p2p_summary = p2p_summary(currencies=['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'MXN', 'ARS', 'BOB'], root=PHASE1_ROOT)
p2p_summary.to_csv(f"{PATH}/p2p_summary.csv")