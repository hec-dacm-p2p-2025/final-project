# Phase 3 — Streamlit P2P Binance Dashboard (Reproducible Local Setup)

This README explains how to reproduce the **Phase 3 Streamlit app locally**, starting from a clean machine:
- install dependencies in an isolated environment
- ensure **Phase 1 processed data** is available
- generate **Phase 3 exports** (CSV files) using the **Phase 2 `p2p_analytics` package**
- run the Streamlit app

---

## Repository layout (key parts)

From the repository root:

```
final-project/
  phase1_data_pipeline/
    data/processed/binance/p2p_master.parquet   # Phase 1 output (required by Phase 2)
  phase3_dashboard/
    exports/                                   # generated CSVs read by Streamlit
    streamlit_app/
      P2P_Binance.py                           # Streamlit entrypoint
      pages/                                   # multipage app
      app/                                     # helpers (data loading, viz, layout)
    requirements.txt                           # Phase 3 dependencies
```

Streamlit entrypoint:
- `phase3_dashboard/streamlit_app/P2P_Binance.py`

---

## 1) Prerequisites

- **Python 3.11+** (3.12 recommended)
- Git
- macOS/Linux commands below (Windows works too, but activation commands differ)


---

## 2) Clone the required repositories

### A) Clone `final-project`
```bash
git clone https://github.com/hec-dacm-p2p-2025/final-project.git
cd final-project
```

### B) Install the Phase 2 package (`p2p_analytics`)

Follow those instuctions: https://hec-dacm-p2p-2025.github.io/p2p-analytics/

From the instuctions:
- you have set a virtual environment.
- p2p analytics has been installed.

---

## 3) Install Phase 3 dependencies

```bash
python -m pip install -r phase3_dashboard/requirements.txt
```
---

## 4) Update the Phase 3 exports with new data (CSV files)

The Streamlit app reads CSVs from:

```
phase3_dashboard/exports/
```

Create export folders (if not already existing):

```bash
mkdir -p phase3_dashboard/exports/{daily_fiat_comparison,intraday_profile_by_currency,official_premium_by_currency,order_imbalance_by_currency,p2p_spread_by_currency,p2p_summary_by_currency,price_volatility_by_currency,top_advertisers_by_currency}
```

Run the notebook to generate the CSVs:

```bash
jupyter notebook phase3_dashboard/exports/generate_phase3_exports.ipynb
```
---

## 5) Run the Streamlit app locally

From `final-project/`:

```bash
streamlit run phase3_dashboard/streamlit_app/P2P_Binance.py
```
---

## Notes on reproducibility

- The Streamlit app is reproducible as long as:
  1) Phase 1 parquet exists, and  
  2) exports CSVs are generated into `phase3_dashboard/exports/`.
