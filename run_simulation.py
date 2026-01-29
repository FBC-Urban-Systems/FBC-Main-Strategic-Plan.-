# ==========================================
# PATH: /run_simulation.py
# UPDATED VERSION: v1.1.0
# ==========================================

from simulation_config import CITY_NODES, SIMULATION_YEARS
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from data_core import store_simulation_result

def run_global_simulation():
    results = []

    for city in CITY_NODES:
        print(f"\n--- Simulating {city.name} ---")

        rev_engine = RevenueOptimizer(city.name)
        rev_result = rev_engine.project_incremental_gain(city.base_revenue)

        energy_result = predict_energy_savings(city.base_energy_bill)

        traffic_engine = TrafficRiskEngine(city.name)
        traffic_result = traffic_engine.analyze_real_time_risk(city.base_traffic_density)

        revenue_gain = rev_result["Total_City_Gain"]
        energy_savings = energy_result["ai_predicted_savings"]
        risk_score = traffic_result["risk_score"]

        # Store into Data Core
        store_simulation_result(city.name, revenue_gain, energy_savings, risk_score)

        results.append({
            "city": city.name,
            "years": SIMULATION_YEARS,
            "revenue_gain": revenue_gain,
            "energy_savings": energy_savings,
            "risk_score": risk_score
        })

    return results


if __name__ == "__main__":
    sim_results = run_global_simulation()
    print("\n========== GLOBAL SIMULATION RESULTS ==========")
    for r in sim_results:
        print(r)
