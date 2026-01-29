# ==========================================
# PATH: /Projects/Project_III_Traffic_Intelligence/accident_pred.py
# DESCRIPTION: Traffic Risk Intelligence Engine
# VERSION: v2.0.0-RISK-MODEL
# ROLE: Realistic Urban Traffic Risk Prediction
# ==========================================

import random
import math

class TrafficRiskEngine:
    def __init__(self, city_name: str):
        self.city = city_name

    def analyze_real_time_risk(self, traffic_density: int):
        """
        Computes realistic traffic risk score based on density,
        stochastic weather impact, and time fluctuation.
        """

        # Normalize density impact
        density_factor = min(traffic_density / 300, 1.0)

        # Weather randomness (0 = clear, 1 = storm)
        weather_factor = random.uniform(0.0, 1.0)

        # Time-of-day risk curve (simulated sine wave)
        time_factor = abs(math.sin(random.uniform(0, math.pi)))

        # Combined weighted risk score
        raw_risk = (
            (density_factor * 0.5) +
            (weather_factor * 0.3) +
            (time_factor * 0.2)
        )

        # Scale to 0–100
        risk_score = round(raw_risk * 100, 2)

        # Human-readable weather state
        if weather_factor < 0.3:
            weather_state = "Clear"
        elif weather_factor < 0.7:
            weather_state = "Rain"
        else:
            weather_state = "Storm"

        return {
            "City": self.city,
            "risk_score": risk_score,
            "live_weather": weather_state,
            "traffic_density": traffic_density
        }
