"""
FBC Digital Systems
Project VI – Global Dominance & Planetary Expansion

Package Role:
Core control package for planetary-scale expansion,
valuation modeling, and Digital Earth execution logic.

Version: v7.0.0
Status: Production / Audit / IPO Grade
"""

from __future__ import annotations

__all__ = [
    "FBCPlanetaryGrowthEngine",
    "__version__",
    "__package_role__",
    "__classification__"
]

# ------------------------------------------------------------
# Package Metadata
# ------------------------------------------------------------
__version__ = "7.0.0"
__package_role__ = "PLANETARY_EXPANSION_CONTROL_LAYER"
__classification__ = "EXECUTIVE_CRITICAL"

# ------------------------------------------------------------
# Public API Exports
# ------------------------------------------------------------
from .global_expansion_sim import FBCPlanetaryGrowthEngine
