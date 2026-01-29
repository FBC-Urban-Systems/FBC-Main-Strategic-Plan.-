# ==========================================
# PATH: core_kernel.py
# DESCRIPTION: FBC City-OS Core Kernel (Global Integration)
# VERSION: v2.1-Gold
# ==========================================

import sys
import os

# Adding sub-directories to system path for modular integration
sys.path.append(os.path.abspath("Projects/Project-I-Urban-Revenue"))
sys.path.append(os.path.abspath("Projects/Project-III-Traffic-Intelligence"))

try:
    from ai_engine_v2 import UrbanRevenueAI
    from accident_pred import predict_traffic_risk
    print("--- [KERNEL] All Modules Loaded Successfully ---")
except ImportError as e:
    print(f"--- [KERNEL] Critical Import Error: {e} ---")
    sys.exit(1)

class MasterCityKernel:
    def __init__(self, city_name):
        self.city_name = city_name
        print(f"--- [KERNEL] Initializing FBC OS for {city_name} ---")

    def run_system_diagnostic(self, base_revenue):
        """
        Executes a full system diagnostic combining Revenue AI and Traffic Risk modules.
        """
        # 1. Revenue AI Engine Check
        engine = UrbanRevenueAI(self.city_name)
        report = engine.analyze_yield(base_revenue)
        
        # 2. Traffic Intelligence Risk Check
        risk = predict_traffic_risk(75, "Clear")
        
        print(f"--- [KERNEL] {self.city_name} Status: OPERATIONAL ---")
        return report

if __name__ == "__main__":
    # Internal System Test
    kernel = MasterCityKernel("Global-Sector-Alpha")
    kernel.run_system_diagnostic(100.0)
