# ==========================================
# PATH: /data_sources/population_data.py
# DESCRIPTION: Real Population Data Connector
# VERSION: v2.1.0-SUPREME-FINAL
# ==========================================

import requests

BASE_URL = "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json"

def fetch_population(country_code: str) -> int:
    """
    Fetch latest population value from World Bank API
    with production-grade safe request handling.
    """

    url = BASE_URL.format(country_code.upper())

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2 or not data[1]:
            raise ValueError("No population data returned")

        latest_entry = data[1][0]
        pop_value = latest_entry.get("value")

        if pop_value is None:
            raise ValueError("Population value missing")

        return int(pop_value)

    except requests.exceptions.RequestException as e:
        print(f"[POPULATION CONNECTOR ERROR] {e}")
        return 0
    except Exception as e:
        print(f"[POPULATION DATA ERROR] {e}")
        return 0
