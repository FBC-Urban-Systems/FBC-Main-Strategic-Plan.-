# ==========================================
# PATH: data_core/__init__.py
# DESCRIPTION: data_core Public API Surface (Enterprise LTS)
# VERSION: v5.0.0-ENTERPRISE-LTS
# ==========================================

"""
data_core
---------

Enterprise-stable public API surface for data ingestion,
storage, and retrieval across FBC systems.

This module is intentionally minimal and side-effect free.
Only symbols explicitly exported here are considered public
and backward-compatible under LTS guarantees.
"""

# --------------------------------------------------
# PUBLIC API IMPORTS (STABLE — DO NOT BREAK)
# --------------------------------------------------
from data_core.core import (
    fetch_all_results,
    store_simulation_result,
)

from data_core.results import (
    fetch_results_as_dict,
)

# --------------------------------------------------
# EXPLICIT PUBLIC EXPORTS
# --------------------------------------------------
__all__ = [
    "fetch_all_results",
    "store_simulation_result",
    "fetch_results_as_dict",
]

# --------------------------------------------------
# ENTERPRISE METADATA
# --------------------------------------------------
__version__ = "5.0.0-ENTERPRISE-LTS"
__package_name__ = "data_core"
__organization__ = "FBC Digital Systems"
__stability__ = "LTS"
