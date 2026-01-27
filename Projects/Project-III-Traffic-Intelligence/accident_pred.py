# FBC Digital Systems - Project III: Traffic Intelligence
# Risk Analysis & Accident Prediction Script

def analyze_traffic_risk(vehicle_density, weather_index):
    """
    Calculates traffic risk score for insurance pricing.
    Input: Density (vehicles/km), Weather Index (0-1).
    """
    risk_score = (vehicle_density * 0.7) + (weather_index * 30)
    
    # Tier labeling for insurance APIs
    if risk_score > 75:
        tier = "High Risk - Premium Pricing"
    else:
        tier = "Standard Risk"
        
    return {
        "risk_score": round(risk_score, 2),
        "insurance_tier": tier
    }

# Example: High density (100) and bad weather (0.8)
report = analyze_traffic_risk(100, 0.8)
print(f"FBC Intelligence Report: Traffic Risk is {report['risk_score']}. Suggested Tier: {report['insurance_tier']}")
