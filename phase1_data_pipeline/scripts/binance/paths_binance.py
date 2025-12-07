import os

# Absolute paths
BINANCE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(BINANCE_DIR)
PHASE1_DIR = os.path.dirname(SCRIPTS_DIR)

DATA_DIR = os.path.join(PHASE1_DIR, "data")

# Raw and processed folders specific to Binance
DATA_RAW_BINANCE = os.path.join(DATA_DIR, "raw", "binance")
DATA_PROCESSED_BINANCE = os.path.join(DATA_DIR, "processed", "binance")

# Processed subfolders
HISTORICAL_FIAT_DIR = os.path.join(DATA_PROCESSED_BINANCE, "historical_fiat")
DAILY_SNAP_DIR = os.path.join(DATA_PROCESSED_BINANCE, "daily_snapshots")

# Master file location
MASTER_PATH = os.path.join(DATA_PROCESSED_BINANCE, "p2p_master.parquet")