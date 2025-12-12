from pathlib import Path

# .../phase3_dashboard/streamlit_app/app/__init__.py
APP_DIR = Path(__file__).resolve().parent              # streamlit_app/app
STREAMLIT_APP_DIR = APP_DIR.parent                     # streamlit_app
PROJECT_ROOT = STREAMLIT_APP_DIR.parent                # phase3_dashboard
EXPORTS_DIR = PROJECT_ROOT / "exports"

# Default currency list (fallback)
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "MXN", "ARS", "BOB"]
