# ==========================================
# PATH: /api_kernel.py
# DESCRIPTION: FBC Unified Global API Kernel
# VERSION: v1.0.0-OMEGA
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
from Project-I-Urban-Revenue.revenue_optimizer import RevenueOptimizer
from Project-II-Private-Districts.energy_forecast import predict_energy_savings
from Project-III-Traffic-Intelligence.accident_pred import TrafficRiskEngine
from Project-III-Security-Ledger.secure_vault import FBCSecureVault

vault = FBCSecureVault()

# ==========================================
# FASTAPI CORE
# ==========================================
app = FastAPI(
    title="FBC Global Intelligence Kernel",
    version="1.0.0",
    description="Unified API Gateway for Planetary-Scale Urban Intelligence"
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
# SYSTEM STATUS
# ==========================================
@app.get("/")
def root():
    return {
        "system": "FBC Global Intelligence Kernel",
        "status": "ONLINE",
        "version": "v1.0.0-OMEGA"
}
