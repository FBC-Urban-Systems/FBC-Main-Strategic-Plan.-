# =========================================================
# PATH: tests/test_engines.py
# DESCRIPTION: Core Engine Contract, Stability & Trust Tests
# VERSION: v5.0.0-ENTERPRISE-LTS
# ROLE: System Integrity, Regression & Interface Validation
# =========================================================

from typing import Dict, Any
import pytest

# ---------------------------------------------------------
# CORE ENGINE IMPORTS (CONTRACT LEVEL — DO NOT MOCK)
# ---------------------------------------------------------
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Projects.Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Projects.Project_III_Security_Ledger.secure_vault import FBCSecureVault


# =========================================================
# FIXTURES (DETERMINISTIC & SIDE-EFFECT FREE)
# =========================================================
@pytest.fixture(scope="module")
def test_city() -> str:
    return "TestCity"


# =========================================================
# REVENUE ENGINE CONTRACT TEST
# =========================================================
def test_revenue_engine_contract(test_city: str) -> None:
    engine = RevenueOptimizer(test_city)

    result: Dict[str, Any] = engine.project_incremental_gain(1_000_000)

    assert isinstance(result, dict)
    assert "Total_City_Gain" in result
    assert isinstance(result["Total_City_Gain"], (int, float))
    assert result["Total_City_Gain"] >= 0


# =========================================================
# ENERGY ENGINE CONTRACT TEST
# =========================================================
@pytest.mark.parametrize("baseline_usage", [10_000, 50_000, 100_000])
def test_energy_engine_contract(baseline_usage: int) -> None:
    result: Dict[str, Any] = predict_energy_savings(baseline_usage)

    assert isinstance(result, dict)
    assert "ai_predicted_savings" in result
    assert isinstance(result["ai_predicted_savings"], (int, float))
    assert result["ai_predicted_savings"] >= 0
    assert "confidence_level" in result
    assert isinstance(result["confidence_level"], str)


# =========================================================
# TRAFFIC ENGINE CONTRACT TEST
# =========================================================
def test_traffic_engine_contract(test_city: str) -> None:
    engine = TrafficRiskEngine(test_city)

    result: Dict[str, Any] = engine.analyze_real_time_risk(120)

    assert isinstance(result, dict)
    assert "risk_score" in result
    assert isinstance(result["risk_score"], (int, float))
    assert 0.0 <= result["risk_score"] <= 1.0
    assert "weather" in result


# =========================================================
# SECURITY LEDGER CONTRACT TEST (STRICT API COMPLIANCE)
# =========================================================
def test_secure_vault_contract() -> None:
    vault = FBCSecureVault()

    # IMPORTANT: positional args only (contract-safe)
    proof: Dict[str, Any] = vault.generate_proof("TEST", "ENTITY", 12345)

    assert isinstance(proof, dict)
    assert "audit_hash" in proof
    assert isinstance(proof["audit_hash"], str)

    # Forward-compatible contract validation
    assert "status" in proof
    assert isinstance(proof["status"], str)
    assert proof["status"].upper().endswith("RECORD")


# =========================================================
# SYSTEM-WIDE SMOKE TEST (NON-DESTRUCTIVE)
# =========================================================
def test_system_smoke(test_city: str) -> None:
    """
    Validates that all core engines initialize and execute
    without raising runtime exceptions.
    """

    RevenueOptimizer(test_city)
    TrafficRiskEngine(test_city)
    FBCSecureVault()

    energy = predict_energy_savings(10_000)
    assert energy is not None
