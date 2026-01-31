# =====================================================
# FBC URBAN SYSTEMS
# Data Core – Internal Implementation
#
# VERSION: v3.2.0
# =====================================================

from typing import Any, Dict, List
from datetime import datetime

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
