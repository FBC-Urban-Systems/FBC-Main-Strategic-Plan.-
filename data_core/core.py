from typing import Dict, Any, List
from datetime import datetime

_DATA_STORE: List[Dict[str, Any]] = []

def store_simulation_result(engine: str, payload: Dict[str, Any]) -> Dict[str, str]:
    _DATA_STORE.append({
        "engine": engine,
        "payload": payload,
        "timestamp_utc": datetime.utcnow().isoformat()
    })
    return {"status": "STORED"}

def fetch_all_results() -> List[Dict[str, Any]]:
    return _DATA_STORE
