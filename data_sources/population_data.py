# ==========================================
# PATH: data_sources/population_data.py
# DESCRIPTION: Enterprise-Grade Population Intelligence Connector
# PRIMARY SOURCE: World Bank Open Data API
# FALLBACK MODE: Deterministic / CI-Safe
#
# VERSION: v4.0.0-LTS
# CLASSIFICATION: ENTERPRISE_CRITICAL
# CONTRACT: POPULATION_DATA_PROVIDER_CORE
# ==========================================

from __future__ import annotations

from typing import Dict
import requests

# --------------------------------------------------
# MODULE METADATA
# --------------------------------------------------
__version__ = "4.0.0-LTS"
__classification__ = "ENTERPRISE_CRITICAL"
__contract_role__ = "POPULATION_DATA_PROVIDER_CORE"

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WORLD_BANK_BASE_URL = (
    "https://api.worldbank.org/v2/country/{}/indicator/SP.POP.TOTL?format=json"
)
DEFAULT_TIMEOUT_SECONDS = 6

REALTIME_MODE = "REAL"
FALLBACK_MODE = "DETERMINISTIC_FALLBACK"

# --------------------------------------------------
# DETERMINISTIC FALLBACK RESPONSE
# --------------------------------------------------
DEFAULT_POPULATION_RESPONSE = {
    "population": 0,
    "provider": "FALLBACK",
    "confidence": "LOW",
    "data_mode": FALLBACK_MODE
}

# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def fetch_population(country_code: str) -> Dict[str, int]:
    """
    Enterprise-grade population intelligence provider.

    Contract Guarantees:
    - Never raises exceptions
    - Always returns validated structure
    - Uses real data when available
    - Deterministic CI-safe fallback
    - Audit-ready output

    Returns:
    {
        population: int,
        provider: str,
        confidence: str,
        data_mode: str
    }
    """

    # -------------------------------
    # INPUT VALIDATION
    # -------------------------------
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
            "confidence": "HIGH",
            "data_mode": REALTIME_MODE
        }

    except Exception:
        # Hard deterministic fallback
        return _fallback_population("NETWORK_OR_API_FAILURE")

# --------------------------------------------------
# BACKWARD-COMPATIBILITY LAYER
# --------------------------------------------------
def get_country_population(country_code: str) -> int:
    """
    Legacy alias (numeric-only population).
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
