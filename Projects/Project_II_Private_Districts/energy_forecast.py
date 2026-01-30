# ======================================================
# ENERGY FORECAST ENGINE
# VERSION: v2.3.0-SUPREME-COMPAT
# ======================================================

def forecast_energy_savings(district_data: dict) -> float:
    """
    Core energy savings forecast logic (NEW PRIMARY API)
    """
    baseline = district_data.get("baseline_consumption", 0)
    efficiency_gain = district_data.get("efficiency_gain", 0.15)

    return baseline * efficiency_gain


# ======================================================
# BACKWARD COMPATIBILITY ALIAS (DO NOT REMOVE)
# ======================================================
def predict_energy_savings(district_data: dict) -> float:
    """
    Legacy alias required by CI + older engines
    """
    return forecast_energy_savings(district_data)
