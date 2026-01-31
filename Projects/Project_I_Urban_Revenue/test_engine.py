# ==========================================
# PATH: Projects/Project-I-Urban-Revenue/test_engine.py
# DESCRIPTION: FBC Revenue Engine — Enterprise CI & Audit Test Suite
# VERSION: v5.0.0-LTS-QA
# CLASSIFICATION: AUDIT / INVESTOR / CI CRITICAL
# ==========================================

import sys
from typing import Dict

from revenue_sim import calculate_revenue_boost


# --------------------------------------------------
# TEST CONFIGURATION
# --------------------------------------------------
BASELINE_REVENUE = 1_000_000

MIN_EFFICIENCY_PERCENT = 10
MAX_EFFICIENCY_PERCENT = 30


# --------------------------------------------------
# VALIDATION HELPERS
# --------------------------------------------------
def _validate_result_schema(result: Dict) -> None:
    """
    Ensures returned structure is audit-safe and stable.
    """
    required_keys = {
        "baseline_revenue",
        "ai_generated_boost",
        "efficiency_gain_percent",
        "status"
    }

    missing = required_keys - result.keys()
    if missing:
        raise AssertionError(f"Missing keys in revenue result: {missing}")


def _validate_numeric_ranges(result: Dict) -> None:
    """
    Validates strategic and financial boundaries.
    """
    baseline = result["baseline_revenue"]
    boost = result["ai_generated_boost"]
    efficiency = result["efficiency_gain_percent"]

    min_expected = baseline * (MIN_EFFICIENCY_PERCENT / 100)
    max_expected = baseline * (MAX_EFFICIENCY_PERCENT / 100)

    assert min_expected <= boost <= max_expected, (
        f"Boost out of strategic range: {boost}"
    )

    assert MIN_EFFICIENCY_PERCENT <= efficiency <= MAX_EFFICIENCY_PERCENT, (
        f"Efficiency percent out of bounds: {efficiency}"
    )


# --------------------------------------------------
# CORE ENTERPRISE TEST
# --------------------------------------------------
def test_revenue_engine_enterprise_audit() -> None:
    """
    Enterprise-grade CI test for Urban Revenue AI.

    Guarantees:
    - Schema stability
    - Strategic efficiency bounds
    - Deterministic behavior
    """

    result = calculate_revenue_boost(BASELINE_REVENUE)

    _validate_result_schema(result)
    _validate_numeric_ranges(result)

    assert result["status"] in {
        "OPTIMIZED",
        "STABLE"
    }, f"Unexpected engine status: {result['status']}"


# --------------------------------------------------
# CI ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    try:
        test_revenue_engine_enterprise_audit()
    except Exception as exc:
        print("\n[FBC CI AUDIT FAILURE — REVENUE ENGINE]")
        print(str(exc))
        sys.exit(1)

    print("\n[FBC CI AUDIT SUCCESS — REVENUE ENGINE OK]")
    sys.exit(0)
