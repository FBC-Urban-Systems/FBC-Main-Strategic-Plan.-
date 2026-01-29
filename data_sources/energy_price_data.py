# ==========================================
# PATH: /data_sources/energy_price_data.py
# DESCRIPTION: Real Electricity Price Loader
# SOURCE: Global Energy Price Dataset (Free Public Source)
# VERSION: v1.0.0
# ==========================================

import requests

# Free dataset from global energy price API proxy
BASE_URL = "https://raw.githubusercontent.com/datasets/electricity-prices/master/data/electricity-prices.json"

def get_country_energy_price(country_code: str):
    """
    Returns average electricity price (USD per kWh) for a country.
    """

    try:
        response = requests.get(BASE_URL, timeout=10)
        data = response.json()

        for record in data:
            if record["country_code"].upper() == country_code.upper():
                return {
                    "country": country_code.upper(),
                    "price_per_kwh": float(record["price_usd_kwh"])
                }

        return None

    except:
        return None
