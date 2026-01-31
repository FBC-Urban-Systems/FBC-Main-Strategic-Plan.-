# ==========================================
# PATH: data_core/results.py
# DESCRIPTION: Enterprise Results Access Layer
# VERSION: v5.0.0-ENTERPRISE-LTS
# ==========================================

from typing import Dict, Any
from datetime import datetime, timezone

from data_core.core import fetch_all_results

# --------------------------------------------------
# ENTERPRISE CONSTANTS
# --------------------------------------------------
ENGINE_VERSION = "5.0.0-ENTERPRISE-LTS"
MODULE_NAME = "data_core.results"


def fetch_results_as_dict() -> Dict[str, Any]:
    """
    Enterprise-stable results access interface.

    Guarantees:
    - Backward compatibility
    - Immutable snapshot semantics
    - Audit-ready metadata
    - CI-safe deterministic output
    """

    results = fetch_all_results()

    return {
        "metadata": {
            "module": MODULE_NAME,
            "engine_version": ENGINE_VERSION,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "results": results,
        "count": len(results),
    }
