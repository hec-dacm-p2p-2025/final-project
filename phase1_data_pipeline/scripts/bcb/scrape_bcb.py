import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

import requests
import pandas as pd
from io import StringIO
import re


def get_bcb_date():
    """
    Extracts the official date displayed by the BCB before scraping tables.
    Returns formatted date: 'YYYY-MM-DD'.
    """

    url = "https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
    html = requests.get(url).text

    match = re.search(r"(\d{1,2}) de ([A-Za-zÁÉÍÓÚáéíóú]+) (\d{4})", html)
    if not match:
        return None

    day, month_text, year = match.groups()

    months = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "setiembre": "09", "octubre": "10",
        "noviembre": "11", "diciembre": "12"
    }

    month_num = months[month_text.lower()]
    day = day.zfill(2)

    return f"{year}-{month_num}-{day}"


def scrape_bcb_official_rates():
    """
    Scrapes the official exchange rate table from the BCB website.
    Returns the raw DataFrame with columns:
    pais, unidad_monetaria, currency, tipo_cambio_bs, tipo_cambio_me
    """

    url = "https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.bcb.gob.bo/",
    }

    html = requests.get(url, headers=headers).text

    # Use StringIO to avoid the pandas deprecation warning
    tables = pd.read_html(StringIO(html), flavor="lxml")

    df = tables[1].copy()
    df.columns = [
        "pais", "unidad_monetaria", "currency",
        "tipo_cambio_bs", "tipo_cambio_me"
    ]

    return df