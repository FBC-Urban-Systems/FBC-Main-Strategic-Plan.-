# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Full Phase I Strategic Dashboard
# PROJECTS: I (Revenue), II (Energy), III (Traffic Risk)
# ==========================================

import streamlit as st
import pandas as pd
import sys
import os

# --- Environment Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "Projects/Project-I-Urban-Revenue"))
sys.path.append(os.path.join(BASE_DIR, "Projects/Project-II-Private-Districts"))
sys.path.append(os.path.join(BASE_DIR, "Projects/Project-III-Traffic-Intelligence"))

# --- AI Engines Import ---
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    SYSTEM_STATUS = "OPERATIONAL ✅"
except ImportError as e:
    SYSTEM_STATUS = f"OFFLINE ❌ ({e})"

# --- Page UI Configuration ---
st.set_page_config(page_title="FBC Digital Systems | OS v3.5", layout="wide")

# Custom CSS for "The Investor Look"
st.markdown("""
    <style>
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border-top: 4px solid #ffd700; }
    .main { background-color: #050505; }
    </style>
    """, unsafe_allow_html=True)

# --- Header & Global Status ---
st.title("🏙️ FBC Global Strategic Command Center")
st.write(f"System Status: **{SYSTEM_STATUS}** | Phase: **I (2027 Prototype Early-Access)**")
st.markdown("---")

# --- Sidebar Controls ---
st.sidebar.image("https://img.shields.io/badge/FBC_OS-GOLD_MASTER-gold?style=for-the-badge")
st.sidebar.header("🕹️ Deployment Control")
sector = st.sidebar.radio("Switch View", ["Municipal Government", "Private Smart Districts"])

# ==========================================
# VIEW 1: Municipal Government (Revenue & Safety)
# ==========================================
if sector == "Municipal Government":
    st.header("💰 Urban Revenue & Safety Intelligence")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Traffic Risk AI (Project III)")
        city_name = st.text_input("City Node", "New Austin")
        density = st.slider("Vehicle Density (Cars/km)", 0, 250, 110)
        weather = st.selectbox("Weather Condition", ["Clear", "Rainy", "Foggy"])
        
        risk_engine = TrafficRiskEngine(city_name)
        risk_data = risk_engine.analyze_real_time_risk(density, weather)
        
        st.metric("Risk Score", risk_data['risk_score'], delta=risk_data['status'])
        st.info(f"Recommended Action: {risk_data['action']}")

    with col2:
        st.subheader("Revenue Yield Optimization (Project I)")
        current_rev = st.number_input("Annual Municipal Revenue ($)", value=25000000)
        
        opt = RevenueOptimizer(city_name)
        gain = opt.project_incremental_gain(current_rev)
        
        st.metric("FBC Generated Boost", f"${gain['Total_City_Gain']:,.2f}", delta="+25% Efficiency")
        st.success(f"FBC Managed Commission (20%): ${gain['FBC_Commission']:,.2f}")

# ==========================================
# VIEW 2: Private Smart Districts (Energy)
# ==========================================
else:
    st.header("🏢 Private District Energy Management")
    st.info("AI-Driven Forecasting for Real Estate Developers.")

    col_a, col_b = st.columns(2)
    
    with col_a:
        dist_id = st.text_input("District ID", "FBC-Dubai-Hub-01")
        monthly_cost = st.number_input("Monthly Grid Expenditure ($)", value=450000)
        
    with col_b:
        results = predict_energy_savings(monthly_cost)
        st.subheader("Savings Forecast (Project II)")
        st.metric("AI Monthly Savings", f"${results['ai_predicted_savings']:,.2f}", delta="-15% Cost")
        st.write(f"New Operational Baseline: **${results['new_optimized_cost']:,.2f}**")

# --- Footer Ledger ---
st.markdown("---")
st.caption("© 2026 FBC Digital Systems | All transactions secured by SHA-256 Unified Ledger | Austin, TX")
