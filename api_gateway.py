# =====================================================
# PATH: /api_gateway.py
# DESCRIPTION: FBC Unified Internal API Gateway
# VERSION: v3.0.0 — REAL DATA LOCKED • FUTURE PROOF
# ROLE: Internal Service-Orchestration Layer for AI Engines
# =====================================================

from typing import Dict, Any

# -----------------------------------------------------
# CORE ENGINE IMPORTS (REAL DATA ONLY)
# -----------------------------------------------------
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault


class FBC_APIGateway:
    """
    Unified internal gateway that orchestrates all FBC AI engines.

    This class is NOT an HTTP layer.
    It is designed for:
    - Simulations
    - Batch processing
    - Internal services
    - Future SDK exposure
    """

    def __init__(self, default_city: str = "GLOBAL"):
        self.vault = FBCSecureVault()
        self.default_city = default_city

    # =================================================
    # REVENUE INTELLIGENCE
    # =================================================
    def simulate_revenue(self, city: str, annual_revenue: float) -> Dict[str, Any]:
        if annual_revenue <= 0:
            raise ValueError("Annual revenue must be positive")

        engine = RevenueOptimizer(city)
        result = engine.project_incremental_gain(annual_revenue)

        audit = self.vault.generate_proof(
            project="REVENUE_SIMULATION",
            entity=city,
            value=result["Total_City_Gain"],
        )

        return {
            "city": city,
            "input_revenue": annual_revenue,
            "output": result,
            "audit": audit,
            "data_mode": "REAL",
        }

    # =================================================
    # ENERGY INTELLIGENCE
    # =================================================
    def forecast_energy_savings(
        self, city: str, annual_energy_bill: float
    ) -> Dict[str, Any]:
        if annual_energy_bill <= 0:
            raise ValueError("Energy bill must be positive")

        result = predict_energy_savings(annual_energy_bill)

        audit = self.vault.generate_proof(
            project="ENERGY_FORECAST",
            entity=city,
            value=result["ai_predicted_savings"],
        )

        return {
            "city": city,
            "input_energy_bill": annual_energy_bill,
            "output": result,
            "audit": audit,
            "data_mode": "REAL",
        }

    # =================================================
    # TRAFFIC INTELLIGENCE
    # =================================================
    def analyze_traffic_risk(
        self, city: str, traffic_density: int
    ) -> Dict[str, Any]:
        if traffic_density < 0:
            raise ValueError("Traffic density must be non-negative")

        engine = TrafficRiskEngine(city)
        result = engine.analyze_real_time_risk(traffic_density)

        audit = self.vault.generate_proof(
            project="TRAFFIC_RISK",
            entity=city,
            value=result["risk_score"],
        )

        return {
            "city": city,
            "traffic_density": traffic_density,
            "output": result,
            "audit": audit,
            "data_mode": "REAL",
        }


# =====================================================
# LOCAL SMOKE TEST (CI SAFE)
# =====================================================
if __name__ == "__main__":
    gateway = FBC_APIGateway()

    print("=== Revenue Simulation ===")
    print(gateway.simulate_revenue("Cairo", 5_000_000))

    print("\n=== Energy Forecast ===")
    print(gateway.forecast_energy_savings("Cairo", 150_000))

    print("\n=== Traffic Risk ===")
    print(gateway.analyze_traffic_risk("Cairo", 120))
