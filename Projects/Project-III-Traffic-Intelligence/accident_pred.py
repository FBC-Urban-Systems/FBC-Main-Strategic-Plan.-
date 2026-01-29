# ==========================================
# PATH: Projects/Project-III-Traffic-Intelligence/accident_pred.py
# DESCRIPTION: FBC Urban Traffic Risk Intelligence Engine
# VERSION: v4.0-URBAN-RISK-AI-GRADE
# ==========================================

import random
from datetime import datetime

class TrafficRiskEngine:
    """
    FBC AI Traffic Risk Engine
    Simulates live weather + density-based accident probability scoring
    Ready for real API integration.
    """

    def __init__(self, city_name):
        self.city = city_name
        self.base_risk = 12.0
        self.engine_version = "TRAFFIC-AI-v4.0"

    # --------------------------------------
    # WEATHER PROVIDER LAYER
    # --------------------------------------
    def get_live_weather(self):
        """
        Simulated Live Weather Feed.
        Can be replaced later with real API call without changing core logic.
        """
        weather_states = ["Clear", "Cloudy", "Rainy", "Foggy", "Stormy"]
        return random.choice(weather_states)

    # --------------------------------------
    # CORE RISK ANALYSIS
    # --------------------------------------
    def analyze_real_time_risk(self, vehicle_density):
        """
        Calculates real-time traffic accident risk score.
        Density input range expected: 0 → 300
        """

        weather = self.get_live_weather()

        # Weather impact multipliers
        weather_multiplier = {
            "Clear": 1.0,
            "Cloudy": 1.2,
            "Rainy": 1.6,
            "Foggy": 2.1,
            "Stormy": 2.8
        }

        multiplier = weather_multiplier.get(weather, 1.0)

        # Core AI-inspired risk formula
        raw_score = (vehicle_density * 0.65 * multiplier) + self.base_risk

        # Normalize to 0–100 scale
        risk_score = min(round(raw_score, 2), 100.0)

        # Status classification
        if risk_score < 40:
            status = "LOW_RISK"
        elif risk_score < 70:
            status = "ELEVATED"
        elif risk_score < 90:
            status = "HIGH_RISK"
        else:
            status = "CRITICAL"

        return {
            "city": self.city,
            "timestamp": datetime.now().isoformat(),
            "engine_version": self.engine_version,
            "live_weather": weather,
            "vehicle_density": vehicle_density,
            "risk_score": risk_score,   # numeric clean value
            "risk_percent": f"{risk_score}%",
            "status": status
        }

# --------------------------------------
# STANDALONE ENGINE TEST
# --------------------------------------
if __name__ == "__main__":
    print("\n--- FBC TRAFFIC INTELLIGENCE TEST ---")

    engine = TrafficRiskEngine("Austin-TX")

    for density in [50, 120, 200, 280]:
        result = engine.analyze_real_time_risk(density)
        print(
            f"City: {result['city']} | "
            f"Density: {density} | "
            f"Weather: {result['live_weather']} | "
            f"Risk: {result['risk_percent']} | "
            f"Status: {result['status']}"
        )

    print("--- TRAFFIC AI OPERATIONAL ✅ ---\n")
