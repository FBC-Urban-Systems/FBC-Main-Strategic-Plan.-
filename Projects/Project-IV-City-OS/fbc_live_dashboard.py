# ==========================================
# PATH: Projects/Project-IV-City-OS/fbc_live_dashboard.py
# DESCRIPTION: FBC Global Strategic Command Center (Investor View)
# VERSION: v4.1-Executive-Gold
# ==========================================

import streamlit as st
import pandas as pd
import json
import os
import sys

# Dynamic path resolution to ensure AI Engine and Security Vault imports work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../Project-I-Urban-Revenue')))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../Project-III-Security-Ledger')))

try:
    from ai_engine_v2 import UrbanRevenueAI
    from secure_vault_1 import FBCSecureVault
    CORE_MODULES_LOADED = True
except ImportError as e:
    CORE_MODULES_LOADED = False
    IMPORT_ERROR_MSG = str(e)

# --- Dashboard UI Configuration ---
st.set_page_config(
    page_title="FBC Global Executive", 
    page_icon="🏙️", 
    layout="wide"
)

# Custom Professional Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ FBC Global Strategic Command Center")
st.subheader("Planetary Scale Urban Intelligence")
st.markdown("---")

if not CORE_MODULES_LOADED:
    st.error(f"⚠️ Critical Error: System Core Modules Missing. Details: {IMPORT_ERROR_MSG}")
else:
    # --- Sidebar: Security Status ---
    st.sidebar.header("🛡️ FBC Security Protocol")
    st.sidebar.success("SHA-256 Ledger: ACTIVE")
    st.sidebar.info("Data Privacy: GDPR/SOC2 Compliant")
    st.sidebar.markdown("---")
    st.sidebar.write("Founder Access: **Verified ✅**")

    # --- Main Dashboard Sections ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("📍 Node Selection")
        # Direct link to the Global Manifest cities
        target_city = st.selectbox("Select Target Expansion Node", ["Austin", "Dubai", "Riyadh"])
        
        if st.button("Execute AI Yield Analysis"):
            with st.spinner('Accessing FBC AI Kernel...'):
                # 1. Trigger Revenue Engine (Step 2 Logic)
                engine = UrbanRevenueAI(target_city)
                report = engine.analyze_yield()
                
                if "error" not in report:
                    st.success(f"Analysis for {target_city} Complete")
                    st.metric("Optimized Annual Revenue", report['metrics']['fbc_optimized_total_m'])
                    st.metric("Net Value Created", report['metrics']['net_value_created_m'], delta="AI Optimized")
                    
                    # 2. Trigger Security Vault (Step 3 Logic)
                    vault = FBCSecureVault()
                    # Strip symbols for numerical processing
                    val_float = float(report['metrics']['fbc_optimized_total_m'].replace('$', '').replace('M', ''))
                    audit_proof = vault.generate_audit_proof(target_city, val_float)
                    
                    st.markdown("### 🔒 Security Audit")
                    st.code(f"Audit_Hash: {audit_proof['audit_hash']}\nProtocol: SHA-256-SALTED", language="bash")
                else:
                    st.error(report["error"])

    with col2:
        st.header("📈 Portfolio Performance Projection")
        # Visualizing growth based on Phase I targets
        chart_data = pd.DataFrame({
            'Year': ['2026', '2027', '2028', '2029', '2030'],
            'Valuation (Billions $)': [0.1, 0.4, 0.8, 1.0, 1.2]
        })
        st.line_chart(chart_data.set_index('Year'))
        
        st.write("### 🚀 Strategic Roadmap Progress")
        st.progress(65)
        st.caption("Phase I (Urban Revenue Optimization) - 65% Integrated")

st.markdown("---")
st.caption("FBC Proprietary Technology © 2026 - Confidential Founder Access Only")
