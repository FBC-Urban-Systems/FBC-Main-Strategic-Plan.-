"""
FBC Digital Systems
Project III – Traffic Intelligence & Risk Systems

Package Role:
City-scale traffic risk intelligence engines providing
deterministic, auditable, and insurance-grade analytics.

Version: v5.0.0-ENTERPRISE-LTS
Classification: MISSION_CRITICAL
"""

from __future__ import annotations

__all__ = [
    "TrafficRiskEngine",
    "__version__",
    "__package_role__",
    "__classification__",
    "__stability__"
]

# ------------------------------------------------------------
# Package Metadata
# ------------------------------------------------------------
__version__ = "5.0.0"
__package_role__ = "TRAFFIC_RISK_INTELLIGENCE_CORE"
__classification__ = "MISSION_CRITICAL"
__stability__ = "LTS"

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
from .accident_pred import TrafficRiskEngine
