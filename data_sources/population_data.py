# ==========================================
# PATH: data_sources/population_data.py
# DESCRIPTION: Enterprise-Grade Population Data Connector
# SOURCE: World Bank Open API
# VERSION: v3.0.0-SUPREME
# ==========================================

from typing import Dict
import requests

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WORLD_BANK_BASE_URL = (
    "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json"
)
DEFAULT_TIMEOUT_SECONDS = 6

# Deterministic fallback (CI-safe)
DEFAULT_POPULATION_RESPONSE = {
    "population": 0,
    "provider": "FALLBACK",
    "confidence": "LOW"
}


# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def fetch_population(country_code: str) -> Dict[str, int]:
    """
    Fetches latest population value using World Bank API.

    Guarantees:
    - Never raises exceptions
    - Always returns deterministic structure
    - Uses real data when available
    - CI-safe fallback otherwise

    Returns:
    {
        population: int,
        provider: str,
        confidence: str
    }
    """

    if not country_code or not isinstance(country_code, str):
        return _fallback_population("INVALID_COUNTRY_CODE")

    url = WORLD_BANK_BASE_URL.format(country_code.upper())

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()

        payload = response.json()

        if not payload or len(payload) < 2 or not payload[1]:
            return _fallback_population("EMPTY_PAYLOAD")

        latest_entry = payload[1][0]
        value = latest_entry.get("value")

        if value is None:
            return _fallback_population("MISSING_VALUE")

        return {
            "population": int(value),
            "provider": "WORLD_BANK",
            "confidence": "HIGH"
        }

    except Exception:
        return _fallback_population("NETWORK_OR_API_FAILURE")


# --------------------------------------------------
# BACKWARD-COMPATIBILITY LAYER
# --------------------------------------------------
def get_country_population(country_code: str) -> int:
    """
    Legacy alias (returns numeric population only).
    Guaranteed to never raise.
    """
    result = fetch_population(country_code)
    return int(result.get("population", 0))


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------
def _fallback_population(reason: str) -> Dict[str, int]:
    fallback = DEFAULT_POPULATION_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback
