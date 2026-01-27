# FBC Digital Systems - Project IV: City Operating System (COS)
# Core Kernel: Centralized Decision Engine (2030-2033)

class CityOSKernel:
    def __init__(self, city_name):
        self.city_name = city_name
        self.systems_status = "Online"

    def process_urban_data(self, traffic_load, energy_demand, emergency_level):
        """
        Integrates multiple urban streams to optimize city performance.
        Priority: 1. Emergency | 2. Traffic | 3. Energy
        """
        decision_log = []
        
        # Logic for Emergency Response
        if emergency_level > 5:
            decision_log.append("EMERGENCY: Rerouting traffic & prioritizing power to hospitals.")
        
        # Logic for Traffic Optimization
        if traffic_load > 80:
            decision_log.append("TRAFFIC: Activating dynamic lane management.")
            
        # Logic for Energy Savings
        if energy_demand > 70:
            decision_log.append("ENERGY: Reducing non-essential street lighting.")

        return {
            "city": self.city_name,
            "status": self.systems_status,
            "actions_taken": decision_log
        }

# Initializing COS for a smart city
fbc_cos = CityOSKernel("New-Capital-X")
status_report = fbc_cos.process_urban_data(traffic_load=85, energy_demand=75, emergency_level=2)

print(f"City-OS Status for {status_report['city']}: {status_report['actions_taken']}")
