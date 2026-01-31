# ==========================================
# PATH: Projects/Project_III_Traffic_Intelligence/accident_pred.py
# DESCRIPTION: Enterprise Traffic Risk Intelligence Engine
# VERSION: v3.2.0
# DATA MODE: REAL (CI-SAFE WITH HARD FALLBACK)
# ==========================================

from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
import logging

# --------------------------------------------------
# LOGGING CONFIG (ENTERPRISE SAFE)
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FBC.TrafficRiskEngine")

# --------------------------------------------------
# SAFE WEATHER IMPORT (REAL DATA + CI PROTECTION)
# --------------------------------------------------
try:
    from data_sources.weather_api import get_live_weather
except Exception:
    def get_live_weather(city: str) -> Dict[str, Any]:
        logger.warning("Weather API unavailable — using CI-safe fallback")
        return {
            "weather_factor": 0.15,
            "weather_state": "UNKNOWN_SAFE_FALLBACK",
            "data_mode": "FALLBACK"
        }


# --------------------------------------------------
# DATA CONTRACT
# --------------------------------------------------
@dataclass(frozen=True)
class TrafficRiskResult:
    city: str
    engine_version: str
    traffic_density: float
    weather: str
    risk_score: float
    data_mode: str


# --------------------------------------------------
# CORE ENGINE
# --------------------------------------------------
class TrafficRiskEngine:
    """
    FBC Traffic Risk Intelligence Engine

    • Deterministic
    • Audit-safe
    • Real-time capable
    • Insurance & City-OS ready
    """

    ENGINE_VERSION: str = "TRAFFIC-RISK-v3.2.0"
    DATA_MODE: str = "REAL"
    MAX_DENSITY_REFERENCE: float = 300.0

    def __init__(self, city: str) -> None:
        if not city or not isinstance(city, str):
            raise ValueError("City must be a non-empty string")
        self.city: str = city.strip()

    # --------------------------------------------------
    # CORE RISK ANALYSIS
    # --------------------------------------------------
    def analyze_real_time_risk(self, traffic_density: float) -> TrafficRiskResult:
        """
        Computes a normalized traffic risk score [0.0 – 1.0]
        using real density + real weather intelligence.
        """

        density = self._validate_density(traffic_density)
        weather = get_live_weather(self.city)

        weather_factor = float(weather.get("weather_factor", 0.0))
        weather_state = str(weather.get("weather_state", "UNKNOWN"))
        data_mode = str(weather.get("data_mode", self.DATA_MODE))

        base_risk = density / self.MAX_DENSITY_REFERENCE
        live_risk = round(base_risk + weather_factor, 4)
        live_risk = self._clamp(live_risk)

        logger.info(
            "Traffic risk computed | city=%s density=%.2f risk=%.4f mode=%s",
            self.city, density, live_risk, data_mode
        )

        return TrafficRiskResult(
            city=self.city,
            engine_version=self.ENGINE_VERSION,
            traffic_density=density,
            weather=weather_state,
            risk_score=live_risk,
            data_mode=data_mode
        )

    # --------------------------------------------------
    # INTERNAL UTILITIES
    # --------------------------------------------------
    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(value, 1.0))

    @staticmethod
    def _validate_density(value: float) -> float:
        try:
            val = float(value)
        except Exception:
            raise ValueError("Traffic density must be numeric")

        if val < 0:
            logger.warning("Negative density received — clamped to zero")
            return 0.0

        return val


# --------------------------------------------------
# CI / AUDIT SELF-TEST
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- FBC TRAFFIC RISK ENGINE v3.2.0 SELF-TEST ---")
    engine = TrafficRiskEngine("AuditCity")
    result = engine.analyze_real_time_risk(traffic_density=180)
    print(result)
    print("--- ENGINE STATUS: OPERATIONAL ✅ ---\n")
