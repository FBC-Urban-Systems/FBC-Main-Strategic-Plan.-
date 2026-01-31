"""
FBC Digital Systems
Project I — Urban Revenue Optimization & Monetization

Package Role:
Enterprise-grade revenue intelligence and optimization layer
for city-scale financial uplift and monetization.

Status:
Production / Audit / CI-Critical

Version:
v6.1.0-ENTERPRISE-MAX-LTS
"""

from __future__ import annotations

__all__ = [
    "UrbanRevenueAI",
    "RevenueOptimizer",
    "calculate_revenue_boost",
    "__version__",
    "__package_role__",
    "__classification__"
]

# --------------------------------------------------
# PACKAGE METADATA
# --------------------------------------------------
__version__ = "6.1.0"
__package_role__ = "URBAN_REVENUE_INTELLIGENCE_LAYER"
__classification__ = "ENTERPRISE_CRITICAL"

# --------------------------------------------------
# PUBLIC API EXPORTS (CONTRACT SAFE)
# --------------------------------------------------
from .ai_engine_v2 import UrbanRevenueAI
from .revenue_optimizer import RevenueOptimizer
from .revenue_sim import calculate_revenue_boost
