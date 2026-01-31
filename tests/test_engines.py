# =========================================================
# PATH: /tests/test_engines.py
# DESCRIPTION: Core Engine Contract & Stability Tests
# VERSION: v4.0.0 — CONTRACT SAFE • CI READY
# ROLE: System Trust & Regression Validation Layer
# =========================================================

import pytest

# ---------------------------------------------------------
# CORE ENGINE IMPORTS
# ---------------------------------------------------------
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault


# =========================================================
# REVENUE ENGINE CONTRACT TEST
# =========================================================
def test_revenue_engine_contract():
    engine = RevenueOptimizer("TestCity")

    result = engine.project_incremental_gain(1_000_000)

    assert isinstance(result, dict)
    assert "Total_City_Gain" in result
    assert isinstance(result["Total_City_Gain"], (int, float))
    assert result["Total_City_Gain"] >= 0


# =========================================================
# ENERGY ENGINE CONTRACT TEST
# =========================================================
def test_energy_engine_contract():
    result = predict_energy_savings(100_000)

    assert isinstance(result, dict)
    assert "ai_predicted_savings" in result
    assert isinstance(result["ai_predicted_savings"], (int, float))
    assert result["ai_predicted_savings"] >= 0


# =========================================================
# TRAFFIC ENGINE CONTRACT TEST
# =========================================================
def test_traffic_engine_contract():
    engine = TrafficRiskEngine("TestCity")

    result = engine.analyze_real_time_risk(120)

    assert isinstance(result, dict)
    assert "risk_score" in result
    assert isinstance(result["risk_score"], (int, float))


# =========================================================
# SECURITY LEDGER CONTRACT TEST
# =========================================================
def test_secure_vault_contract():
    vault = FBCSecureVault()

    proof = vault.generate_proof("TEST", "ENTITY", 12345)

    assert isinstance(proof, dict)
    assert "audit_hash" in proof
    assert isinstance(proof["audit_hash"], str)

    assert "status" in proof
    assert proof["status"] in {
        "SIGNED",
        "VERIFIED",
        "SECURED"
    }


# =========================================================
# SYSTEM-WIDE SMOKE TEST
# =========================================================
def test_system_smoke():
    """
    Validates that all core engines initialize and execute
    without raising runtime exceptions.
    """

    RevenueOptimizer("SmokeCity")
    TrafficRiskEngine("SmokeCity")
    FBCSecureVault()

    energy = predict_energy_savings(10_000)
    assert energy is not None
