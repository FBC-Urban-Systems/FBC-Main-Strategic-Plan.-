# ==========================================
# PATH: /simulation_config.py
# DESCRIPTION: FBC Global Simulation Configuration
# VERSION: v2.0.0-REAL-DATA
# ROLE: Master Parameters using Real Population Data
# ==========================================

from dataclasses import dataclass
from data_sources.population_data import get_country_population

@dataclass
class CityNode:
    name: str
    country_code: str
    base_revenue: float
    base_energy_bill: float
    base_traffic_density: int
    population: int

# ==========================================
# Fetch Real Population Data
# ==========================================

def load_population(country_code, fallback):
    data = get_country_population(country_code)
    if data and data["population"]:
        return data["population"]
    return fallback

# ==========================================
# GLOBAL SIMULATION SETTINGS
# ==========================================

SIMULATION_YEARS = 5
SIMULATION_START_YEAR = 2026

# ==========================================
# INITIAL CITY NODES (Now Using Real Population)
# ==========================================

CITY_NODES = [
    CityNode(
        name="Cairo",
        country_code="EG",
        base_revenue=5_000_000,
        base_energy_bill=150_000,
        base_traffic_density=180,
        population=load_population("EG", 20_000_000)
    ),
    CityNode(
        name="Austin-TX",
        country_code="US",
        base_revenue=10_000_000,
        base_energy_bill=200_000,
        base_traffic_density=120,
        population=load_population("US", 330_000_000)
    ),
    CityNode(
        name="Dubai",
        country_code="AE",
        base_revenue=20_000_000,
        base_energy_bill=300_000,
        base_traffic_density=90,
        population=load_population("AE", 10_000_000)
    )
]
