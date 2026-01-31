"""
FBC Digital Systems
Project VI – Global Dominance & Planetary Expansion

ROLE:
Enterprise MAX package entrypoint for planetary-scale expansion,
ARR growth orchestration, valuation modeling, and Digital Earth execution.

COMPLIANCE:
- IPO / Audit / Board Grade
- Deterministic & Reproducible
- CI / Governance Ready

VERSION: v7.1.0-LTS-ENTERPRISE-MAX
CLASSIFICATION: EXECUTIVE_CRITICAL
"""

from __future__ import annotations

# ============================================================
# PACKAGE METADATA (MAX ENTERPRISE)
# ============================================================
__version__ = "7.1.0-LTS-ENTERPRISE-MAX"
__package_role__ = "PLANETARY_EXPANSION_CONTROL_LAYER"
__classification__ = "EXECUTIVE_CRITICAL"
__audit_profile__ = "ENTERPRISE_MAX"
__audit_mode__ = "CONTINUOUS_AUTONOMOUS"
__lifecycle_status__ = "PRODUCTION_LTS"

# ============================================================
# PUBLIC API SURFACE
# ============================================================
__all__ = [
    "FBCPlanetaryGrowthEngine",
    "__version__",
    "__package_role__",
    "__classification__",
    "__audit_profile__",
    "__audit_mode__",
    "__lifecycle_status__"
]

# ============================================================
# PUBLIC ENGINE EXPORTS
# ============================================================
from .global_expansion_sim import FBCPlanetaryGrowthEngine
