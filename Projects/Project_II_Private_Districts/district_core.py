# ==========================================
# PATH: Projects/Project-II-Private-Districts/district_core.py
# DESCRIPTION: FBC Private Smart District Management Engine
# VERSION: v4.0-PRIVATE-DISTRICT-GRADE
# TARGET ARR: $20M - $30M by 2030
# ==========================================

from datetime import datetime

class PrivateDistrictManager:
    """
    FBC Private District Operating Core
    Handles onboarding, activation, SaaS billing, and reporting
    """

    def __init__(self, district_id, setup_fee_usd):
        self.district_id = district_id
        self.setup_fee = float(setup_fee_usd)
        self.is_active = False
        self.activation_timestamp = None
        self.manager_version = "DISTRICT-CORE-v4.0"

    # --------------------------------------------------
    # ACTIVATE DISTRICT NODE
    # --------------------------------------------------
    def activate_district(self):
        self.is_active = True
        self.activation_timestamp = datetime.now().isoformat()
        return {
            "district_id": self.district_id,
            "status": "ONLINE",
            "activated_at": self.activation_timestamp
        }

    # --------------------------------------------------
    # CALCULATE ANNUAL SAAS FEES
    # --------------------------------------------------
    def calculate_annual_saas(self, units_count):
        """
        SaaS model:
        Base fee = $500K
        Per-unit scaling = $120 / unit
        Hard cap = $1M annually
        """
        base_fee = 500000
        scale_bonus = units_count * 120
        total_saas = min(base_fee + scale_bonus, 1_000_000)

        return {
            "district_id": self.district_id,
            "units_count": units_count,
            "annual_saas_usd": round(total_saas, 2)
        }

    # --------------------------------------------------
    # TOTAL FIRST YEAR REVENUE
    # --------------------------------------------------
    def first_year_revenue(self, units_count):
        saas_data = self.calculate_annual_saas(units_count)
        total = self.setup_fee + saas_data["annual_saas_usd"]

        return {
            "district_id": self.district_id,
            "setup_fee_usd": self.setup_fee,
            "annual_saas_usd": saas_data["annual_saas_usd"],
            "total_first_year_revenue_usd": round(total, 2)
        }

    # --------------------------------------------------
    # INVESTOR SUMMARY REPORT
    # --------------------------------------------------
    def investor_report(self, units_count):
        rev = self.first_year_revenue(units_count)

        return {
            "district": self.district_id,
            "core_version": self.manager_version,
            "activation_status": self.is_active,
            "first_year_revenue_usd": f"${rev['total_first_year_revenue_usd']:,.2f}",
            "recurring_revenue_usd": f"${rev['annual_saas_usd']:,.2f}"
        }

# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- FBC PRIVATE DISTRICT CORE TEST ---")

    fbc_district = PrivateDistrictManager("Industrial-Zone-A", 1_500_000)

    status = fbc_district.activate_district()
    print("Activation:", status)

    report = fbc_district.investor_report(units_count=4200)
    print("Investor Report:", report)

    print("--- PRIVATE DISTRICT CORE OPERATIONAL ✅ ---\n")
