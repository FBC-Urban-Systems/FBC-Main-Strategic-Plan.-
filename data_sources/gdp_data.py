# ==========================================
# PATH: data_sources/gdp_data.py
# DESCRIPTION: Enterprise-Grade GDP Intelligence Connector
# PRIMARY SOURCE: World Bank Open Data API
# FALLBACK MODE: Deterministic / CI-Safe
#
# VERSION: v4.0.0-LTS
# CLASSIFICATION: ENTERPRISE_CRITICAL
# CONTRACT: GDP_DATA_PROVIDER_CORE
# ==========================================

from __future__ import annotations

from typing import Dict
import requests

# --------------------------------------------------
# MODULE METADATA
# --------------------------------------------------
__version__ = "4.0.0-LTS"
__classification__ = "ENTERPRISE_CRITICAL"
__contract_role__ = "GDP_DATA_PROVIDER_CORE"

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WORLD_BANK_BASE_URL = (
    "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json"
)
DEFAULT_TIMEOUT_SECONDS = 6

REALTIME_MODE = "REAL"
FALLBACK_MODE = "DETERMINISTIC_FALLBACK"

# --------------------------------------------------
# DETERMINISTIC FALLBACK RESPONSE
# --------------------------------------------------
DEFAULT_GDP_RESPONSE = {
    "gdp": 0.0,
    "provider": "FALLBACK",
    "confidence": "LOW",
    "data_mode": FALLBACK_MODE
}

# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def fetch_gdp(country_code: str) -> Dict[str, float]:
    """
    Enterprise-grade GDP intelligence provider.

    Contract Guarantees:
    - Never raises exceptions
    - Always returns validated structure
    - Uses real data when available
    - Deterministic CI-safe fallback
    - Audit-ready output

    Returns:
    {
        gdp: float,
        provider: str,
        confidence: str,
        data_mode: str
    }
    """

    # -------------------------------
    # INPUT VALIDATION
    # -------------------------------
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
            "confidence": "HIGH",
            "data_mode": REALTIME_MODE
        }

    except Exception:
        # Hard deterministic fallback
        return _fallback_gdp("NETWORK_OR_API_FAILURE")

# --------------------------------------------------
# BACKWARD-COMPATIBILITY LAYER
# --------------------------------------------------
def get_country_gdp(country_code: str) -> float:
    """
    Legacy alias (numeric-only GDP).
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
