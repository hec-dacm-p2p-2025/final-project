import os
import time
from datetime import datetime, UTC
import socket

from binance.update_binance import update_binance
from bcb.update_bcb import update_bcb

base_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(base_dir, "..", "logs")

binance_log_dir = os.path.join(logs_dir, "binance")
bcb_log_dir = os.path.join(logs_dir, "bcb")

for d in [logs_dir, binance_log_dir, bcb_log_dir]:
    os.makedirs(d, exist_ok=True)

today = datetime.now(UTC).strftime("%Y-%m-%d")

binance_log_file = os.path.join(binance_log_dir, f"binance_{today}.log")
bcb_log_file = os.path.join(bcb_log_dir, f"bcb_{today}.log")


def write_log(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def has_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False


if __name__ == "__main__":

    if not has_internet():
        print("No internet connection — skipping pipeline.")
        write_log(binance_log_file, "Skip due to no internet connection.")
        write_log(bcb_log_file, "Skip due to no internet connection.")
        exit(0)

    pipeline_start = time.time()

    print("=== Running Binance Pipeline ===")
    start = time.time()
    write_log(binance_log_file, "\nRunning Binance Pipeline")
    write_log(binance_log_file, f"Start (UTC): {datetime.now(UTC)}")

    try:
        update_binance()
        end = time.time()
        duration = round(end - start, 2)

        write_log(binance_log_file, f"End (UTC): {datetime.now(UTC)}")
        write_log(binance_log_file, f"Duration: {duration} seconds")
        write_log(binance_log_file, "Status: success")

    except Exception as e:
        write_log(binance_log_file, f"Error: {str(e)}")

    print("=== Running BCB Pipeline ===")
    start = time.time()
    write_log(bcb_log_file, "\nRunning BCB Pipeline")
    write_log(bcb_log_file, f"Start (UTC): {datetime.now(UTC)}")

    try:
        df_fx = update_bcb()

        end = time.time()
        duration = round(end - start, 2)

        write_log(bcb_log_file, f"End (UTC): {datetime.now(UTC)}")
        write_log(bcb_log_file, f"Duration: {duration} seconds")

        from bcb.scrape_bcb import get_bcb_date
        extracted_date = get_bcb_date()
        write_log(bcb_log_file, f"Extracted date: {extracted_date}")

        if df_fx is None:
            write_log(bcb_log_file, "Skip: true")
        else:
            write_log(bcb_log_file, "Skip: false")

        write_log(bcb_log_file, "Status: success")

    except Exception as e:
        write_log(bcb_log_file, f"Error: {str(e)}")

    total_time = round(time.time() - pipeline_start, 2)
    print(f"Total pipeline runtime: {total_time} seconds")