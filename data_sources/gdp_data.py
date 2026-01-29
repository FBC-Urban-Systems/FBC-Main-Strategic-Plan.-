# ==========================================
# PATH: /data_sources/gdp_data.py
# DESCRIPTION: Real GDP Data Loader
# SOURCE: World Bank Open Data
# VERSION: v1.0.0
# ==========================================

import requests

# World Bank API for GDP (Current US$)
BASE_URL = "https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json"

def get_country_gdp(country_code: str):
    """
    Fetches latest GDP data for a given country code.
    Example: EG, US, AE
    """

    url = BASE_URL.format(country_code=country_code.upper())
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if len(data) < 2 or not data[1]:
        return None

    latest_record = data[1][0]
    gdp = latest_record["value"]
    year = latest_record["date"]

    return {
        "country": country_code.upper(),
        "gdp_usd": gdp,
        "year": year
    }
