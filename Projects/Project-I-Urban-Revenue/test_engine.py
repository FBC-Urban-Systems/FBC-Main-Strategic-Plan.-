# FBC Digital Systems - Automated Quality Assurance
# Testing the Urban AI Revenue Engine

from revenue_sim import calculate_revenue_boost

def test_revenue_logic():
    print("Starting FBC System Audit...")
    
    # Test case: $1M input
    test_val = 1000000
    result = calculate_revenue_boost(test_val)
    
    # Asserting that boost is exactly 25% as defined in our logic
    if result['ai_generated_boost'] == 250000:
        print("✅ Audit Passed: Revenue Calculation is Precise.")
    else:
        print("❌ Audit Failed: Calculation Error Detected.")

if __name__ == "__main__":
    test_revenue_logic()
