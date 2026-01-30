# ======================================================
# ENERGY FORECAST ENGINE
# VERSION: v2.4.0-SUPREME-STABLE
# ======================================================

def forecast_energy_savings(district_data: dict) -> float:
    """
    Core energy savings forecast logic
    """
    baseline = district_data.get("baseline_consumption", 0)
    efficiency_gain = district_data.get("efficiency_gain", 0.15)
    return baseline * efficiency_gain


# ======================================================
# BACKWARD COMPATIBILITY – FUNCTION
# ======================================================
def predict_energy_savings(district_data: dict) -> float:
    return forecast_energy_savings(district_data)


# ======================================================
# BACKWARD COMPATIBILITY – CLASS (CRITICAL)
# ======================================================
class EnergyForecaster:
    """
    Legacy-compatible class wrapper used by Core Engine
    """

    def __init__(self, efficiency_gain: float = 0.15):
        self.efficiency_gain = efficiency_gain

    def predict(self, district_data: dict) -> float:
        district_data = dict(district_data)
        district_data.setdefault("efficiency_gain", self.efficiency_gain)
        return forecast_energy_savings(district_data)
