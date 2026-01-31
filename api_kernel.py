# =========================================================
# PATH: /api_kernel.py
# DESCRIPTION: FBC Unified Global API Kernel
# VERSION: v3.0.0 — REAL DATA LOCKED • AUDIT READY
# ROLE: Central Execution Gateway for all FBC Systems
# =========================================================

from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
import sys
import os

# =========================================================
# PATH REGISTRATION (SAFE & DETERMINISTIC)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_PATH = os.path.join(BASE_DIR, "Projects")

if PROJECTS_PATH not in sys.path:
    sys.path.insert(0, PROJECTS_PATH)

# =========================================================
# IMPORT CORE ENGINES (REAL DATA ONLY)
# =========================================================
from Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Project_III_Security_Ledger.secure_vault import FBCSecureVault

# =========================================================
# IMPORT DATA CORE
# =========================================================
from data_core import fetch_results_as_dict

vault = FBCSecureVault()

# =========================================================
# FASTAPI APPLICATION
# =========================================================
app = FastAPI(
    title="FBC Global Intelligence Kernel",
    version="3.0.0-REAL-DATA",
    description=(
        "Unified, audit-grade API gateway for FBC Urban Intelligence. "
        "All endpoints operate exclusively on real data sources "
        "and verified AI engines."
    ),
)

# =========================================================
# GOVERNMENT INTELLIGENCE ROUTES
# =========================================================
@app.get("/government/risk/{city}/{density}", response_model=Dict[str, Any])
def get_city_risk(city: str, density: int):
    if density < 0:
        raise HTTPException(status_code=400, detail="Traffic density must be non-negative")

    engine = TrafficRiskEngine(city)
    return engine.analyze_real_time_risk(density)


@app.get("/government/revenue/{city}/{annual_revenue}", response_model=Dict[str, Any])
def get_revenue_projection(city: str, annual_revenue: float):
    if annual_revenue <= 0:
        raise HTTPException(status_code=400, detail="Annual revenue must be positive")

    optimizer = RevenueOptimizer(city)
    return optimizer.project_incremental_gain(annual_revenue)

# =========================================================
# PRIVATE DISTRICT INTELLIGENCE
# =========================================================
@app.get("/private/energy/{bill}", response_model=Dict[str, Any])
def get_energy_savings(bill: float):
    if bill <= 0:
        raise HTTPException(status_code=400, detail="Energy bill must be positive")

    return predict_energy_savings(bill)

# =========================================================
# SECURITY LEDGER
# =========================================================
@app.get("/ledger/proof/{project}/{entity}/{value}", response_model=Dict[str, Any])
def generate_ledger_proof(project: str, entity: str, value: float):
    if value < 0:
        raise HTTPException(status_code=400, detail="Ledger value must be non-negative")

    return vault.generate_proof(project, entity, value)

# =========================================================
# DATA CORE — SIMULATION HISTORY
# =========================================================
@app.get("/data/simulations")
def get_all_simulations() -> Dict[str, Any]:
    simulations = fetch_results_as_dict()
    return {
        "count": len(simulations),
        "simulations": simulations,
        "data_mode": "REAL",
    }

# =========================================================
# SYSTEM STATUS & HEALTH
# =========================================================
@app.get("/")
def root() -> Dict[str, str]:
    return {
        "system": "FBC Global Intelligence Kernel",
        "status": "ONLINE",
        "data_mode": "REAL",
        "version": "v3.0.0",
    }
