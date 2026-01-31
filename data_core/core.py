# ==========================================
# PATH: data_core/core.py
# DESCRIPTION: Enterprise Data Core (In-Memory, Audit-Ready)
# VERSION: v5.0.0-ENTERPRISE-LTS
# ==========================================

from typing import Dict, Any, List
from datetime import datetime, timezone
from threading import Lock
import uuid
import copy

# --------------------------------------------------
# INTERNAL STATE (PRIVATE — DO NOT ACCESS DIRECTLY)
# --------------------------------------------------
_DATA_STORE: List[Dict[str, Any]] = []
_DATA_LOCK = Lock()

# Soft limit to prevent runaway memory usage (CI-safe)
_MAX_RECORDS = 100_000


# --------------------------------------------------
# PUBLIC API (STABLE — DO NOT BREAK)
# --------------------------------------------------
def store_simulation_result(engine: str, payload: Dict[str, Any]) -> Dict[str, str]:
    """
    Stores a simulation result with enterprise-grade metadata.

    Parameters
    ----------
    engine : str
        Source engine identifier
    payload : dict
        Simulation result payload (validated)

    Returns
    -------
    dict
        Storage operation status
    """

    if not isinstance(engine, str) or not engine:
        raise ValueError("engine must be a non-empty string")

    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")

    record = {
        "record_id": str(uuid.uuid4()),
        "engine": engine,
        "payload": copy.deepcopy(payload),
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }

    with _DATA_LOCK:
        if len(_DATA_STORE) >= _MAX_RECORDS:
            _DATA_STORE.pop(0)  # FIFO eviction (deterministic)

        _DATA_STORE.append(record)

    return {"status": "STORED"}


def fetch_all_results() -> List[Dict[str, Any]]:
    """
    Returns an immutable snapshot of all stored simulation results.
    """

    with _DATA_LOCK:
        return copy.deepcopy(_DATA_STORE)
