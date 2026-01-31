# ==========================================
# PATH: data_core/__init__.py
# DESCRIPTION: data_core public API surface
# VERSION: data-core v3.3.0
# ==========================================

from data_core.core import (
    fetch_all_results,
    store_simulation_result,
)

from data_core.results import fetch_results_as_dict

__all__ = [
    "fetch_all_results",
    "store_simulation_result",
    "fetch_results_as_dict",
]

__version__ = "3.3.0"
