# ==========================================
# PATH: /simulation_config.py
# DESCRIPTION: FBC Global Simulation Configuration
# VERSION: v1.0.0
# ROLE: Master Parameters for All System Simulations
# ==========================================

from dataclasses import dataclass

@dataclass
class CityNode:
    name: str
    country: str
    base_revenue: float
    base_energy_bill: float
    base_traffic_density: int

# ==========================================
# GLOBAL SIMULATION SETTINGS
# ==========================================

SIMULATION_YEARS = 5
SIMULATION_START_YEAR = 2026

# ==========================================
# INITIAL CITY NODES
# ==========================================

CITY_NODES = [
    CityNode("Austin-TX", "USA", 10_000_000, 200_000, 120),
    CityNode("Cairo", "Egypt", 5_000_000, 150_000, 180),
    CityNode("Dubai", "UAE", 20_000_000, 300_000, 90)
]

# ==========================================
# SYSTEM GLOBAL FLAGS
# ==========================================

ENABLE_LEDGER = True
ENABLE_AI_SAFETY = True
ENABLE_REAL_TIME_STREAMS = False
