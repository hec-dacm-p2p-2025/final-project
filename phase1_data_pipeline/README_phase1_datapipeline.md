# Phase 1 — Data Pipeline

Automated pipeline collecting P2P exchange rate data from Binance and official rates from the Central Bank of Bolivia (BCB).

## What It Does

- *Binance P2P*: Scrapes BUY/SELL advertisements for 8 currencies every 15 minutes
- *BCB*: Scrapes official exchange rates daily

## How It Runs
```text
CRON-JOBS.ORG (every 15 min)
        ↓
GitHub Actions workflow
        ↓
run_pipeline.py
        ↓
    ┌───┴───┐
    ↓       ↓
Binance   BCB
    ↓       ↓
Parquet files (raw + processed)
```

## Output
```text
data/
├── raw/
│   ├── binance/
│   └── bcb/
└── processed/
    ├── binance/
    │   ├── p2p_master.parquet
    │   ├── daily_snapshots/
    │   └── historical_fiat/
    └── bcb/
        └── bcb_master.parquet
```

## Usage

Triggered automatically. To run manually:
bash
python phase1_data_pipeline/scripts/run_pipeline.py


## Documentation

Full details in the [Project Documentation](link-to-your-quarto-doc).
