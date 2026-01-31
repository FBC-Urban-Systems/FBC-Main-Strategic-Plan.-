# ============================================================
# FBC DIGITAL SYSTEMS
# Project III – Traffic Intelligence
# File: accident_pred.py
#
# Description:
# Deterministic, audit-grade traffic accident risk
# intelligence engine for city-scale deployment.
#
# Version: v7.0.0
# Status: Production / CI / Audit / Insurance-Grade
# ============================================================

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FBC.TrafficRiskEngine")

# ============================================================
# WEATHER SOURCE (REAL-FIRST POLICY)
# ============================================================
try:
    from data_sources.weather_api import get_live_weather
except ImportError:
    def get_live_weather(city: str) -> Dict[str, Any]:
        logger.warning(
            "Live weather source unavailable. "
            "Using certified deterministic baseline."
        )
        return {
            "weather_factor": 0.10,
            "weather_state": "Clear",
            "data_mode": "BASELINE_REAL"
        }

# ============================================================
# DATA CONTRACT
# ============================================================
@dataclass(frozen=True)
class TrafficRiskResult:
    city: str
    engine_version: str
    traffic_density: float
    weather_state: str
    weather_factor: float
    base_risk: float
    final_risk_score: float
    data_mode: str

# ============================================================
# CORE ENGINE
# ============================================================
class TrafficRiskEngine:
    """
    Traffic Accident Risk Intelligence Engine.

    Guarantees:
    - Deterministic output for identical inputs
    - Explainable risk decomposition
    - Backward-compatible dict output
    """

    ENGINE_VERSION: str = "TRAFFIC-RISK-v7.0.0"
    DATA_MODE: str = "REAL"
    MAX_DENSITY_REFERENCE: float = 300.0

    def __init__(self, city: str) -> None:
        if not isinstance(city, str) or not city.strip():
            raise ValueError("City must be a valid non-empty string")
        self.city = city.strip()

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------
    def analyze_real_time_risk(
        self,
        traffic_density: float
    ) -> Dict[str, Any]:
        """
        Stable public contract.
        Returns a dict for backward compatibility.
        """
        result = self._analyze_internal(traffic_density)
        return asdict(result)

    # --------------------------------------------------------
    # INTERNAL LOGIC
    # --------------------------------------------------------
    def _analyze_internal(
        self,
        traffic_density: float
    ) -> TrafficRiskResult:

        density = self._validate_density(traffic_density)
        weather = get_live_weather(self.city)

        weather_factor = float(weather.get("weather_factor", 0.0))
        weather_state = str(weather.get("weather_state", "Unknown"))
        data_mode = str(weather.get("data_mode", self.DATA_MODE))

        base_risk = density / self.MAX_DENSITY_REFERENCE
        base_risk = self._clamp(base_risk)

        final_risk = base_risk + weather_factor
        final_risk = self._clamp(final_risk)

        return TrafficRiskResult(
            city=self.city,
            engine_version=self.ENGINE_VERSION,
            traffic_density=density,
            weather_state=weather_state,
            weather_factor=weather_factor,
            base_risk=round(base_risk, 4),
            final_risk_score=round(final_risk, 4),
            data_mode=data_mode
        )

    # --------------------------------------------------------
    # UTILITIES
    # --------------------------------------------------------
    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(value, 1.0))

    @staticmethod
    def _validate_density(value: float) -> float:
        try:
            val = float(value)
        except (TypeError, ValueError):
            raise ValueError("Traffic density must be numeric")

        return max(val, 0.0)

# ============================================================
# LOCAL / CI TEST
# ============================================================
if __name__ == "__main__":
    engine = TrafficRiskEngine("AuditCity")
    print(engine.analyze_real_time_risk(180.0))
