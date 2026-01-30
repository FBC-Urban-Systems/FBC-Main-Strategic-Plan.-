# ==========================================
# PATH: /Projects/Project_I_Urban_Revenue/revenue_optimizer.py
# DESCRIPTION: Revenue Optimization Engine using Real GDP Data
# VERSION: v3.0.0-REAL-DATA
# ==========================================

from data_sources.gdp_data import get_country_gdp
from data_sources.population_data import get_country_population

class RevenueOptimizer:
    def __init__(self, country_code):
        self.country_code = country_code.upper()

        self.gdp_data = get_country_gdp(self.country_code)
        self.pop_data = get_country_population(self.country_code)

    def project_incremental_gain(self):
        """
        Calculates projected city revenue optimization
        based on real GDP and population data.
        """

        if not self.gdp_data or not self.pop_data:
            return {"error": "Real data unavailable"}

        gdp = self.gdp_data["gdp_usd"]
        population = self.pop_data["population"]

        # Estimate average city share from national GDP
        gdp_per_capita = gdp / population

        # Assume optimized city captures 8% GDP activity
        estimated_city_revenue = gdp * 0.08

        # FBC optimization gain assumption 3%
        fbc_gain = estimated_city_revenue * 0.03

        return {
            "country": self.country_code,
            "gdp_year": self.gdp_data["year"],
            "population_year": self.pop_data["year"],
            "gdp_per_capita": round(gdp_per_capita, 2),
            "estimated_city_revenue": round(estimated_city_revenue, 2),
            "fbc_projected_gain": round(fbc_gain, 2)
        }
