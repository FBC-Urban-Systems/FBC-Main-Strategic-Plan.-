# =====================================================
# FBC URBAN SYSTEMS
# Projects Package Initializer
#
# ROLE:
# - Unified public import surface for all core engines
# - Contract-stable entry point (CI / API / SDK safe)
# - Lazy-load tolerant to avoid hard import failures
#
# VERSION: v3.2.0 (STABLE • ENTERPRISE • FUTURE-READY)
# =====================================================

from __future__ import annotations

__version__ = "3.2.0"

__all__ = [
    "RevenueOptimizer",
    "EnergyForecaster",
    "TrafficRiskEngine",
    "FBCSecureVault",
]

# -----------------------------------------------------
# SAFE / CONTRACT-STABLE IMPORTS
# -----------------------------------------------------
# NOTE:
# Imports are wrapped to prevent package-level crashes
# during partial deployments, CI checks, or future splits.
# -----------------------------------------------------

try:
    # Revenue Optimization Engine
    from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
except Exception as e:  # pragma: no cover
    RevenueOptimizer = None  # type: ignore

try:
    # Energy Forecasting Engine
    from Projects.Project_II_Private_Districts.energy_forecast import EnergyForecaster
except Exception as e:  # pragma: no cover
    EnergyForecaster = None  # type: ignore

try:
    # Traffic Intelligence Engine
    from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
except Exception as e:  # pragma: no cover
    TrafficRiskEngine = None  # type: ignore

try:
    # Secure Ledger Engine
    from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault
except Exception as e:  # pragma: no cover
    FBCSecureVault = None  # type: ignore
