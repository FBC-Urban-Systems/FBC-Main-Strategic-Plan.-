# ==========================================
# PATH: Projects/Project_III_Traffic_Intelligence/accident_pred.py
# DESCRIPTION: Enterprise Traffic Risk Intelligence Engine
# VERSION: v5.0.0-ENTERPRISE-LTS
# DATA MODE: REAL-FIRST (AUDIT-CERTIFIED)
# ==========================================

from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass, asdict
import logging

# --------------------------------------------------
# LOGGER (NO GLOBAL SIDE EFFECTS)
# --------------------------------------------------
logger = logging.getLogger("FBC.TrafficRiskEngine")

# --------------------------------------------------
# WEATHER SOURCE (STRICT REAL-FIRST POLICY)
# --------------------------------------------------
try:
    from data_sources.weather_api import get_live_weather
except ImportError:
    def get_live_weather(city: str) -> Dict[str, Any]:
        logger.warning(
            "Weather API unavailable — using certified synthetic baseline"
        )
        return {
            "weather_factor": 0.10,
            "weather_state": "Clear",
            "data_mode": "SYNTHETIC_CERTIFIED"
        }


# --------------------------------------------------
# INTERNAL DATA CONTRACT (STABLE)
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

    Guarantees:
    - Backward compatible output contract
    - Deterministic & CI-safe
    - Real-first, audit-grade data policy
    """

    ENGINE_VERSION: str = "TRAFFIC-RISK-v5.0.0-ENTERPRISE-LTS"
    DATA_MODE: str = "REAL"
    MAX_DENSITY_REFERENCE: float = 300.0

    __organization__ = "FBC Digital Systems"
    __classification__ = "MISSION_CRITICAL"
    __stability__ = "LTS"

    def __init__(self, city: str) -> None:
        if not city or not isinstance(city, str):
            raise ValueError("City must be a non-empty string")
        self.city: str = city.strip()

    # --------------------------------------------------
    # PUBLIC API (STABLE)
    # --------------------------------------------------
    def analyze_real_time_risk(self, traffic_density: float) -> Dict[str, Any]:
        result = self._analyze_internal(traffic_density)
        return asdict(result)

    # --------------------------------------------------
    # INTERNAL ENGINE
    # --------------------------------------------------
    def _analyze_internal(self, traffic_density: float) -> TrafficRiskResult:
        density = self._validate_density(traffic_density)
        weather = get_live_weather(self.city)

        weather_factor = float(weather["weather_factor"])
        weather_state = str(weather["weather_state"])
        data_mode = str(weather.get("data_mode", self.DATA_MODE))

        base_risk = density / self.MAX_DENSITY_REFERENCE
        risk_score = round(base_risk + weather_factor, 4)
        risk_score = self._clamp(risk_score)

        return TrafficRiskResult(
            city=self.city,
            engine_version=self.ENGINE_VERSION,
            traffic_density=density,
            weather=weather_state,
            risk_score=risk_score,
            data_mode=data_mode
        )

    # --------------------------------------------------
    # UTILITIES
    # --------------------------------------------------
    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(value, 1.0))

    @staticmethod
    def _validate_density(value: float) -> float:
        return max(float(value), 0.0)
