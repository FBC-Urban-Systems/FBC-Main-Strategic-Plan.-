# ==========================================
# PATH: data_sources/gdp_data.py
# DESCRIPTION: Enterprise-Grade GDP Data Connector
# SOURCE: World Bank Open API
# VERSION: v3.0.0-SUPREME
# ==========================================

from typing import Dict
import requests

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WORLD_BANK_BASE_URL = (
    "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json"
)
DEFAULT_TIMEOUT_SECONDS = 6

# Deterministic fallback (CI-safe)
DEFAULT_GDP_RESPONSE = {
    "gdp": 0.0,
    "provider": "FALLBACK",
    "confidence": "LOW"
}


# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def fetch_gdp(country_code: str) -> Dict[str, float]:
    """
    Fetches latest GDP value using World Bank API.

    Guarantees:
    - Never raises exceptions
    - Always returns deterministic structure
    - Uses real data when available
    - CI-safe fallback otherwise

    Returns:
    {
        gdp: float,
        provider: str,
        confidence: str
    }
    """

    if not country_code or not isinstance(country_code, str):
        return _fallback_gdp("INVALID_COUNTRY_CODE")

    url = WORLD_BANK_BASE_URL.format(country_code.upper())

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()

        payload = response.json()

        if not payload or len(payload) < 2 or not payload[1]:
            return _fallback_gdp("EMPTY_PAYLOAD")

        latest_entry = payload[1][0]
        value = latest_entry.get("value")

        if value is None:
            return _fallback_gdp("MISSING_VALUE")

        return {
            "gdp": float(value),
            "provider": "WORLD_BANK",
            "confidence": "HIGH"
        }

    except Exception:
        return _fallback_gdp("NETWORK_OR_API_FAILURE")


# --------------------------------------------------
# BACKWARD-COMPATIBILITY LAYER
# --------------------------------------------------
def get_country_gdp(country_code: str) -> float:
    """
    Legacy alias (returns numeric GDP only).
    Guaranteed to never raise.
    """
    result = fetch_gdp(country_code)
    return float(result.get("gdp", 0.0))


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------
def _fallback_gdp(reason: str) -> Dict[str, float]:
    fallback = DEFAULT_GDP_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback
