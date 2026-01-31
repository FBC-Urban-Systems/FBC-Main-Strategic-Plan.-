"""
FBC Digital Systems
Project III – Security Ledger

Package Role:
Immutable security, audit, and financial ledger infrastructure
used across sector, city, and planetary systems.

Version: v5.0.0-ENTERPRISE-LTS
Stability: Long-Term Support (LTS)
Classification: Executive-Critical
"""

from __future__ import annotations

# ------------------------------------------------------------
# ENTERPRISE METADATA (STABLE)
# ------------------------------------------------------------
__version__ = "5.0.0-ENTERPRISE-LTS"
__package_role__ = "IMMUTABLE_SECURITY_LEDGER_CORE"
__classification__ = "EXECUTIVE_CRITICAL"
__organization__ = "FBC Digital Systems"
__stability__ = "LTS"

# ------------------------------------------------------------
# PUBLIC API (EXPLICIT)
# ------------------------------------------------------------
from .secure_vault import FBCSecureVault

__all__ = [
    "FBCSecureVault",
    "__version__",
    "__package_role__",
    "__classification__",
    "__organization__",
    "__stability__",
]
