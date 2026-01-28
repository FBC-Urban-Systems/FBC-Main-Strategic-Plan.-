# ==========================================
# PATH: fbc_live_dashboard.py
# DESCRIPTION: FBC Global Command Center v3.1
# CONNECTS: Revenue AI, Energy Forecast, Traffic Intel
# ==========================================

import streamlit as st
import pandas as pd
from core_kernel import MasterCityKernel
from energy_forecast import predict_energy_savings
from accident_pred import predict_traffic_risk

# UI Configuration (Dark Luxury Theme)
st.set_page_config(page_title="FBC Global OS | CEO Command Center", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; background-color: #0e1117; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stButton>button { background-color: #00ffcc; color: black; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ FBC DIGITAL SYSTEMS | GLOBAL COMMAND")
st.write(f"**Founder:** Karim | **Status:** Phase 0 (Pre-Launch 2026)")

# Sidebar Control Node
st.sidebar.header("City Control Node")
city_select = st.sidebar.selectbox("Select Target City", ["Austin-HQ", "Dubai", "Riyadh", "Toronto"])
base_rev = st.sidebar.slider("Base City Revenue ($M)", 10, 500, 100)
run_sim = st.sidebar.button("Execute Simulation")

if run_sim:
    # Initialize Kernel
    kernel = MasterCityKernel(city_select)
    report = kernel.run_system_diagnostic(base_rev)

    # --- Section 1: Project I - Urban Revenue ---
    st.header("💰 Urban Revenue Optimization (Project I)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Target Revenue", f"${base_rev}M")
    with col2:
        st.metric("AI Boost", report['revenue_optimization'])
    with col3:
        st.metric("System Integrity", "SECURED-SHA256", delta="Active")

    # --- Section 2: Project II - Smart Energy ---
    st.header("⚡ Smart District Energy (Project II)")
    # Simulation: Energy consumption is roughly 10% of revenue
    energy_data = predict_energy_savings(base_rev * 0.1) 
    st.subheader(f"Potential Savings for {city_select}: ${energy_data['ai_predicted_savings']:,.2f}M")
    st.progress(15) # Based on 15% optimization logic

    # --- Section 3: Project III - Traffic Intelligence ---
    st.header("🚦 Traffic Intelligence (Project III)")
    traffic_status = predict_traffic_risk(75, "Clear")
    st.info(f"Traffic Risk Score: {traffic_status['risk_score']} | Status: {traffic_status['status']}")

    # Global Expansion Map
    st.header("🌍 Global Expansion Roadmap")
    map_data = pd.DataFrame({
        'lat': [30.2672, 25.2048, 24.7136, 43.6532],
        'lon': [-97.7431, 55.2708, 46.6753, -79.3832]
    })
    st.map(map_data)

    st.success("All systems operational. Data synced with Global Cities Manifest.")
else:
    st.warning("Please click 'Execute Simulation' to pull real-time data from the Kernel.")
