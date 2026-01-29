# ==========================================
# PATH: /data_sources/population_data.py
# DESCRIPTION: Real Population Data Loader
# SOURCE: World Bank Open Data
# VERSION: v1.0.0
# ==========================================

import requests

# World Bank API for population
BASE_URL = "https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json"

def get_country_population(country_code: str):
    """
    Fetches latest population data for a given country code.
    Example codes: EG = Egypt, US = United States, AE = UAE
    """

    url = BASE_URL.format(country_code=country_code.upper())
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    # Data format: [metadata, [records]]
    if len(data) < 2 or not data[1]:
        return None

    latest_record = data[1][0]
    population = latest_record["value"]
    year = latest_record["date"]

    return {
        "country": country_code.upper(),
        "population": population,
        "year": year
    }
