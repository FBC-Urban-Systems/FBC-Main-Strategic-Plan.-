# =====================================================
# FBC URBAN SYSTEMS
# Data Core – Internal Engine
#
# VERSION: v3.2.1
# =====================================================

from typing import Dict, Any, List
from datetime import datetime

__all__ = [
    "store_simulation_result",
    "fetch_all_results",
]

_DATA_STORE: List[Dict[str, Any]] = []


def store_simulation_result(engine: str, payload: Dict[str, Any]) -> Dict[str, Any]:
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
    return list(_DATA_STORE)
