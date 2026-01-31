# ==========================================
# PATH: data_sources/energy_price_data.py
# DESCRIPTION: Enterprise-Grade Energy Price Intelligence Connector
# PRIMARY SOURCE: Global Electricity Prices (Public Dataset)
# FALLBACK MODE: Deterministic / CI-Safe
#
# VERSION: v4.0.0-LTS
# CLASSIFICATION: ENTERPRISE_CRITICAL
# CONTRACT: ENERGY_PRICE_DATA_PROVIDER_CORE
# ==========================================

from __future__ import annotations

from typing import Dict
import requests

# --------------------------------------------------
# MODULE METADATA
# --------------------------------------------------
__version__ = "4.0.0-LTS"
__classification__ = "ENTERPRISE_CRITICAL"
__contract_role__ = "ENERGY_PRICE_DATA_PROVIDER_CORE"

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
DATASET_URL = (
    "https://raw.githubusercontent.com/datasets/electricity-prices/master/data/electricity-prices.json"
)

DEFAULT_TIMEOUT_SECONDS = 6

REALTIME_MODE = "REAL"
FALLBACK_MODE = "DETERMINISTIC_FALLBACK"

# --------------------------------------------------
# DETERMINISTIC FALLBACK RESPONSE
# --------------------------------------------------
DEFAULT_ENERGY_PRICE_RESPONSE = {
    "country": "UNKNOWN",
    "price_per_kwh": 0.0,
    "provider": "FALLBACK",
    "confidence": "LOW",
    "data_mode": FALLBACK_MODE
}

# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def get_country_energy_price(country_code: str) -> Dict[str, float]:
    """
    Enterprise-grade energy price intelligence provider.

    Contract Guarantees:
    - Never raises exceptions
    - Always returns validated structure
    - Uses real public data when available
    - Deterministic CI-safe fallback
    - Audit-ready output

    Returns:
    {
        country: str,
        price_per_kwh: float,
        provider: str,
        confidence: str,
        data_mode: str
    }
    """

    # -------------------------------
    # INPUT VALIDATION
    # -------------------------------
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
                    "confidence": "MEDIUM",
                    "data_mode": REALTIME_MODE
                }

        return _fallback_energy_price("COUNTRY_NOT_FOUND")

    except Exception:
        # Hard deterministic fallback
        return _fallback_energy_price("NETWORK_OR_DATASET_FAILURE")

# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------
def _fallback_energy_price(reason: str) -> Dict[str, float]:
    fallback = DEFAULT_ENERGY_PRICE_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback
