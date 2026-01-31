"""
FBC Digital Systems
Project III – Security Ledger

Package Role:
Immutable security, audit, and financial ledger infrastructure
used across sector, city, and planetary systems.

Version: v7.0.0
Classification: Executive-Critical
"""

from __future__ import annotations

__all__ = [
    "FBCSecureVault",
    "__version__",
    "__package_role__",
    "__classification__"
]

# ------------------------------------------------------------
# Package Metadata
# ------------------------------------------------------------
__version__ = "7.0.0"
__package_role__ = "IMMUTABLE_SECURITY_LEDGER_CORE"
__classification__ = "EXECUTIVE_CRITICAL"

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
from .secure_vault import FBCSecureVault
