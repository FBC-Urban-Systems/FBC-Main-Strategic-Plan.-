import random

def predict_traffic_risk(vehicle_density, weather_condition):
    """
    FBC Traffic Risk Predictor v1.0
    Analyzes real-time city data to prevent accidents.
    """
    # Simple AI Logic: Risk increases with density and bad weather
    risk_score = (vehicle_density * 0.7)
    
    if weather_condition.lower() in ["rainy", "foggy"]:
        risk_score += 30
    
    status = "HIGH RISK" if risk_score > 75 else "NORMAL"
    
    return {
        "risk_score": f"{round(risk_score, 2)}%",
        "status": status,
        "action": "Deploying Smart Traffic Units" if status == "HIGH RISK" else "Monitoring"
    }

if __name__ == "__main__":
    print("--- FBC TRAFFIC INTELLIGENCE ACTIVE ---")
    # Simulating 85% density during rainy weather
    analysis = predict_traffic_risk(85, "rainy")
    print(f"Risk Analysis: {analysis}")
