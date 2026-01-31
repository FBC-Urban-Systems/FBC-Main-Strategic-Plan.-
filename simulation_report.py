# =========================================================
# PATH: /simulation_report.py
# DESCRIPTION: Global Simulation Report Export Engine
# VERSION: v2.0.0 — REAL DATA SAFE • FUTURE PROOF
# ROLE: Deterministic, Auditable Export Layer for Simulation Outputs
# =========================================================

import json
import os
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from run_simulation import run_global_simulation


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
REPORT_DIR = os.getenv("SIMULATION_REPORT_DIR", "simulation_reports")
EXPORT_TIMEZONE = "UTC"

os.makedirs(REPORT_DIR, exist_ok=True)


# ---------------------------------------------------------
# CORE EXPORT ENGINE
# ---------------------------------------------------------
def export_reports() -> Dict[str, Any]:
    """
    Executes the global simulation and exports results
    in multiple deterministic formats (JSON, CSV).

    Returns:
        dict: Export metadata and file paths
    """

    results = run_global_simulation()

    if not isinstance(results, (list, dict)):
        raise ValueError("Simulation output must be a list or dict")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base_filename = f"simulation_{timestamp}"

    # -----------------------
    # JSON EXPORT
    # -----------------------
    json_path = os.path.join(REPORT_DIR, f"{base_filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    # -----------------------
    # CSV EXPORT
    # -----------------------
    try:
        df = pd.DataFrame(results)
        csv_path = os.path.join(REPORT_DIR, f"{base_filename}.csv")
        df.to_csv(csv_path, index=False)
    except Exception:
        csv_path = None  # CSV is optional depending on structure

    return {
        "status": "EXPORT_SUCCESS",
        "timestamp_utc": timestamp,
        "json_report": json_path,
        "csv_report": csv_path,
        "record_count": len(results) if hasattr(results, "__len__") else 1
    }


# ---------------------------------------------------------
# CLI ENTRYPOINT
# ---------------------------------------------------------
if __name__ == "__main__":
    metadata = export_reports()

    print("\n📊 FBC Simulation Reports Generated")
    print("----------------------------------")
    print(f"Status        : {metadata['status']}")
    print(f"Timestamp UTC : {metadata['timestamp_utc']}")
    print(f"JSON Report   : {metadata['json_report']}")

    if metadata["csv_report"]:
        print(f"CSV Report    : {metadata['csv_report']}")
    else:
        print("CSV Report    : Skipped (non-tabular data)")
