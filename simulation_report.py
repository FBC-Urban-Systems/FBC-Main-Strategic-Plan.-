# ==========================================
# PATH: /simulation_report.py
# DESCRIPTION: Simulation Report Exporter
# VERSION: v1.0.0
# ROLE: Exports Global Simulation Results to Files
# ==========================================

import json
import pandas as pd
from run_simulation import run_global_simulation
from datetime import datetime
import os

REPORT_DIR = "simulation_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def export_reports():
    results = run_global_simulation()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Export JSON
    json_path = os.path.join(REPORT_DIR, f"simulation_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)

    # Export CSV
    df = pd.DataFrame(results)
    csv_path = os.path.join(REPORT_DIR, f"simulation_{timestamp}.csv")
    df.to_csv(csv_path, index=False)

    print(f"\nReports generated:")
    print(f"JSON → {json_path}")
    print(f"CSV  → {csv_path}")

if __name__ == "__main__":
    export_reports()
