# =========================================================
# PATH: /run_simulation.py
# DESCRIPTION: Global Simulation Execution Engine
# VERSION: v2.1.0 (ENTERPRISE STABLE)
# CLASSIFICATION: PRODUCTION / AUDIT / CI-SAFE
# ROLE: Deterministic Orchestrator for City-Level AI Engines
# DATA MODE: REALISTIC-DETERMINISTIC
# =========================================================

from typing import List, Dict
from datetime import datetime

from simulation_config import CITY_NODES, SIMULATION_YEARS
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from data_core import store_simulation_result


# =========================================================
# GLOBAL SIMULATION ORCHESTRATOR
# =========================================================
def run_global_simulation() -> List[Dict[str, object]]:
    """
    Executes a deterministic global simulation across all
    configured city nodes.

    Guarantees:
    - No randomness
    - No shared mutable state
    - City-level isolation
    - Audit-safe outputs
    """

    results: List[Dict[str, object]] = []
    execution_timestamp: str = datetime.utcnow().isoformat() + "Z"

    for city in CITY_NODES:
        # -------------------------------------------------
        # Revenue Optimization Engine
        # -------------------------------------------------
        revenue_engine = RevenueOptimizer(city.name)
        revenue_result = revenue_engine.project_incremental_gain(
            base_revenue=city.base_revenue
        )

        # -------------------------------------------------
        # Energy Optimization Engine
        # -------------------------------------------------
        energy_result = predict_energy_savings(
            city.base_energy_bill
        )

        # -------------------------------------------------
        # Traffic Risk Intelligence Engine
        # -------------------------------------------------
        traffic_engine = TrafficRiskEngine(city.name)
        traffic_result = traffic_engine.analyze_real_time_risk(
            city.base_traffic_density
        )

        # -------------------------------------------------
        # Normalize Outputs (Strict Casting)
        # -------------------------------------------------
        revenue_gain: float = float(
            revenue_result.get("Total_City_Gain", 0.0)
        )
        energy_savings: float = float(
            energy_result.get("ai_predicted_savings", 0.0)
        )
        risk_score: float = float(
            traffic_result.get("risk_score", 0.0)
        )

        # -------------------------------------------------
        # Persist Results (Deterministic Side-Effect)
        # -------------------------------------------------
        store_simulation_result(
            city=city.name,
            revenue_gain=revenue_gain,
            energy_savings=energy_savings,
            risk_score=risk_score,
            executed_at=execution_timestamp
        )

        # -------------------------------------------------
        # Append Structured Result
        # -------------------------------------------------
        results.append({
            "city": city.name,
            "simulation_years": SIMULATION_YEARS,
            "population": city.population,
            "revenue_gain": revenue_gain,
            "energy_savings": energy_savings,
            "risk_score": risk_score,
            "executed_at": execution_timestamp,
            "data_mode": "REALISTIC-DETERMINISTIC"
        })

    return results


# =========================================================
# CLI EXECUTION MODE (CI SAFE)
# =========================================================
if __name__ == "__main__":
    simulation_results = run_global_simulation()

    print("========== GLOBAL SIMULATION RESULTS ==========")
    for record in simulation_results:
        print(record)
