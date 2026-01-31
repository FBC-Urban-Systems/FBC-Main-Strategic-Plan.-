# =====================================================
# FBC URBAN SYSTEMS
# Data Core Layer
#
# ROLE:
# - Unified data access contract for all engines
# - CI / API / Application safe abstraction
# - Storage-agnostic (DB, Lake, API, Future adapters)
#
# VERSION: v3.2.0 (STABLE • ENTERPRISE • FUTURE-READY)
# =====================================================

from __future__ import annotations
from typing import Any, Dict, List
from datetime import datetime

__version__ = "3.2.0"


# -----------------------------------------------------
# In-memory fallback storage (CI / local / safe mode)
# -----------------------------------------------------
_DATA_STORE: List[Dict[str, Any]] = []


def store_simulation_result(
    engine: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Stores a simulation or engine result.

    This is a contract-safe abstraction layer.
    Backend can later be swapped to:
    - PostgreSQL
    - Data Lake
    - Blockchain Ledger
    - External API
    """

    record = {
        "engine": engine,
        "payload": payload,
        "timestamp_utc": datetime.utcnow().isoformat(),
    }

    _DATA_STORE.append(record)

    return {
        "status": "STORED",
        "engine": engine,
    }


def fetch_all_results() -> List[Dict[str, Any]]:
    """
    Fetches all stored simulation results.

    CI-safe, read-only operation.
    """
    return list(_DATA_STORE)
