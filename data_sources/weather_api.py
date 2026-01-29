# ==========================================
# PATH: /data_sources/weather_api.py
# DESCRIPTION: Real Weather Data Connector
# SOURCE: Open-Meteo Free API (No Key Required)
# VERSION: v1.0.0
# ==========================================

import requests

# Simple city → coordinates mapping
CITY_COORDS = {
    "Cairo": (30.0444, 31.2357),
    "Austin-TX": (30.2672, -97.7431),
    "Dubai": (25.2048, 55.2708)
}

def get_live_weather(city_name: str):
    """
    Fetches real-time weather condition for a city.
    Returns weather_state and numeric weather_factor.
    """

    if city_name not in CITY_COORDS:
        return {"weather_state": "Unknown", "weather_factor": 0.3}

    lat, lon = CITY_COORDS[city_name]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        current = data["current_weather"]

        # Weather code mapping
        weather_code = current["weathercode"]

        # Basic mapping to factor
        if weather_code in [0]:  # Clear
            return {"weather_state": "Clear", "weather_factor": 0.1}
        elif weather_code in [1,2,3]:  # Cloudy
            return {"weather_state": "Cloudy", "weather_factor": 0.3}
        elif weather_code in [45,48,51,53,55,61,63,65]:  # Rain/Fog
            return {"weather_state": "Rain", "weather_factor": 0.6}
        else:  # Storm / Snow etc
            return {"weather_state": "Storm", "weather_factor": 0.9}

    except:
        return {"weather_state": "Unavailable", "weather_factor": 0.3}
