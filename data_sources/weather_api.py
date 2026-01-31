# ==========================================
# PATH: data_sources/weather_api.py
# DESCRIPTION: Enterprise-Grade Weather Intelligence Connector
# PRIMARY SOURCE: Open-Meteo (Real-Time)
# FALLBACK MODE: Deterministic / CI-Safe
#
# VERSION: v3.0.0-LTS
# CLASSIFICATION: ENTERPRISE_CRITICAL
# CONTRACT: WEATHER_DATA_PROVIDER_CORE
# ==========================================

from __future__ import annotations

from typing import Dict
import requests

# --------------------------------------------------
# MODULE METADATA
# --------------------------------------------------
__version__ = "3.0.0-LTS"
__classification__ = "ENTERPRISE_CRITICAL"
__contract_role__ = "WEATHER_DATA_PROVIDER_CORE"

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WEATHER_PROVIDER = "OPEN_METEO"
DEFAULT_TIMEOUT_SECONDS = 4

# Explicit operating mode for audit & CI
REALTIME_MODE = "REAL"
FALLBACK_MODE = "DETERMINISTIC_FALLBACK"

# --------------------------------------------------
# CITY → COORDINATES REGISTRY
# --------------------------------------------------
CITY_COORDS = {
    "Cairo": (30.0444, 31.2357),
    "Austin-TX": (30.2672, -97.7431),
    "Dubai": (25.2048, 55.2708),
    "TestCity": (30.0, 30.0)  # CI-safe virtual city
}

# --------------------------------------------------
# DETERMINISTIC FALLBACK RESPONSE
# --------------------------------------------------
DEFAULT_WEATHER_RESPONSE = {
    "weather_state": "Stable",
    "weather_factor": 0.3,
    "provider": "FALLBACK",
    "data_mode": FALLBACK_MODE
}

# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def get_live_weather(city_name: str) -> Dict[str, float]:
    """
    Enterprise-grade weather intelligence provider.

    Contract Guarantees:
    - Never raises exceptions
    - Always returns validated structure
    - Uses real data when available
    - Deterministic CI-safe fallback
    - Audit-ready output

    Returns:
    {
        weather_state: str,
        weather_factor: float (0.0 → 1.0),
        provider: str,
        data_mode: str
    }
    """

    # -------------------------------
    # CITY VALIDATION
    # -------------------------------
    if city_name not in CITY_COORDS:
        return _fallback_weather("UNKNOWN_CITY")

    lat, lon = CITY_COORDS[city_name]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        response.raise_for_status()

        payload = response.json()
        current = payload.get("current_weather")

        if not current or "weathercode" not in current:
            return _fallback_weather("INVALID_PAYLOAD")

        return _map_weather_code(current["weathercode"])

    except Exception:
        # Hard deterministic fallback (audit + CI safe)
        return _fallback_weather("NETWORK_FAILURE")

# --------------------------------------------------
# WEATHER CODE NORMALIZATION
# --------------------------------------------------
def _map_weather_code(weather_code: int) -> Dict[str, float]:
    """
    Normalizes Open-Meteo weather codes
    into FBC risk-weighted factors.
    """

    if weather_code == 0:
        return _response("Clear", 0.1)

    if weather_code in {1, 2, 3}:
        return _response("Cloudy", 0.3)

    if weather_code in {45, 48, 51, 53, 55, 61, 63, 65}:
        return _response("Rain", 0.6)

    return _response("Severe", 0.9)

# --------------------------------------------------
# RESPONSE BUILDERS
# --------------------------------------------------
def _response(state: str, factor: float) -> Dict[str, float]:
    return {
        "weather_state": state,
        "weather_factor": _clamp(factor),
        "provider": WEATHER_PROVIDER,
        "data_mode": REALTIME_MODE
    }

def _fallback_weather(reason: str) -> Dict[str, float]:
    fallback = DEFAULT_WEATHER_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback

def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
