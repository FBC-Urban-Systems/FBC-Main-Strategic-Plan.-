# ==========================================
# PATH: /data_core/core.py
# DESCRIPTION: Core Data Abstraction Layer
# VERSION: v1.0.1 — PACKAGE SAFE • CI READY
# ==========================================

from typing import Any, Dict, List
from datetime import datetime

_DATA_STORE: List[Dict[str, Any]] = []


def store_simulation_result(result: Dict[str, Any]) -> None:
    record = {
        "timestamp_utc": datetime.utcnow().isoformat(),
        "payload": result
    }
    _DATA_STORE.append(record)


def fetch_all_results() -> List[Dict[str, Any]]:
    return list(_DATA_STORE)
