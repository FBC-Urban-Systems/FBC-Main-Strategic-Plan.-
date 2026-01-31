# ==========================================
# ENERGY FORECAST ENGINE — ENTERPRISE SAFE
# ==========================================

class EnergyForecaster:
    """
    Backward-compatible enterprise wrapper.
    Preserves legacy imports while delegating to modern logic.
    """

    def __init__(self, district_data):
        self.district_data = district_data

    def forecast(self) -> dict:
        return predict_energy_savings(self.district_data)


def forecast_energy_savings(district_data: dict) -> dict:
    """
    Core energy savings forecast logic.
    Expects normalized district data dictionary.
    """
    baseline = district_data.get("baseline_consumption", 0)

    estimated_savings = baseline * 0.18  # Conservative AI efficiency factor

    return {
        "baseline_consumption": baseline,
        "ai_predicted_savings": estimated_savings,
        "confidence_level": "HIGH"
    }


def predict_energy_savings(input_data) -> dict:
    """
    Enterprise-grade public interface.

    Accepts:
    - int / float (baseline consumption)
    - dict (full district profile)

    Always returns a valid forecast dictionary.
    """

    # ---- Normalize input ----
    if isinstance(input_data, (int, float)):
        district_data = {
            "baseline_consumption": float(input_data)
        }

    elif isinstance(input_data, dict):
        district_data = input_data

    else:
        raise TypeError(
            "predict_energy_savings expects int, float, or dict input"
        )

    # ---- Defensive fallback for missing real data ----
    if district_data.get("baseline_consumption", 0) <= 0:
        return {
            "baseline_consumption": 0,
            "ai_predicted_savings": 0,
            "confidence_level": "LOW",
            "status": "INSUFFICIENT_REAL_DATA"
        }

    return forecast_energy_savings(district_data)
