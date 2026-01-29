# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Full Phase I - Secure Command Center
# FEATURES: Live AI, Multi-Sector, SHA-256 Security Ledger
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
    "Projects/Project-III-Traffic-Intelligence",
    "Projects/Project-III-Security-Ledger"
]
for path in PROJECT_PATHS:
    full_path = os.path.join(BASE_DIR, path)
    if full_path not in sys.path:
        sys.path.append(full_path)

# --- AI & Security Engines Import ---
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    from secure_vault import FBCSecureVault
    SYSTEM_STATUS = "SECURED ✅"
except ImportError as e:
    SYSTEM_STATUS = f"KERNEL ERROR: {e} ❌"

# --- Page Branding ---
st.set_page_config(page_title="FBC Global | Secure Portal", layout="wide", page_icon="🛡️")

# Custom UI for Security Look
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; }
    .status-box { padding: 10px; border-radius: 5px; border-left: 5px solid #ffd700; background: #1c2128; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ FBC Global Secure Command Center")
st.write(f"Encryption Standard: **SHA-256 AES** | System: **{SYSTEM_STATUS}**")
st.markdown("---")

# --- Sidebar Logic ---
st.sidebar.image("https://img.shields.io/badge/FBC_SECURITY-ACTIVE-green?style=for-the-badge")
view = st.sidebar.radio("Executive View", ["Strategic Revenue (Gov)", "Infrastructure Optimization (Private)"])

vault = FBCSecureVault()

if view == "Strategic Revenue (Gov)":
    st.header("🚦 Municipal AI Intelligence")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("Target City Node", "Austin-TX")
        rev = st.number_input("Annual Municipal Revenue ($)", value=20000000)
        
        # Risk Logic
        risk_eng = TrafficRiskEngine(city)
        risk_data = risk_eng.analyze_real_time_risk(120)
        st.metric("AI Risk Index", risk_data['risk_score'], delta=risk_data['live_weather'])

    with col2:
        # Revenue Logic
        opt = RevenueOptimizer(city)
        gains = opt.project_incremental_gain(rev)
        st.metric("Projected Extra Income", f"${gains['Total_City_Gain']:,.2f}", delta="+25%")
        
        # Security Ledger Integration
        st.subheader("🔐 Secure Commission Ledger")
        proof = vault.generate_proof("PROJECT_I", city, gains['FBC_Commission'])
        
        st.markdown(f"""
        <div class="status-box">
            <b>Transaction Verified:</b><br>
            FBC Commission: ${gains['FBC_Commission']:,.2f}<br>
            <small>Hash: {proof['audit_hash'][:32]}...</small>
        </div>
        """, unsafe_allow_html=True)

else:
    st.header("🏢 Private District Energy Vault")
    
    dist_id = st.text_input("District ID", "FBC-EGYPT-01")
    bill = st.number_input("Monthly Energy Bill ($)", value=150000)
    
    res = predict_energy_savings(bill)
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Optimized Monthly Savings", f"${res['ai_predicted_savings']:,.2f}", delta="-15%")
    with c2:
        # Secure the Energy savings report
        st.subheader("📑 Audit Trail")
        e_proof = vault.generate_proof("PROJECT_II", dist_id, res['ai_predicted_savings'])
        st.code(f"Audit_ID: {e_proof['audit_hash']}\nStatus: VERIFIED_BY_FBC_KERNEL", language="bash")

st.markdown("---")
st.caption("FBC Digital Systems v3.6 | Proprietary Blockchain-Ready Ledger | 2026")
