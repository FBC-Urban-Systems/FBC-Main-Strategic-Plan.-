# ==========================================
# PATH: Projects/Project-IV-City-OS/dashboard.py
# DESCRIPTION: FBC Global Strategic Command Center (Investor View)
# VERSION: v2.5-Executive
# ==========================================

import streamlit as st
import pandas as pd
import json
import os

# Page Configuration for a professional look
st.set_page_config(
    page_title="FBC Global Executive Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match FBC Branding
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    </style>
    """, unsafe_allow_html=True)

def load_global_manifest():
    """Loads the core financial and expansion data from the Root Manifest."""
    manifest_path = '../../global_cities_manifest.json'
    # Fallback for different execution contexts
    if not os.path.exists(manifest_path):
        manifest_path = 'global_cities_manifest.json'
        
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading system data: {e}")
        return None

# Load System Data
data = load_global_manifest()

if data:
    metrics = data['financial_model_v2']
    
    # --- SIDEBAR ---
    st.sidebar.image("https://img.shields.io/badge/FBC_OS-v2.2.0-gold?style=for-the-badge")
    st.sidebar.title("Navigation")
    st.sidebar.info("Operational Status: **ACTIVE**")
    st.sidebar.divider()
    st.sidebar.write(f"**Security Protocol:** {data['technical_compliance']['security_protocol']}")
    st.sidebar.write(f"**Last Audit:** {data['technical_compliance']['audit_status']} ✅")

    # --- MAIN CONTENT ---
    st.title("🏙️ FBC Global Strategic Command Center")
    st.markdown("### *Proprietary Urban Intelligence & Revenue Optimization*")
    
    st.divider()

    # Section 1: Executive KPI Metrics
    st.subheader("🚀 Financial Performance & Valuation")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Target Valuation", f"${metrics['series_a_valuation_target_usd_b']}B", "Phase I Goal")
    col2.metric("LTV/CAC Ratio", f"{metrics['unit_economics']['ltv_cac_ratio']}x", "Top Tier")
    col3.metric("Projected ARR (2027)", f"${metrics['projected_arr_2027_usd_m']}M", "Scale Target")
    col4.metric("Gross Margin", f"{metrics['unit_economics']['gross_margin_percent']}%", "SaaS Standard")

    st.divider()

    # Section 2: Expansion & Revenue Breakdown
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🌍 Active & Strategic City Nodes")
        df_nodes = pd.DataFrame(metrics['expansion_nodes'])
        # Styling the dataframe for display
        st.dataframe(df_nodes, use_container_width=True, hide_index=True)

    with right_col:
        st.subheader("💰 Revenue Streams")
        streams = metrics['revenue_streams']
        for s in streams:
            st.write(f"**{s['stream']}**")
            st.progress(s['contribution_percent'] / 100)
            st.caption(f"Contribution: {s['contribution_percent']}%")

    st.divider()
    
    # Section 3: Compliance & Trust
    st.subheader("🛡️ System Integrity")
    t_col1, t_col2 = st.columns(2)
    t_col1.success(f"Audit Status: {data['technical_compliance']['audit_status']}")
    t_col2.info(f"Compliance: {data['technical_compliance']['data_privacy']}")

else:
    st.warning("Please ensure 'global_cities_manifest.json' is present in the repository root.")

# Footer
st.markdown("---")
st.caption("FBC Confidential | Prepared for Executive Review | © 2026")
