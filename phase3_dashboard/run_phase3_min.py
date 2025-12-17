import subprocess
import sys

# 1) Notebook
subprocess.run(
    [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute",
        "--output", "phase3_dashboard/exports/data_extraction_executed.ipynb",
        "phase3_dashboard/data_extraction.ipynb",
    ],
    check=True,
)

# 2) Script
subprocess.run([sys.executable, "phase3_dashboard/P2P_Binance.py"], check=True)
