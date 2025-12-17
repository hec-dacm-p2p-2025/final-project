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
  phase3_dashboard/
    exports/                                   # generated CSVs read by Streamlit
    streamlit_app/
      P2P_Binance.py                           # Streamlit entrypoint
      pages/                                   # multipage app
      app/                                     # helpers (data loading, viz, layout)
    requirements.txt                           # Phase 3 dependencies
```

---

## 1) Prerequisites

- **Python 3.11+** (3.12 recommended)
- Git
- macOS/windows


---

## 2) Clone the required repositories

### A) Clone `final-project`

For macOS/windows:
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

For macOS/windows:
```bash
python -m pip install -r phase3_dashboard/requirements.txt
```
---

## 4) Update the Phase 3 exports with new data (CSV files)

The Streamlit app reads CSVs from:

```
phase3_dashboard/exports/
```

Create export folders if they do not exist yet.


Run the pyhon file to update the CSVs:

For macOS/windows:
```bash
python phase3_dashboard/data_extraction.py
```
---

## 5) Run the Streamlit app locally

From `final-project/`:

For macOS/windows:
```bash
streamlit run phase3_dashboard/streamlit_app/P2P_Binance.py
```
---
