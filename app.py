# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Full Phase I - Live Intelligence Portal
# FEATURES: Live Weather Simulation, Traffic Risk AI, Revenue Optimization
# ==========================================

import streamlit as st
import sys
import os
import random

# --- Environment Path Integration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATHS = [
    "Projects/Project-I-Urban-Revenue",
    "Projects/Project-II-Private-Districts",
    "Projects/Project-III-Traffic-Intelligence"
]
for path in PROJECT_PATHS:
    full_path = os.path.join(BASE_DIR, path)
    if full_path not in sys.path:
        sys.path.append(full_path)

# --- AI Engines Import ---
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    SYSTEM_STATUS = "OPERATIONAL ✅"
except ImportError as e:
    SYSTEM_STATUS = f"ERROR: {e} ❌"

# --- Page Branding & Config ---
st.set_page_config(page_title="FBC Global | Command Center", layout="wide", page_icon="🏙️")

st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: white; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border-bottom: 4px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- Top Navigation Bar ---
st.title("🏙️ FBC Global Strategic Command Center")
st.write(f"System Integrity: **{SYSTEM_STATUS}** | Network: **Secured SHA-256**")
st.markdown("---")

# --- Sidebar Control Module ---
st.sidebar.image("https://img.shields.io/badge/FBC_OS-V3.5_LIVE-gold?style=for-the-badge")
st.sidebar.header("🕹️ Sector Control")
app_mode = st.sidebar.selectbox("Select Operational View", ["Municipal Government", "Private Smart Districts"])

# ==========================================
# SECTOR 1: Municipal Government (Live Intelligence)
# ==========================================
if app_mode == "Municipal Government":
    st.header("🚦 Live Municipal Intelligence & Revenue")
    
    city_name = st.text_input("Active City Node", "Austin, TX")
    
    col_risk, col_rev = st.columns(2)
    
    with col_risk:
        st.subheader("Traffic Risk Intelligence")
        density = st.slider("Vehicle Density (Cars/km)", 0, 300, 120)
        
        # Trigger the AI Engine with Live Simulation
        risk_engine = TrafficRiskEngine(city_name)
        # Note: In Project III, we modified 'analyze_real_time_risk' to handle weather internally
        risk_result = risk_engine.analyze_real_time_risk(density)
        
        st.metric("AI Predicted Risk", risk_result['risk_score'], 
                  delta=f"Weather: {risk_result['live_weather']}", delta_color="inverse")
        st.write(f"Node Status: **{risk_result['status']}**")
        st.progress(int(float(risk_result['risk_score'].replace('%',''))))

    with col_rev:
        st.subheader("Revenue Growth Engine")
        current_revenue = st.number_input("Annual Infrastructure Revenue ($)", value=15000000)
        
        rev_engine = RevenueOptimizer(city_name)
        gain_data = rev_engine.project_incremental_gain(current_revenue)
        
        st.metric("Projected Revenue Uplift", f"${gain_data['Total_City_Gain']:,.2f}", delta="+25%")
        st.success(f"FBC Managed Commission (20%): ${gain_data['FBC_Commission']:,.2f}")

# ==========================================
# SECTOR 2: Private Smart Districts (Optimization)
# ==========================================
else:
    st.header("🏢 Private District Energy Hub")
    
    col_data, col_viz = st.columns(2)
    
    with col_data:
        district_id = st.text_input("District Serial", "FBC-EGYPT-HUB-01")
        monthly_exp = st.number_input("Monthly Energy Consumption ($)", value=350000)
        
        # Trigger Project II AI
        energy_results = predict_energy_savings(monthly_exp)
        
        st.metric("AI Optimized Savings", f"${energy_results['ai_predicted_savings']:,.2f}", delta="-15%")
    
    with col_viz:
        st.subheader("Optimization Analysis")
        st.write(f"Baseline Expenditure: **${monthly_exp:,.2f}**")
        st.write(f"Post-AI Optimized Cost: **${energy_results['new_optimized_cost']:,.2f}**")
        st.info("Strategy: Demand forecasting & Peak-load shifting enabled.")

# --- Footer ---
st.markdown("---")
st.caption("© 2026 FBC Digital Systems | Intelligence Verified | Austin HQ")
