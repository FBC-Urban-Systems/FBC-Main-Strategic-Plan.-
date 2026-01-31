# ==========================================
# PATH: data_core/results.py
# DESCRIPTION: Unified results access layer
# VERSION: data-core v3.3.0
# ==========================================

from typing import Dict, Any
from .core import fetch_all_results


def fetch_results_as_dict() -> Dict[str, Any]:
    """
    Stable API Kernel interface.
    Returns all stored simulation results in a dictionary format.
    This function is guaranteed to remain backward compatible.
    """
    results = fetch_all_results()

    return {
        "results": results,
        "count": len(results),
    }
