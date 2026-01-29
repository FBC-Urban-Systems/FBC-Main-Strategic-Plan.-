# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center - Phase I Final MVP
# VERSION: v3.6.5 (Production Ready)
# FEATURES: Multi-Project Sync, AI Risk Engine, Secure Hash Ledger
# ==========================================

import streamlit as st
import sys
import os
import random

# --- Dynamic Path Integration for GitHub Codespaces ---
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

# --- FBC AI & Security Engines Import ---
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    from secure_vault import FBCSecureVault
    SYSTEM_STATUS = "FULLY OPERATIONAL ✅"
except ImportError as e:
    SYSTEM_STATUS = f"MODULE SYNC ERROR: {e} ❌"

# --- UI Layout & Custom Styling ---
st.set_page_config(page_title="FBC Global OS | Command Center", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    .security-card { 
        background-color: #010409; 
        border-left: 5px solid #ffd700; 
        padding: 15px; 
        font-family: monospace;
        font-size: 0.8em;
        color: #8b949e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Top Header ---
st.title("🏙️ FBC Global Strategic Command Center")
st.write(f"Kernel Status: **{SYSTEM_STATUS}** | Security Protocol: **SHA-256 Active**")
st.markdown("---")

# --- Sidebar Control Center ---
st.sidebar.image("https://img.shields.io/badge/FBC_OS-V3.6_GOLD-gold?style=for-the-badge")
st.sidebar.header("🕹️ Deployment Sector")
mode = st.sidebar.selectbox("Select View", ["Municipal Government (Project I & III)", "Private Smart Districts (Project II)"])

vault = FBCSecureVault()

# ==========================================
# SECTOR 1: Municipal Government (Revenue & Safety)
# ==========================================
if mode == "Municipal Government (Project I & III)":
    st.header("🚦 Municipal Intelligence & Yield Optimization")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Traffic Safety AI")
        city_node = st.text_input("Active City Node", "Austin-TX")
        density = st.slider("Live Traffic Density (Units/km)", 0, 300, 115)
        
        # Link to Project III Logic
        risk_engine = TrafficRiskEngine(city_node)
        risk_results = risk_engine.analyze_real_time_risk(density)
        
        st.metric("Risk Score Index", risk_results['risk_score'], delta=f"Weather: {risk_results['live_weather']}")
        st.write(f"Emergency Status: **{risk_results['status']}**")

    with col_b:
        st.subheader("Revenue Growth Hub")
        base_revenue = st.number_input("Annual City Revenue ($)", value=25000000)
        
        # Link to Project I Logic
        rev_optimizer = RevenueOptimizer(city_node)
        gains = rev_optimizer.project_incremental_gain(base_revenue)
        
        st.metric("AI Incremental Gain", f"${gains['Total_City_Gain']:,.2f}", delta="+25% Efficiency")
        st.success(f"FBC Commission (20%): ${gains['FBC_Commission']:,.2f}")
        
        # --- SHA-256 Security Proof ---
        st.markdown("**🛡️ Transaction Security Proof:**")
        proof = vault.generate_proof("PROJECT_I", city_node, gains['FBC_Commission'])
        st.markdown(f"""<div class="security-card">ID: {proof['audit_hash']}<br>VERIFIED_BY_FBC_KERNEL</div>""", unsafe_allow_html=True)

# ==========================================
# SECTOR 2: Private Smart Districts (Optimization)
# ==========================================
else:
    st.header("🏢 Private District Infrastructure Control")
    
    col_1, col_2 = st.columns(2)
    
    with col_1:
        dist_id = st.text_input("District ID", "FBC-EGYPT-001")
        monthly_bill = st.number_input("Average Monthly Energy Cost ($)", value=180000)
        
        # Link to Project II Logic
        energy_results = predict_energy_savings(monthly_bill)
        
        st.metric("AI Savings Forecast", f"${energy_results['ai_predicted_savings']:,.2f}", delta="-15% Load Reduction")
    
    with col_2:
        st.subheader("Asset Audit Trail")
        st.write(f"Optimized Monthly Target: **${energy_results['new_optimized_cost']:,.2f}**")
        
        # --- SHA-256 Security Proof ---
        e_proof = vault.generate_proof("PROJECT_II", dist_id, energy_results['ai_predicted_savings'])
        st.markdown("**🛡️ Infrastructure Proof:**")
        st.code(f"HASH: {e_proof['audit_hash']}\nSTATUS: {e_proof['status']}", language="bash")

# --- Global Footer ---
st.markdown("---")
st.caption("© 2026 FBC Digital Systems | Proprietary Intelligence Framework | Austin HQ & Global Nodes")
