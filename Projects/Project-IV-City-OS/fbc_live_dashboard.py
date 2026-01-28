import streamlit as st
import pandas as pd
import json
from datetime import datetime

# --- 1. GLOBAL BRANDING & CONFIGURATION ---
st.set_page_config(page_title="FBC Global OS | CEO Command Center", layout="wide")

# High-end Corporate UI Styling (Billion-Dollar Look)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { border: 1px solid #00ffcc; border-radius: 10px; padding: 20px; background-color: #0e1117; box-shadow: 0 4px 15px rgba(0,255,204,0.1); }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Orbitron', sans-serif; }
    .stButton>button { background-color: #00ffcc; color: black; border-radius: 5px; font-weight: bold; width: 100%; }
    .status-box { border: 1px solid #333; padding: 15px; border-radius: 10px; background: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: #0e1117; 
        border-radius: 5px; border: 1px solid #333; color: #00ffcc;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- 2. EXECUTIVE HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏙️ FBC DIGITAL SYSTEMS | GLOBAL OS")
    st.subheader("Strategic Command Center: Phase I Deployment")
with col_h2:
    st.metric("SYSTEM STATUS", "ACTIVE", delta="SHA-256 VERIFIED")

st.divider()

# --- 3. CORE FINANCIAL KPIS (The $35B Path) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("VALUATION TARGET", "$35,000,000,000", delta="By 2037")
with m2:
    st.metric("EXPANSION NODES", "80 GLOBAL CITIES", delta="Active Growth")
with m3:
    st.metric("UNIT ECONOMICS", "42x LTV/CAC", delta="Optimized")
with m4:
    st.metric("PHASE I ARR", "$40M - $60M", delta="Target")

# --- 4. THE STRATEGIC WORKSPACE ---
tab1, tab2, tab3 = st.tabs(["🌍 Global Expansion", "💰 Revenue Optimizer", "🧠 Ecosystem Health"])

with tab1:
    st.subheader("Global Deployment Hubs")
    # Data derived from global_cities_manifest.json
    map_data = pd.DataFrame({
        'city': ['Austin (HQ)', 'Dubai', 'Riyadh', 'Singapore', 'London', 'Toronto'],
        'lat': [30.2672, 25.2048, 24.7136, 1.3521, 51.5074, 43.6532],
        'lon': [-97.7431, 55.2708, 46.6753, 103.8198, -0.1278, -79.3832]
    })
    st.map(map_data)
    st.info("Primary Focus: North America & MENA Region (Saudi Arabia / UAE)")

with tab2:
    st.subheader("Project I: AI Revenue Engine Simulation")
    col_in, col_out = st.columns([1, 1])
    
    with col_in:
        base_val = st.number_input("Input City Revenue Base ($M)", value=100.0, step=10.0)
        efficiency = st.slider("AI Optimization Factor (%)", 10, 30, 25)
    
    with col_out:
        boosted = base_val * (1 + (efficiency/100))
        net = boosted - base_val
        st.success(f"Optimized Annual Revenue: ${boosted:,.2f}M")
        st.warning(f"AI-Generated Surplus: +${net:,.2f}M")

with tab3:
    st.subheader("Ecosystem Integration Status")
    projects = {
        "Project I: Urban Revenue Engine": "OPERATIONAL ✅",
        "Project II: Private Smart Districts": "ACTIVE ✅",
        "Project III: Traffic Intelligence": "BETA TESTING 🚦",
        "Project IV: City-OS Kernel": "INTEGRATING 🧠",
        "Project V: Digital Earth Data": "READY 🔒",
        "Project VI: Global Scaling": "SIMULATING 🌍"
    }
    for p, status in projects.items():
        c1, c2 = st.columns([2, 1])
        c1.write(f"**{p}**")
        c2.info(status)

# --- 5. FOOTER ---
st.divider()
st.caption(f"FBC Confidential CEO Terminal | Last Sync: {datetime.now().isoformat()} | Secure Node: TX-AUS-001")
