# ==========================================
# PATH: /data_core.py
# DESCRIPTION: Core Data Abstraction Layer
# VERSION: v1.0.0 — CONTRACT SAFE • FUTURE READY
# ROLE: Central Data Orchestration Interface
# ==========================================

from typing import Any, Dict, List
from datetime import datetime

# In-memory fallback store (can be replaced by DB / Data Lake)
_DATA_STORE: List[Dict[str, Any]] = []


def store_simulation_result(result: Dict[str, Any]) -> None:
    """
    Stores simulation or engine output in the core data layer.

    Parameters
    ----------
    result : dict
        Engine result payload
    """

    record = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "payload": result
    }

    _DATA_STORE.append(record)


def fetch_all_results() -> List[Dict[str, Any]]:
    """
    Fetches all stored simulation results.

    Returns
    -------
    list
        Stored engine outputs
    """

    return list(_DATA_STORE)
