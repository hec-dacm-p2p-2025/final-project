import os

# Absolute paths
BCB_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(BCB_DIR)
PHASE1_DIR = os.path.dirname(SCRIPTS_DIR)

DATA_DIR = os.path.join(PHASE1_DIR, "data")

# Raw and processed folders for BCB
DATA_RAW_BCB = os.path.join(DATA_DIR, "raw", "bcb")
DATA_PROCESSED_BCB = os.path.join(DATA_DIR, "processed", "bcb")

# Metadata folder inside processed/bcb
DATA_PROCESSED_BCB_METADATA = os.path.join(DATA_PROCESSED_BCB, "metadata")

# Metadata file path
METADATA_BCB = os.path.join(DATA_PROCESSED_BCB_METADATA, "bcb_metadata.json")
