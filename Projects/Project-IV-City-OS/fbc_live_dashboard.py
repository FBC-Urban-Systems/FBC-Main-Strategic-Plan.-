# ==========================================
# PATH: Projects/Project-IV-City-OS/dashboard.py
# DESCRIPTION: FBC Global Strategic Command Center (Investor View)
# VERSION: v2.6-Executive-Gold
# ==========================================

import streamlit as st
import pandas as pd
import json
import os

# Page Configuration
st.set_page_config(
    page_title="FBC Global Executive Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Investor Experience
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ffd700;
    }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def load_global_manifest():
    """Syncs with the central financial manifest."""
    manifest_path = '../../global_cities_manifest.json'
    if not os.path.exists(manifest_path):
        manifest_path = 'global_cities_manifest.json'
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except Exception:
        return None

data = load_global_manifest()

if data:
    metrics = data['financial_model_v2']
    
    # --- SIDEBAR (Operational Context) ---
    st.sidebar.image("https://img.shields.io/badge/FBC_OS-v2.6.0-gold?style=for-the-badge")
    st.sidebar.title("Operational Control")
    st.sidebar.success(f"Audit Status: {data['technical_compliance']['audit_status']} ✅")
    st.sidebar.divider()
    st.sidebar.write("**Strategic Targets (2030):**")
    st.sidebar.write(f"- Valuation: ${metrics['series_a_valuation_target_usd_b']}B")
    st.sidebar.write("- LTV/CAC: 40x+")
    st.sidebar.divider()
    st.sidebar.caption("FBC Confidential Proprietary System")

    # --- MAIN HEADER ---
    st.title("🏙️ FBC Global Strategic Command Center")
    st.markdown("#### *AI-Driven Urban Revenue Optimization & Planetary Scale Intelligence*")
    st.divider()

    # SECTION 1: GLOBAL FINANCIALS (Based on PDF Page 1 & 5)
    st.subheader("🚀 Phase I Financial Performance (2027-2030)")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Seed Funding Ask", f"${metrics['seed_funding_ask_usd_m']}M", "2027 Launch")
    col2.metric("Target LTV/CAC", "40.2x", "Industry Leading")
    col3.metric("Projected ARR (2027)", f"${metrics['projected_arr_2027_usd_m']}M", "Series A Pipeline")
    col4.metric("EBITDA Margin", "45%", "Target 2037")

    st.divider()

    # SECTION 2: PROJECT II SIMULATOR (Private Districts - PDF Page 2)
    st.subheader("🏢 Project II: Private Smart District Expansion")
    
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.write("##### ROI Simulator")
        districts = st.slider("Select Active Districts (2030 Target: 25)", 1, 100, 25)
        avg_setup = st.select_slider("Avg. Setup Fee (Million $)", options=[1, 1.5, 2, 2.5, 3], value=2)
        
        # [span_3](start_span)Calculation based on Strategic Plan[span_3](end_span)
        total_revenue = districts * (avg_setup + 0.75) # Fee + Avg SaaS
        st.metric("Estimated District Revenue", f"${total_revenue}M", delta="Setup + Annual SaaS")

    with right_col:
        st.write("##### Expansion Roadmap & City Nodes")
        df_nodes = pd.DataFrame(metrics['expansion_nodes'])
        st.dataframe(df_nodes, use_container_width=True, hide_index=True)

    st.divider()

    # SECTION 3: REVENUE STREAMS & COMPLIANCE
    bot_left, bot_right = st.columns(2)
    
    with bot_left:
        st.subheader("💰 Revenue Distribution")
        for stream in metrics['revenue_streams']:
            st.write(f"**{stream['stream']}** ({stream['contribution_percent']}%)")
            st.progress(stream['contribution_percent'] / 100)

    with bot_right:
        st.subheader("🛡️ System Integrity & Security")
        st.code(f"Protocol: {data['technical_compliance']['security_protocol']}\nStatus: ENCRYPTED\nAudit: VERIFIED", language="bash")
        st.write(f"Compliance Standard: **{data['technical_compliance']['data_privacy']}**")

else:
    st.error("CRITICAL ERROR: Global Manifest not found. Please sync repository.")

# FOOTER
st.markdown("---")
st.caption(f"© 2026 FBC Digital Systems | Headquarters: Austin, Texas | Version {data['system_metadata']['version'] if data else 'N/A'}")
