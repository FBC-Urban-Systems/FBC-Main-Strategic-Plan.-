# ==========================================
# PATH: Projects/Project_II_Private_Districts/district_core.py
# DESCRIPTION: FBC Private Smart District Management Engine
# VERSION: v5.0-SUPREME-PRIVATE-DISTRICT
# DATA MODE: REAL
# GOVERNANCE: ENTERPRISE / AUDIT-READY
# ==========================================

from datetime import datetime
from typing import Dict


class PrivateDistrictManager:
    """
    FBC Private District Operating Core (Enterprise Supreme)

    Responsibilities:
    - District lifecycle management
    - SaaS revenue computation
    - Investor-grade reporting
    - Forward-compatible financial governance
    """

    CORE_VERSION = "DISTRICT-CORE-v5.0-SUPREME"
    DATA_MODE = "REAL"

    # Enterprise financial constants (centralized & auditable)
    BASE_SAAS_FEE_USD = 500_000
    PER_UNIT_FEE_USD = 120
    SAAS_CAP_USD = 1_000_000

    def __init__(self, district_id: str, setup_fee_usd: float):
        self.district_id = str(district_id)
        self.setup_fee = float(setup_fee_usd)

        self.is_active = False
        self.activation_timestamp = None
        self.manager_version = self.CORE_VERSION

    # --------------------------------------------------
    # ACTIVATE DISTRICT NODE
    # --------------------------------------------------
    def activate_district(self) -> Dict[str, str]:
        """
        Activates the district in REAL data mode.
        Idempotent-safe (calling twice won't corrupt state).
        """
        if not self.is_active:
            self.is_active = True
            self.activation_timestamp = datetime.utcnow().isoformat()

        return {
            "district_id": self.district_id,
            "status": "ONLINE",
            "activated_at": self.activation_timestamp,
            "data_mode": self.DATA_MODE
        }

    # --------------------------------------------------
    # CALCULATE ANNUAL SAAS FEES
    # --------------------------------------------------
    def calculate_annual_saas(self, units_count: int) -> Dict[str, float]:
        """
        Deterministic SaaS pricing model (Enterprise Contract Safe)

        - Base fee: $500,000
        - Per-unit scaling: $120 / unit
        - Annual hard cap: $1,000,000
        """
        units = max(int(units_count), 0)

        variable_fee = units * self.PER_UNIT_FEE_USD
        total_saas = min(
            self.BASE_SAAS_FEE_USD + variable_fee,
            self.SAAS_CAP_USD
        )

        return {
            "district_id": self.district_id,
            "units_count": units,
            "annual_saas_usd": round(total_saas, 2)
        }

    # --------------------------------------------------
    # TOTAL FIRST YEAR REVENUE
    # --------------------------------------------------
    def first_year_revenue(self, units_count: int) -> Dict[str, float]:
        """
        First-year revenue = Setup fee + Annual SaaS
        """
        saas_data = self.calculate_annual_saas(units_count)

        total = self.setup_fee + saas_data["annual_saas_usd"]

        return {
            "district_id": self.district_id,
            "setup_fee_usd": round(self.setup_fee, 2),
            "annual_saas_usd": saas_data["annual_saas_usd"],
            "total_first_year_revenue_usd": round(total, 2)
        }

    # --------------------------------------------------
    # INVESTOR SUMMARY REPORT
    # --------------------------------------------------
    def investor_report(self, units_count: int) -> Dict[str, str]:
        """
        Investor-safe, presentation-ready report.
        Formatting isolated here (core math stays numeric).
        """
        revenue = self.first_year_revenue(units_count)

        return {
            "district_id": self.district_id,
            "core_version": self.manager_version,
            "activation_status": self.is_active,
            "data_mode": self.DATA_MODE,
            "first_year_revenue_usd": f"${revenue['total_first_year_revenue_usd']:,.2f}",
            "recurring_revenue_usd": f"${revenue['annual_saas_usd']:,.2f}"
        }


# --------------------------------------------------
# STANDALONE ENTERPRISE SELF-TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- FBC PRIVATE DISTRICT CORE SUPREME TEST ---")

    district = PrivateDistrictManager("Industrial-Zone-A", 1_500_000)

    status = district.activate_district()
    print("Activation:", status)

    report = district.investor_report(units_count=4200)
    print("Investor Report:", report)

    print("--- PRIVATE DISTRICT CORE OPERATIONAL ✅ ---\n")
