# ==========================================
# PATH: /api_kernel.py
# DESCRIPTION: FBC Unified Global API Kernel
# VERSION: v2.0.0-DATA-CORE
# ROLE: Central Execution Gateway for all FBC Systems
# ==========================================

from fastapi import FastAPI
import sys, os

# ==========================================
# PATH REGISTRATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_PATH = os.path.join(BASE_DIR, "Projects")
sys.path.append(PROJECTS_PATH)

# ==========================================
# IMPORT CORE ENGINES
# ==========================================
from Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Project_III_Security_Ledger.secure_vault import FBCSecureVault

# ==========================================
# IMPORT DATA CORE
# ==========================================
from data_core import fetch_all_results

vault = FBCSecureVault()

# ==========================================
# FASTAPI CORE
# ==========================================
app = FastAPI(
    title="FBC Global Intelligence Kernel",
    version="2.0.0-DATA-CORE",
    description="Unified API Gateway for FBC Planetary Urban Intelligence"
)

# ==========================================
# GOVERNMENT ROUTES
# ==========================================
@app.get("/government/risk/{city}/{density}")
def get_city_risk(city: str, density: int):
    engine = TrafficRiskEngine(city)
    return engine.analyze_real_time_risk(density)

@app.get("/government/revenue/{city}/{annual_revenue}")
def get_revenue_projection(city: str, annual_revenue: float):
    optimizer = RevenueOptimizer(city)
    return optimizer.project_incremental_gain(annual_revenue)

# ==========================================
# PRIVATE DISTRICT ROUTES
# ==========================================
@app.get("/private/energy/{bill}")
def get_energy_savings(bill: float):
    return predict_energy_savings(bill)

# ==========================================
# SECURITY LEDGER ROUTES
# ==========================================
@app.get("/ledger/proof/{project}/{entity}/{value}")
def generate_ledger_proof(project: str, entity: str, value: float):
    return vault.generate_proof(project, entity, value)

# ==========================================
# DATA CORE ROUTE — SIMULATION HISTORY
# ==========================================
@app.get("/data/simulations")
def get_all_simulations():
    rows = fetch_all_results()
    results = []

    for r in rows:
        results.append({
            "id": r[0],
            "timestamp": r[1],
            "city": r[2],
            "revenue_gain": r[3],
            "energy_savings": r[4],
            "risk_score": r[5]
        })

    return {
        "count": len(results),
        "simulations": results
    }

# ==========================================
# SYSTEM STATUS
# ==========================================
@app.get("/")
def root():
    return {
        "system": "FBC Global Intelligence Kernel",
        "status": "ONLINE",
        "version": "v2.0.0-DATA-CORE"
    }
