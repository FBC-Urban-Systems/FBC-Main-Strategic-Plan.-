"""
FBC Digital Systems
Project V — Digital Earth & Planetary Urban Intelligence Exchange

Package Initialization:
Enterprise-grade data exchange core entrypoint, exports public API.

Version: v7.0.0-LTS
Classification: ENTERPRISE CRITICAL
Data Mode: REAL-TIME / DETERMINISTIC
"""

from __future__ import annotations

__all__ = [
    "DigitalEarthEngine",
    "__version__",
    "__package_role__",
    "__classification__"
]

# --------------------------------------------------
# PACKAGE METADATA
# --------------------------------------------------
__version__ = "7.0.0"
__package_role__ = "PLANETARY_URBAN_DATA_EXCHANGE_LAYER"
__classification__ = "ENTERPRISE_CRITICAL"

# --------------------------------------------------
# Public API Exports
# --------------------------------------------------
from .digital_earth_engine import DigitalEarthEngine
