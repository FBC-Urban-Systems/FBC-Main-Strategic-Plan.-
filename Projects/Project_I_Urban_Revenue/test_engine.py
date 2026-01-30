# ==========================================
# PATH: Projects/Project-I-Urban-Revenue/test_engine.py
# DESCRIPTION: FBC Automated QA & CI Audit Test
# VERSION: v4.0-QA-CI-GRADE
# ==========================================

import sys
from revenue_sim import calculate_revenue_boost

def test_revenue_logic():
    print("\n--- FBC SYSTEM AUDIT: REVENUE ENGINE TEST ---")

    test_val = 1_000_000
    result = calculate_revenue_boost(test_val)

    boost = result["ai_generated_boost"]
    efficiency = result["efficiency_gain_percent"]

    # Expected strategic range: 10% → 30%
    min_expected = test_val * 0.10
    max_expected = test_val * 0.30

    if min_expected <= boost <= max_expected:
        print("✅ Audit Passed: Revenue Boost within Strategic Range.")
        print(f"   Efficiency Gain: {efficiency}%")
        print(f"   Boost Value: ${boost:,.2f}")
        return True
    else:
        print("❌ Audit Failed: Revenue Boost Out of Strategic Range.")
        print(f"   Boost Value: ${boost:,.2f}")
        return False

# --------------------------------------------------
# CI ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    success = test_revenue_logic()
    if not success:
        sys.exit(1)   # Forces GitHub Actions to fail
    else:
        sys.exit(0)
