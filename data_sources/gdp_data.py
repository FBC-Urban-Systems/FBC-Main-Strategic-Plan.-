# ==========================================
# PATH: /data_sources/gdp_data.py
# DESCRIPTION: Real GDP Data Connector
# VERSION: v2.0.0-SUPREME-STABLE
# ==========================================

import requests

BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json"

def fetch_gdp(country_code: str) -> float:
    """
    Fetch latest GDP value for given country code from World Bank API.
    Supreme-grade safe network handling.
    """

    url = BASE_URL.format(country_code.upper())

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2 or not data[1]:
            raise ValueError("No GDP data returned")

        latest_entry = data[1][0]
        gdp_value = latest_entry.get("value")

        if gdp_value is None:
            raise ValueError("GDP value missing")

        return float(gdp_value)

    except requests.exceptions.RequestException as e:
        print(f"[GDP CONNECTOR ERROR] {e}")
        return 0.0
    except Exception as e:
        print(f"[GDP DATA ERROR] {e}")
        return 0.0
