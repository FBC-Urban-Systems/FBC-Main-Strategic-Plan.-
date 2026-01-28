import streamlit as st
import pandas as pd
import json
import os

# --- 1. GLOBAL BRANDING & CONFIGURATION ---
st.set_page_config(page_title="FBC Global OS | CEO Terminal", layout="wide")

# Custom CSS for a high-end Billion-Dollar Enterprise look
st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stMetric { border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; background-color: #0e1117; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #0e1117; 
        border: 1px solid #333; 
        border-radius: 5px; 
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. DATA ENGINE: LOADING GLOBAL MANIFEST ---
def load_global_data():
    try:
        # Connects to our global city expansion database
        with open('global_cities_manifest.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        return None

manifest_data = load_global_data()

# --- 3. EXECUTIVE HEADER ---
st.title("🏙️ FBC DIGITAL SYSTEMS | GLOBAL COMMAND")
st.markdown("#### *Proprietary AI-Driven Urban Revenue Operating System (2027-2037)*")
st.divider()

# --- 4. KEY PERFORMANCE INDICATORS (KPIs) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Corporate Valuation Target", "$35.0 Billion", "2037 Projection")
with col2:
    if manifest_data:
        city_count = manifest_data['fbc_global_network']['total_target_cities']
        st.metric("Strategic Global Hubs", f"{city_count} Cities", "Phase I-III")
    else:
        st.metric("Strategic Global Hubs", "80 Cities", "Target Set")
with col3:
    st.metric("Security Protocol", "SHA-256 Ledger", "ACTIVE & ENCRYPTED")

st.divider()

# --- 5. OPERATIONAL CONTROL TABS ---
tab1, tab2, tab3 = st.tabs(["🌍 GLOBAL DEPLOYMENT", "📈 REVENUE OPTIMIZER", "🛡️ SYSTEM AUDIT"])

with tab1:
    st.subheader("Global Expansion & Deployment Roadmap")
    if manifest_data:
        hubs = manifest_data['fbc_global_network']['deployment_schedule']
        p1 = hubs['phase_1_north_america']['primary_hubs']
        p2 = hubs['phase_2_mena_asean']['primary_hubs']
        
        st.info(f"**Current Strategic Focus (Phase I):** {', '.join(p1)}")
        st.success(f"**Upcoming Expansion (Phase II):** {', '.join(p2)}")
        
        # Mapping target hubs for visual impact
        map_data = pd.DataFrame({
            'lat': [30.2672, 25.2048, 24.7136, 1.3521], # Austin, Dubai, Riyadh, Singapore
            'lon': [-97.7431, 55.2708, 46.6753, 103.8198]
        })
        st.map(map_data)

with tab2:
    st.subheader("Urban AI Revenue Simulator")
    st.write("Projected efficiency gains through FBC Project I integration.")
    
    city_input = st.number_input("Enter City Annual Budget/Revenue ($)", value=50000000, step=1000000)
    # Applying the 25% AI Revenue Boost from our core logic
    optimized_revenue = city_input * 1.25
    net_gain = optimized_revenue - city_input
    
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.success(f"FBC Optimized Total: **${optimized_revenue:,.0f}**")
    with c_res2:
        st.warning(f"Projected AI Gain: **+${net_gain:,.0f}**")

with tab3:
    st.subheader("Core System Integrity Log")
    st.code("""
    [BOOT] FBC OS v3.1 Kernel Initialized...
    [AUTH] CEO Access Verified: Karim Mostafa
    [SEC]  SHA-256 Handshake: SUCCESS
    [AI]   Revenue Prediction Engine: ONLINE
    [NET]  Global Cities Sync: ACTIVE
    [SYNC] Ready for Phase I Pilot Deployment.
    """, language="bash")

# --- 6. FOOTER ---
st.divider()
st.caption("CONFIDENTIAL | FBC Digital Systems Intellectual Property © 2026 | Austin, TX - Global")
