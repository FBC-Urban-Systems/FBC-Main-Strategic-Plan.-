# =====================================================
# FBC URBAN SYSTEMS
# Projects Package Initializer
#
# ROLE:
# - Unified public import surface for all core engines
# - Contract-stable entry point (CI / API / SDK safe)
# - Explicit failure signaling for missing engines
#
# VERSION: v3.3.0 (STABLE • ENTERPRISE • FUTURE-READY)
# =====================================================

from __future__ import annotations
from typing import TYPE_CHECKING

__version__ = "3.3.0"

__all__ = [
    "RevenueOptimizer",
    "EnergyForecaster",
    "TrafficRiskEngine",
    "FBCSecureVault",
]

# -----------------------------------------------------
# INTERNAL IMPORT GUARD
# -----------------------------------------------------

class _MissingDependency:
    """
    Placeholder object returned when an engine fails to import.
    Accessing it raises a clear, contract-safe error instead
    of failing silently or at import time.
    """

    def __init__(self, name: str, reason: Exception):
        self._name = name
        self._reason = reason

    def __getattr__(self, item):
        raise ImportError(
            f"{self._name} is unavailable due to an import failure: {self._reason}"
        )

    def __call__(self, *args, **kwargs):
        raise ImportError(
            f"{self._name} cannot be instantiated due to an import failure: {self._reason}"
        )


# -----------------------------------------------------
# CONTRACT-STABLE ENGINE IMPORTS
# -----------------------------------------------------

try:
    from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
except Exception as exc:  # pragma: no cover
    RevenueOptimizer = _MissingDependency("RevenueOptimizer", exc)  # type: ignore


try:
    from Projects.Project_II_Private_Districts.energy_forecast import EnergyForecaster
except Exception as exc:  # pragma: no cover
    EnergyForecaster = _MissingDependency("EnergyForecaster", exc)  # type: ignore


try:
    from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
except Exception as exc:  # pragma: no cover
    TrafficRiskEngine = _MissingDependency("TrafficRiskEngine", exc)  # type: ignore


try:
    from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault
except Exception as exc:  # pragma: no cover
    FBCSecureVault = _MissingDependency("FBCSecureVault", exc)  # type: ignore


# -----------------------------------------------------
# TYPE CHECKING SUPPORT (STATIC ANALYSIS ONLY)
# -----------------------------------------------------
if TYPE_CHECKING:  # pragma: no cover
    from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
    from Projects.Project_II_Private_Districts.energy_forecast import EnergyForecaster
    from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
    from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault
