# ==========================================
# PATH: Projects/Project-I-Urban-Revenue/ai_engine_v2.py
# DESCRIPTION: FBC AI Engine - Manifest-Driven Revenue Optimization
# VERSION: v2.7-Stable
# ==========================================

import json
import os
import numpy as np
from datetime import datetime

class UrbanRevenueAI:
    def __init__(self, city_name):
        self.city_name = city_name
        self.boost_factor = 0.25  # FBC Standard 25% Boost
        self.manifest_data = self._load_manifest()

    def _load_manifest(self):
        """
        Locates and loads the Global Cities Manifest to get real economic data.
        """
        # Look for the manifest in the root directory relative to this project
        path = os.path.join(os.getcwd(), 'global_cities_manifest.json')
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                nodes = data.get('financial_model_v2', {}).get('expansion_nodes', [])
                for node in nodes:
                    if node['city'].lower() == self.city_name.lower():
                        return node
            return None
        except Exception as e:
            print(f"--- [SYSTEM ERROR] Manifest unreachable: {e} ---")
            return None

    def analyze_yield(self):
        """
        Calculates optimized revenue using data from the manifest.
        """
        if not self.manifest_data:
            return {"error": f"City '{self.city_name}' not found in global manifest."}

        # Pulling the base revenue directly from your JSON file
        base_val = self.manifest_data['expected_revenue_m']
        
        # Simulating AI Intelligence: adding market volatility (-2% to +5%)
        volatility = np.random.uniform(-0.02, 0.05)
        final_gain_percent = self.boost_factor + volatility
        
        optimized_total = base_val * (1 + final_gain_percent)
        net_profit = optimized_total - base_val
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": self.city_name,
            "region": self.manifest_data['region'],
            "metrics": {
                "base_revenue_m": f"${base_val}M",
                "ai_boost_percent": f"{final_gain_percent*100:.2f}%",
                "fbc_optimized_total_m": f"${optimized_total:.2f}M",
                "net_value_created_m": f"${net_profit:.2f}M"
            }
        }

if __name__ == "__main__":
    # Test Run: Analyze Austin based on the real JSON data
    engine = UrbanRevenueAI("Austin")
    report = engine.analyze_yield()
    
    print("--- [FBC REVENUE ENGINE REPORT] ---")
    print(json.dumps(report, indent=4))
