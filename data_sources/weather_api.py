# ==========================================
# PATH: data_sources/weather_api.py
# DESCRIPTION: Enterprise-Safe Real Weather Data Connector
# SOURCE: Open-Meteo (Primary) + Deterministic Fallback
# VERSION: v2.0.0-SUPREME
# ==========================================

from typing import Dict
import requests
import os

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
WEATHER_PROVIDER = "OPEN_METEO"
DEFAULT_TIMEOUT_SECONDS = 4

# City → Coordinates Registry (Extensible)
CITY_COORDS = {
    "Cairo": (30.0444, 31.2357),
    "Austin-TX": (30.2672, -97.7431),
    "Dubai": (25.2048, 55.2708),
    "TestCity": (30.0, 30.0)  # CI-safe virtual city
}

# Deterministic fallback (CI + offline safe)
DEFAULT_WEATHER_RESPONSE = {
    "weather_state": "Stable",
    "weather_factor": 0.3,
    "provider": "FALLBACK"
}


# --------------------------------------------------
# PUBLIC CONTRACT
# --------------------------------------------------
def get_live_weather(city_name: str) -> Dict[str, float]:
    """
    Enterprise-grade real weather fetcher.

    Guarantees:
    - Never raises exceptions
    - Always returns valid structure
    - Uses real data when available
    - CI-safe deterministic fallback

    Returns:
    {
        weather_state: str,
        weather_factor: float (0.0 → 1.0),
        provider: str
    }
    """

    # -------------------------------
    # City Validation
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
        # Hard CI-safe fallback (no logging, no crash)
        return _fallback_weather("NETWORK_FAILURE")


# --------------------------------------------------
# WEATHER CODE NORMALIZATION
# --------------------------------------------------
def _map_weather_code(weather_code: int) -> Dict[str, float]:
    """
    Maps Open-Meteo weather codes to FBC risk factors.
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
        "provider": WEATHER_PROVIDER
    }


def _fallback_weather(reason: str) -> Dict[str, float]:
    fallback = DEFAULT_WEATHER_RESPONSE.copy()
    fallback["fallback_reason"] = reason
    return fallback


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
