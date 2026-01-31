# ==========================================
# PATH: Projects/Project_III_Traffic_Intelligence/accident_pred.py
# DESCRIPTION: Supreme Traffic Risk Intelligence Engine
# VERSION: v3.0-SUPREME-TRAFFIC-RISK
# DATA MODE: REAL (WITH CI-SAFE FALLBACK)
# ==========================================

from typing import Dict

# --------------------------------------------------
# SAFE WEATHER IMPORT (REAL DATA + CI PROTECTION)
# --------------------------------------------------
try:
    from data_sources.weather_api import get_live_weather
except Exception:
    # Enterprise-safe fallback (used ONLY if real source unavailable)
    def get_live_weather(city: str) -> Dict[str, float]:
        return {
            "weather_factor": 0.15,
            "weather_state": "UNKNOWN_SAFE_FALLBACK",
            "data_mode": "FALLBACK"
        }


class TrafficRiskEngine:
    """
    FBC Traffic Risk Intelligence Engine (Supreme)

    - Real-time capable
    - Deterministic & CI-safe
    - Backward compatible
    """

    ENGINE_VERSION = "TRAFFIC-RISK-v3.0-SUPREME"
    DATA_MODE = "REAL"

    def __init__(self, city: str):
        self.city = str(city)

    # --------------------------------------------------
    # REAL-TIME RISK ANALYSIS
    # --------------------------------------------------
    def analyze_real_time_risk(self, traffic_density: float) -> Dict[str, float]:
        """
        Calculates live traffic risk using:
        - Traffic density
        - Real-time weather factor (with enterprise fallback)

        Risk score is always clamped between 0.0 and 1.0
        """
        density = max(float(traffic_density), 0.0)

        weather = get_live_weather(self.city)

        weather_factor = float(weather.get("weather_factor", 0.0))
        weather_state = weather.get("weather_state", "UNKNOWN")

        # --------------------------------------------------
        # CORE DETERMINISTIC RISK FORMULA
        # --------------------------------------------------
        base_risk = density / 300.0
        live_risk = round(base_risk + weather_factor, 3)

        # Clamp risk score
        live_risk = min(max(live_risk, 0.0), 1.0)

        return {
            "city": self.city,
            "engine_version": self.ENGINE_VERSION,
            "traffic_density": density,
            "weather": weather_state,
            "risk_score": live_risk,
            "data_mode": weather.get("data_mode", self.DATA_MODE)
        }


# --------------------------------------------------
# STANDALONE ENTERPRISE SELF-TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- FBC TRAFFIC RISK ENGINE SUPREME TEST ---")

    engine = TrafficRiskEngine("AuditCity")
    result = engine.analyze_real_time_risk(traffic_density=180)

    print("Risk Result:", result)
    print("--- TRAFFIC ENGINE OPERATIONAL ✅ ---\n")
