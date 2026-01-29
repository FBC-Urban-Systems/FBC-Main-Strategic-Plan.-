# ==========================================
# PATH: Projects/Project-III-Traffic-Intelligence/accident_pred.py
# DESCRIPTION: FBC AI Risk Engine with Live Weather Integration
# ==========================================

import requests

class TrafficRiskEngine:
    def __init__(self, city_name):
        self.city = city_name
        self.base_risk = 15.0

    def get_live_weather(self):
        """
        Simulating a call to a Weather API. 
        In production, this connects to OpenWeatherMap API.
        """
        # For now, we simulate the 'Live' feel. 
        # Later we will add the API Key.
        import random
        return random.choice(["Clear", "Rainy", "Foggy", "Stormy"])

    def analyze_real_time_risk(self, vehicle_density):
        weather = self.get_live_weather()
        
        multipliers = {"Clear": 1.0, "Rainy": 1.5, "Foggy": 2.0, "Stormy": 3.0}
        multiplier = multipliers.get(weather, 1.0)
        
        raw_score = (vehicle_density * 0.7 * multiplier) + self.base_risk
        risk_score = min(round(raw_score, 2), 100.0)
        
        return {
            "city": self.city,
            "live_weather": weather,
            "risk_score": f"{risk_score}%",
            "status": "CRITICAL" if risk_score > 70 else "STABLE"
        }
