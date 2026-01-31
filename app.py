# ==========================================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center (Unified Interface)
# VERSION: v7.0.0 — REAL DATA LOCKED • FUTURE PROOF
# ROLE: Executive Control Panel for All FBC Intelligence Engines
# ==========================================================

import os
import sys
import streamlit as st

# ==========================================================
# PATH SETUP (SAFE & DETERMINISTIC)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "Projects")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)
sys.path.insert(0, PROJECTS_DIR)

# ==========================================================
# REAL DATA ENGINE IMPORTS (CONTRACT SAFE)
# ==========================================================
from Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Project_II_Private_Districts.energy_forecast import predict_energy_savings
from Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine

from reports.pdf_report_generator import generate_fbc_report

# ==========================================================
# STREAMLIT CONFIG
# ==========================================================
st.set_page_config(
    page_title="FBC Global Command Center",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("FBC Global Command Center")
st.caption("Supreme Real-Data Urban Intelligence Platform")

st.markdown("---")

# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================
module = st.sidebar.radio(
    "Select Intelligence Module",
    (
        "Traffic Risk Analysis",
        "Revenue Projection",
        "Energy Savings Forecast",
    ),
)

# ==========================================================
# MODULE 1 — TRAFFIC RISK
# ==========================================================
if module.startswith("Traffic"):
    st.header("Real-Time Traffic Risk Intelligence")

    city = st.text_input("City Name", value="Cairo")
    density = st.slider("Traffic Density Index", 0, 300, 120)

    if st.button("Run Traffic Analysis", type="primary"):
        engine = TrafficRiskEngine(city)
        result = engine.analyze_real_time_risk(density)

        st.success("Traffic Analysis Completed")

        st.metric("Risk Score", result["risk_score"])
        st.write("Weather Condition:", result["weather"])

        if st.button("Generate PDF Report"):
            pdf_path = os.path.join(REPORTS_DIR, f"Traffic_Report_{city}.pdf")
            generate_fbc_report(
                "Traffic Risk Analysis Report",
                {
                    "City": city,
                    "Traffic Density": density,
                    "Weather": result["weather"],
                    "Risk Score": result["risk_score"],
                },
                pdf_path,
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                )

# ==========================================================
# MODULE 2 — REVENUE
# ==========================================================
elif module.startswith("Revenue"):
    st.header("GDP-Based Urban Revenue Projection")

    city = st.text_input("City Name", value="Cairo")
    annual_revenue = st.number_input(
        "Current Annual City Revenue (USD)",
        min_value=0.0,
        value=5_000_000.0,
        step=100_000.0,
    )

    if st.button("Run Revenue Projection", type="primary"):
        engine = RevenueOptimizer(city)
        result = engine.project_incremental_gain(annual_revenue)

        st.success("Revenue Projection Completed")

        st.metric("Projected Total Gain", f"${result['Total_City_Gain']:,.2f}")

        if st.button("Generate PDF Report"):
            pdf_path = os.path.join(REPORTS_DIR, f"Revenue_Report_{city}.pdf")
            generate_fbc_report(
                "Urban Revenue Projection Report",
                result,
                pdf_path,
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                )

# ==========================================================
# MODULE 3 — ENERGY
# ==========================================================
else:
    st.header("Energy Cost Optimization & Savings")

    annual_energy_bill = st.number_input(
        "Annual Energy Bill (USD)",
        min_value=0.0,
        value=150_000.0,
        step=10_000.0,
    )

    if st.button("Run Energy Forecast", type="primary"):
        result = predict_energy_savings(annual_energy_bill)

        st.success("Energy Forecast Completed")

        st.metric(
            "AI Predicted Savings",
            f"${result['ai_predicted_savings']:,.2f}",
        )

        if st.button("Generate PDF Report"):
            pdf_path = os.path.join(REPORTS_DIR, "Energy_Report.pdf")
            generate_fbc_report(
                "Energy Savings Forecast Report",
                result,
                pdf_path,
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                )

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")
st.caption("© 2026 FBC Digital Systems — REAL DATA • AUDIT READY • FUTURE PROOF")
