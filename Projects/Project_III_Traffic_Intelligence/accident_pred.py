# ==========================================
# PATH: /Projects/Project_III_Traffic_Intelligence/accident_pred.py
# DESCRIPTION: Traffic Risk Engine with Real-Time Weather Data
# VERSION: v2.0.0-REAL-DATA
# ==========================================

from data_sources.weather_api import get_live_weather

class TrafficRiskEngine:
    def __init__(self, city):
        self.city = city

    def analyze_real_time_risk(self, traffic_density):
        """
        Calculates live traffic risk using:
        - Traffic density input
        - Real-time weather factor
        """

        weather = get_live_weather(self.city)

        weather_factor = weather["weather_factor"]
        weather_state = weather["weather_state"]

        # Core Risk Formula
        base_risk = traffic_density / 300
        live_risk = round((base_risk + weather_factor), 2)

        # Clamp between 0 and 1
        if live_risk > 1:
            live_risk = 1.0

        return {
            "city": self.city,
            "traffic_density": traffic_density,
            "weather": weather_state,
            "risk_score": live_risk
        }
