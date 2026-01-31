# ==========================================
# PATH: data_sources/energy_price_data.py
# DESCRIPTION: Enterprise-Grade Energy Price Data Connector
# SOURCE: Global Electricity Prices (Public Dataset)
# VERSION: v3.0.0-SUPREME
# ==========================================

from typing import Dict
import requests

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
DATASET_URL = (
    "https://raw.githubusercontent.com/datasets/electricity-prices/master/data/electricity-prices.json"
)

DEFAULT_TIMEOUT_SECONDS = 6

DEFAULT_ENERGY_PRICE_RESPONSE = {
    "country": "UNKNOWN",
    "price_per_kwh": 0.0,
    "provider": "FALLBACK",
    "confidence": "LOW"
}


# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def get_country_energy_price(country_code: str) -> Dict[str, float]:
    """
    Fetches average electricity price (USD per kWh) for a country.

    Guarantees:
    - Never raises exceptions
    - Always returns deterministic structure
    - Uses real public dataset when available
    - CI-safe fallback on failure

    Returns:
    {
        country: str,
        price_per_kwh: float,
        provider: str,
        confidence: str
    }
    """

    if not country_code or not isinstance(country_code, str):
        return _fallback_energy_price("INVALID_COUNTRY_CODE")

    try:
        response = requests.get(DATASET_URL, timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()

        dataset = response.json()

        for record in dataset:
            if record.get("country_code", "").upper() == country_code.upper():
                price = record.get("price_usd_kwh")

                if price is None:
                    return _fallback_energy_price("MISSING_PRICE")

                return {
                    "country": country_code.upper(),
                    "price_per_kwh": float(price),
                    "provider": "GLOBAL_ELECTRICITY_DATASET",
                    "confidence": "MEDIUM"
                }

        return _fallback_energy_price("COUNTRY_NOT_FOUND")

    except Exception:
        return _fallback_energy_price("NETWORK_OR_DATASET_FAILURE")


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------
def _fallback_energy_price(reason: str) -> Dict[str, float]:
    fallback = DEFAULT_ENERGY_PRICE_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback
