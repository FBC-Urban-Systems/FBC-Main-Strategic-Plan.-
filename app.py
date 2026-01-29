# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Strategic Client Portal (SaaS Interface)
# VERSION: v3.2.0-Production
# ==========================================

import streamlit as st
import pandas as pd
import sys
import os

# Ensure the kernel and project paths are recognized
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "Projects/Project-I-Urban-Revenue"))
sys.path.append(os.path.join(BASE_DIR, "Projects/Project-II-Private-Districts"))

# Importing your AI Engines
try:
    from energy_forecast import predict_energy_savings
    from revenue_optimizer import RevenueOptimizer
except ImportError as e:
    st.error(f"Critical Error: AI Modules not found. System Trace: {e}")

# Page Configuration (Premium Branding)
st.set_page_config(
    page_title="FBC Digital Systems | Client Intelligence Portal",
    page_icon="🏙️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ FBC Global Strategic Intelligence")
st.subheader("Urban Revenue & Energy Optimization Hub")
st.markdown("---")

# Sidebar for Navigation and Input
st.sidebar.image("https://img.shields.io/badge/FBC_OS-OPERATIONAL-green?style=for-the-badge", use_column_width=False)
st.sidebar.header("Global Control Center")
client_type = st.sidebar.selectbox("Select Sector", ["Private Smart Districts", "Municipal Governments"])

if client_type == "Private Smart Districts":
    st.header("🏢 Private District Energy Optimization")
    st.info("Targeting 15% Reduction in Grid Operational Costs.")
    
    col1, col2 = st.columns(2)
    with col1:
        monthly_bill = st.number_input("Average Monthly Energy Expenditure ($)", min_value=1000, value=100000, step=5000)
        units = st.slider("Total Integrated Infrastructure Units", 10, 5000, 500)
    
    # Execute AI Forecast (Project II)
    results = predict_energy_savings(monthly_bill)
    
    with col2:
        st.subheader("AI Efficiency Projection")
        st.metric("Annual Savings Opportunity", f"${results['ai_predicted_savings'] * 12:,.2f}", delta="15% Optimized")
        st.write(f"New Monthly Operational Cost: **${results['new_optimized_cost']:,.2f}**")
        st.button("Download Full Energy Audit PDF")

elif client_type == "Municipal Governments":
    st.header("💰 Urban Revenue Growth Engine")
    st.info("AI-Driven Yield Optimization for Smart Cities.")
    
    col1, col2 = st.columns(2)
    with col1:
        city_name = st.text_input("Municipality Name", "New Austin")
        current_revenue = st.number_input("Current Annual Infrastructure Revenue ($)", min_value=100000, value=5000000)
    
    # Execute Revenue AI (Project I)
    opt = RevenueOptimizer(city_name)
    gain = opt.project_incremental_gain(current_revenue)
    
    with col2:
        st.subheader("Financial Impact Analysis")
        st.metric("Projected Revenue Uplift", f"${gain['Total_City_Gain']:,.2f}", delta="+25% Efficiency")
        st.success(f"FBC Managed Share: ${gain['FBC_Commission']:,.2f}")
        st.write(f"Net City Profit (After FBC Share): **${gain['ROI_for_City']:,.2f}**")

st.markdown("---")
st.caption("© 2026 FBC Digital Systems | Secure SHA-256 Ledger Active | Austin, TX")
