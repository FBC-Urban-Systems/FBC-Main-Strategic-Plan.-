# ==========================================
# PATH: /Projects/Project_II_Private_Districts/energy_forecast.py
# DESCRIPTION: Energy Forecast Engine using Real Electricity Price Data
# VERSION: v2.0.0-REAL-DATA
# ==========================================

from data_sources.energy_price_data import get_country_energy_price
from data_sources.population_data import get_country_population

class EnergyForecaster:
    def __init__(self, country_code):
        self.country_code = country_code.upper()
        self.energy_price_data = get_country_energy_price(self.country_code)
        self.population_data = get_country_population(self.country_code)

    def forecast(self):
        """
        Forecasts national-scale energy cost using:
        - Real electricity price per kWh
        - Real population data
        """

        if not self.energy_price_data or not self.population_data:
            return {"error": "Real energy data unavailable"}

        price_per_kwh = self.energy_price_data["price_per_kwh"]
        population = self.population_data["population"]

        # Assumption: average annual kWh consumption per capita
        avg_kwh_per_capita = 1800  

        total_kwh = population * avg_kwh_per_capita
        total_energy_cost = total_kwh * price_per_kwh

        # FBC optimization savings assumption 12%
        fbc_savings = total_energy_cost * 0.12

        return {
            "country": self.country_code,
            "price_per_kwh": price_per_kwh,
            "population": population,
            "total_energy_cost_usd": round(total_energy_cost, 2),
            "fbc_projected_savings": round(fbc_savings, 2)
        }
