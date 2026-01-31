"""
FBC Digital Systems
Project III – Traffic Intelligence & Risk Systems

Package Role:
City-scale traffic risk intelligence engines providing
deterministic, auditable, and insurance-grade analytics.

Version: v7.0.0
Classification: Executive-Critical
"""

from __future__ import annotations

__all__ = [
    "TrafficRiskEngine",
    "__version__",
    "__package_role__",
    "__classification__"
]

# ------------------------------------------------------------
# Package Metadata
# ------------------------------------------------------------
__version__ = "7.0.0"
__package_role__ = "TRAFFIC_RISK_INTELLIGENCE_CORE"
__classification__ = "EXECUTIVE_CRITICAL"

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
from .accident_pred import TrafficRiskEngine
