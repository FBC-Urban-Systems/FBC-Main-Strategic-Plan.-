# ==========================================
# PATH: Projects/Project-VI-Global-Dominance/global_expansion_sim.py
# DESCRIPTION: FBC Planetary Expansion & Valuation Simulation Engine
# VERSION: v6.0-PLANETARY-GRADE
# ==========================================

import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==========================================
# LOAD GLOBAL MANIFEST
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "global_cities_manifest.json"

class ManifestLoadError(Exception):
    pass


class FBCPlanetaryGrowthEngine:
    """
    Simulates FBC expansion from 2027 → 2037
    Using official Strategic Plan & Global Cities Manifest
    """

    def __init__(self):
        self.manifest = self.load_manifest()
        self.arr_projection = self.manifest["financial_model"]["arr_projection_usd_m"]
        self.valuation_targets = self.manifest["financial_model"]["valuation_targets_usd_b"]
        self.expansion_strategy = self.manifest["global_expansion_strategy"]
        self.target_cities_final = self.manifest["digital_earth_layer"]["network_scale_targets"]["cities_connected"]
        self.valuation_multiple = 25  # High-growth Urban AI SaaS benchmark

    # --------------------------------------
    # Manifest Loader
    # --------------------------------------
    def load_manifest(self):
        if not MANIFEST_PATH.exists():
            raise ManifestLoadError("Global Cities Manifest not found.")
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)

    # --------------------------------------
    # Core Simulation
    # --------------------------------------
    def run_simulation(self):
        results = []
        active_cities = 0

        for year in range(2027, 2038):

            # Phase logic based on Strategic Plan
            if year <= 2029:
                active_cities += len(self.expansion_strategy["phase_1_2027_2029"]["target_cities"])
            elif year <= 2031:
                active_cities += len(self.expansion_strategy["phase_2_2030_2031"]["target_cities"])
            elif year <= 2034:
                active_cities += len(self.expansion_strategy["phase_3_2032_2034"]["target_cities"])
            else:
                # Scale to planetary target
                remaining = self.target_cities_final - active_cities
                active_cities += max(1, remaining // 3)

            active_cities = min(active_cities, self.target_cities_final)

            # ARR projection reference
            arr_year_key = str(year if str(year) in self.arr_projection else max(self.arr_projection.keys()))
            arr_value_m = self.arr_projection[arr_year_key]

            # Valuation calculation
            valuation_b = (arr_value_m * self.valuation_multiple) / 1000

            results.append({
                "Year": year,
                "Active_Cities": active_cities,
                "ARR_USD_M": round(arr_value_m, 2),
                "Estimated_Valuation_USD_B": round(valuation_b, 2)
            })

        return pd.DataFrame(results)

    # --------------------------------------
    # Executive Report Generator
    # --------------------------------------
    def generate_executive_report(self, df: pd.DataFrame):
        final = df.iloc[-1]

        status = "GOAL REACHED ✅" if final["Estimated_Valuation_USD_B"] >= \
                 self.valuation_targets["ipo_2037"] else "PHASE IV REQUIRED ⚠️"

        report = {
            "simulation_timestamp_utc": datetime.utcnow().isoformat(),
            "final_year": int(final["Year"]),
            "final_active_cities": int(final["Active_Cities"]),
            "final_arr_usd_m": float(final["ARR_USD_M"]),
            "final_estimated_valuation_usd_b": float(final["Estimated_Valuation_USD_B"]),
            "target_valuation_usd_b": self.valuation_targets["ipo_2037"],
            "status": status
        }

        return report

# ==========================================
# CLI Execution
# ==========================================
if __name__ == "__main__":
    engine = FBCPlanetaryGrowthEngine()
    df_results = engine.run_simulation()
    executive_report = engine.generate_executive_report(df_results)

    print("\n=== FBC PLANETARY EXPANSION SIMULATION ===\n")
    print(df_results.to_string(index=False))
    print("\n=== EXECUTIVE STRATEGIC SUMMARY ===\n")
    for k, v in executive_report.items():
        print(f"{k}: {v}")
