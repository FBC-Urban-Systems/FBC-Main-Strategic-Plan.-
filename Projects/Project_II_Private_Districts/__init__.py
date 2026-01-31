"""
FBC Digital Systems
Project II – Private Districts Intelligence Platform

Package Role:
Enterprise-grade operating layer for private smart districts,
including energy optimization, revenue modeling, and district governance.

Classification: EXECUTIVE_CRITICAL
Status: PRODUCTION / AUDIT / INVESTOR READY
Version: v6.0.0-LTS
"""

from __future__ import annotations

# --------------------------------------------------
# PACKAGE METADATA (LOCKED)
# --------------------------------------------------
__version__ = "6.0.0-LTS"
__package_name__ = "FBC_Private_Districts"
__package_role__ = "PRIVATE_DISTRICT_INTELLIGENCE_LAYER"
__classification__ = "EXECUTIVE_CRITICAL"
__data_mode__ = "REAL"
__audit_status__ = "TRACEABLE"

# --------------------------------------------------
# PUBLIC API EXPORTS (STABLE CONTRACT)
# --------------------------------------------------
__all__ = [
    "PrivateDistrictManager",
    "EnergyForecaster",
    "predict_energy_savings"
]

# --------------------------------------------------
# CORE EXPORTS
# --------------------------------------------------
from .district_core import PrivateDistrictManager
from .energy_forecast import EnergyForecaster, predict_energy_savings
