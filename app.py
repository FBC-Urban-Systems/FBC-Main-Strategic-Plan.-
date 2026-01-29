# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center
# VERSION: v5.0.0 DATA-CORE-INTEGRATED
# ==========================================

import streamlit as st
import sys, os, datetime
import pandas as pd

# ==========================================
# PATH INTEGRATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_PATH = os.path.join(BASE_DIR, "Projects")
sys.path.append(PROJECTS_PATH)

# ==========================================
# IMPORT ENGINES
# ==========================================
from Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine
from Project_III_Security_Ledger.secure_vault import FBCSecureVault

# ==========================================
# DATA CORE
# ==========================================
from data_core import fetch_all_results, store_simulation_result

vault = FBCSecureVault()

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(page_title="FBC Global Command Center", layout="wide")

st.title("🌍 FBC Global Command Center")
st.caption("Planetary Urban Intelligence Dashboard")

st.markdown("---")

# ==========================================
# SIDEBAR MODE SELECT
# ==========================================
mode = st.sidebar.radio(
    "Select Operation Mode",
    ["Run New Simulation", "Global Oversight Ledger"]
)

# ==========================================
# MODE 1 — RUN NEW SIMULATION
# ==========================================
if mode == "Run New Simulation":

    st.header("🚀 Run City AI Simulation")

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.text_input("City Name", "Cairo")

    with col2:
        base_revenue = st.number_input("Base Annual Revenue ($)", value=5_000_000)

    with col3:
        base_energy_bill = st.number_input("Base Monthly Energy Bill ($)", value=150_000)

    traffic_density = st.slider("Traffic Density Index", 50, 300, 150)

    if st.button("Run Simulation"):

        with st.spinner("Executing AI Engines..."):

            # Run Engines
            rev_engine = RevenueOptimizer(city)
            rev_result = rev_engine.project_incremental_gain(base_revenue)

            energy_result = predict_energy_savings(base_energy_bill)

            traffic_engine = TrafficRiskEngine(city)
            traffic_result = traffic_engine.analyze_real_time_risk(traffic_density)

            revenue_gain = rev_result["Total_City_Gain"]
            energy_savings = energy_result["ai_predicted_savings"]
            risk_score = traffic_result["risk_score"]

            # Store in Data Core
            store_simulation_result(city, revenue_gain, energy_savings, risk_score)

            # Generate Ledger Proof
            proof = vault.generate_proof("SIMULATION", city, revenue_gain)

        st.success("Simulation Completed Successfully")

        colA, colB, colC = st.columns(3)

        colA.metric("Revenue Gain ($)", f"{revenue_gain:,.2f}")
        colB.metric("Energy Savings ($)", f"{energy_savings:,.2f}")
        colC.metric("Traffic Risk Score", f"{risk_score}")

        st.markdown("### 🔐 Ledger Proof")
        st.code(f"Audit Hash: {proof['audit_hash']}\nStatus: {proof['status']}")

# ==========================================
# MODE 2 — GLOBAL OVERSIGHT
# ==========================================
else:

    st.header("🛰️ Global Oversight Console")

    data_rows = fetch_all_results()

    if data_rows:

        df = pd.DataFrame(data_rows, columns=[
            "ID","Timestamp","City","Revenue Gain","Energy Savings","Risk Score"
        ])

        total_revenue = df["Revenue Gain"].sum()
        total_savings = df["Energy Savings"].sum()

        colx, coly = st.columns(2)
        colx.metric("Total Simulated Revenue Gain", f"${total_revenue:,.2f}")
        coly.metric("Total Simulated Energy Savings", f"${total_savings:,.2f}")

        st.subheader("Simulation History")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No simulation data found. Run a simulation first.")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption("© 2026 FBC Digital Systems | Global Urban Intelligence OS")
