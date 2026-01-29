# =====================================================
# FBC URBAN SYSTEMS - UNIFIED API GATEWAY
# Core Service Bridge for All AI Engines
# =====================================================

from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import EnergyForecaster
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault

class FBC_API_Gateway:
    """
    Unified Gateway to access all FBC AI Engines
    """

    def __init__(self):
        self.revenue_engine = RevenueOptimizer()
        self.energy_engine = EnergyForecaster()
        self.traffic_engine = TrafficRiskEngine("GLOBAL")
        self.vault = FBCSecureVault()

    # -------------------------------
    # Revenue Simulation Endpoint
    # -------------------------------
    def simulate_revenue(self, city: str, population: int):
        result = self.revenue_engine.simulate(city, population)
        proof = self.vault.generate_proof("REVENUE_SIM", city, result)
        return {
            "city": city,
            "population": population,
            "projected_revenue": result,
            "audit": proof
        }

    # -------------------------------
    # Energy Forecast Endpoint
    # -------------------------------
    def forecast_energy(self, city: str, population: int, price_per_kwh: float):
        result = self.energy_engine.forecast(city, population, price_per_kwh)
        proof = self.vault.generate_proof("ENERGY_FORECAST", city, result)
        return {
            "city": city,
            "population": population,
            "energy_price": price_per_kwh,
            "projected_energy_cost": result,
            "audit": proof
        }

    # -------------------------------
    # Traffic Risk Endpoint
    # -------------------------------
    def traffic_risk(self, city: str, density: int):
        result = self.traffic_engine.analyze_real_time_risk(density)
        proof = self.vault.generate_proof("TRAFFIC_RISK", city, result["risk_score"])
        return {
            "city": city,
            "traffic_density": density,
            "risk_analysis": result,
            "audit": proof
        }


# =====================================================
# Simple Local Test
# =====================================================
if __name__ == "__main__":
    api = FBC_API_Gateway()

    print("=== Revenue Test ===")
    print(api.simulate_revenue("Cairo", 5000000))

    print("=== Energy Test ===")
    print(api.forecast_energy("Cairo", 5000000, 0.12))

    print("=== Traffic Risk Test ===")
    print(api.traffic_risk("Cairo", 120))
