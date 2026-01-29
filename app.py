# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center - Persistent Intelligence Edition
# VERSION: v3.8.0 (Database Integrated)
# ==========================================

import streamlit as st
import sys
import os
import pandas as pd

# --- Path Integration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDERS = [
    "Project-I-Urban-Revenue",
    "Project-II-Private-Districts",
    "Project-III-Traffic-Intelligence",
    "Project-III-Security-Ledger"
]
for folder in PROJECT_FOLDERS:
    sys.path.append(os.path.join(BASE_DIR, "Projects", folder))

# --- Engine Imports ---
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    from secure_vault import FBCSecureVault
    
    vault = FBCSecureVault()
    SYSTEM_STATUS = "SECURED & LOGGING ✅"
except Exception as e:
    SYSTEM_STATUS = f"KERNEL SYNC ERROR: {e} ❌"

# --- Dashboard Config ---
st.set_page_config(page_title="FBC Global | Intelligent Ledger", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e6edf3; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; }
    .audit-card { background-color: #010409; border-left: 4px solid #ffd700; padding: 15px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ FBC Global Strategic Intelligence")
st.caption(f"Status: {SYSTEM_STATUS} | SHA-256 Ledger Active")
st.markdown("---")

# --- Sidebar Control ---
st.sidebar.image("https://img.shields.io/badge/FBC_OS-V3.8_PRO-gold?style=for-the-badge")
mode = st.sidebar.radio("Deployment Sector", ["Governments", "Private Developers"])

# ==========================================
# SECTOR: Governments (Revenue & Safety)
# ==========================================
if mode == "Governments":
    st.header("🚦 Municipal Operations & Revenue Hub")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Live Traffic Risk AI")
        city = st.text_input("City Node", "Austin-TX")
        density = st.slider("Traffic Density", 0, 300, 150)
        risk_eng = TrafficRiskEngine(city)
        risk_res = risk_eng.analyze_real_time_risk(density)
        st.metric("Risk Score", risk_res['risk_score'], delta=risk_res['live_weather'])

    with col2:
        st.subheader("Revenue Yield Optimization")
        rev_val = st.number_input("Annual Revenue ($)", value=10000000)
        opt = RevenueOptimizer(city)
        gain = opt.project_incremental_gain(rev_val)
        st.metric("AI Incremental Gain", f"${gain['Total_City_Gain']:,.2f}", delta="+25%")
        
        # --- SECURE LOGGING ---
        if st.button("Authorize & Secure Transaction"):
            proof = vault.generate_proof("PROJECT_I", city, gain['FBC_Commission'])
            st.markdown(f'<div class="audit-card">HASH: {proof["audit_hash"]}<br>STATUS: {proof["status"]}</div>', unsafe_allow_html=True)

# ==========================================
# SECTOR: Private Developers (Energy)
# ==========================================
else:
    st.header("🏢 Private Infrastructure Optimization")
    col_a, col_b = st.columns(2)
    
    with col_a:
        dist_id = st.text_input("District ID", "FBC-EGYPT-01")
        bill = st.number_input("Monthly Energy Bill ($)", value=200000)
        energy_res = predict_energy_savings(bill)
        st.metric("AI Forecasted Savings", f"${energy_res['ai_predicted_savings']:,.2f}", delta="-15%")

    with col_b:
        st.subheader("Security Audit")
        if st.button("Log Savings Report"):
            e_proof = vault.generate_proof("PROJECT_II", dist_id, energy_res['ai_predicted_savings'])
            st.code(f"Audit_Hash: {e_proof['audit_hash']}\nStatus: {e_proof['status']}")

# --- MASTER AUDIT TRAIL (THE PERSISTENCE VIEW) ---
st.markdown("---")
st.header("📜 Master Audit Ledger (Permanent Record)")
logs_df = vault.get_all_logs()
if not logs_df.empty:
    st.dataframe(logs_df.tail(10), use_container_width=True)
    st.metric("Total Value Secured (System Lifetime)", f"${logs_df['Value'].sum():,.2f}")
else:
    st.info("No transactions logged yet. Authorize a transaction to start the ledger.")

st.caption("© 2026 FBC Digital Systems | Intelligence & Security Unified")
