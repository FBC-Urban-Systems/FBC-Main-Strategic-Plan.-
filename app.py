# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center
# VERSION: v6.0.0 REAL-DATA + PDF-DEMO
# ==========================================

import streamlit as st
import os

# ==========================================
# PATH INTEGRATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_PATH = os.path.join(BASE_DIR, "Projects")
REPORTS_PATH = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_PATH, exist_ok=True)

import sys
sys.path.append(PROJECTS_PATH)

# ==========================================
# IMPORT REAL-DATA ENGINES
# ==========================================
from Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Project_II_Private_Districts.energy_forecast import EnergyForecaster
from Project_III_Traffic_Intelligence.accident_pred import TrafficRiskEngine

# PDF Generator
from reports.pdf_report_generator import generate_fbc_report

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(page_title="FBC Global Command Center", layout="wide")

st.title("🌍 FBC Global Command Center")
st.caption("Real-Data Urban Intelligence Platform")

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================
mode = st.sidebar.radio(
    "Select Module",
    [
        "Traffic Risk Analysis",
        "Revenue Forecast",
        "Energy Forecast"
    ]
)

# ==========================================
# MODULE 1 — TRAFFIC
# ==========================================
if mode == "Traffic Risk Analysis":

    st.header("🚦 Real-Time Traffic Risk Engine")

    city = st.text_input("City Name", "Cairo")
    density = st.slider("Traffic Density Index", 0, 300, 120)

    if st.button("Run Traffic Analysis"):

        engine = TrafficRiskEngine(city)
        result = engine.analyze_real_time_risk(density)

        st.success("Analysis Completed")

        st.metric("Risk Score", result["risk_score"])
        st.write("Weather:", result["weather"])

        # PDF Button
        if st.button("📄 Generate PDF Report"):
            report_data = {
                "City": result["city"],
                "Traffic Density": result["traffic_density"],
                "Weather Condition": result["weather"],
                "Risk Score": result["risk_score"]
            }

            output_file = os.path.join(REPORTS_PATH, f"Traffic_Report_{city}.pdf")
            pdf_result = generate_fbc_report(
                "Traffic Risk Analysis Report",
                report_data,
                output_file
            )

            st.success(pdf_result["status"])
            with open(output_file, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF",
                    data=f,
                    file_name=f"Traffic_Report_{city}.pdf"
                )

# ==========================================
# MODULE 2 — REVENUE
# ==========================================
elif mode == "Revenue Forecast":

    st.header("💰 Real GDP-Based Revenue Engine")

    country_code = st.text_input("Country Code (EG, US, AE)", "EG")

    if st.button("Run Revenue Forecast"):

        engine = RevenueOptimizer(country_code)
        result = engine.project_incremental_gain()

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Forecast Completed")

            st.metric("GDP Per Capita", f"${result['gdp_per_capita']:,.2f}")
            st.metric("Estimated City Revenue", f"${result['estimated_city_revenue']:,.2f}")
            st.metric("FBC Projected Gain", f"${result['fbc_projected_gain']:,.2f}")

            # PDF Button
            if st.button("📄 Generate PDF Report"):
                report_data = result

                output_file = os.path.join(REPORTS_PATH, f"Revenue_Report_{country_code}.pdf")
                pdf_result = generate_fbc_report(
                    "Revenue Forecast Report",
                    report_data,
                    output_file
                )

                st.success(pdf_result["status"])
                with open(output_file, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        data=f,
                        file_name=f"Revenue_Report_{country_code}.pdf"
                    )

# ==========================================
# MODULE 3 — ENERGY
# ==========================================
else:

    st.header("⚡ Real Energy Cost & Savings Engine")

    country_code = st.text_input("Country Code (EG, US, AE)", "EG")

    if st.button("Run Energy Forecast"):

        engine = EnergyForecaster(country_code)
        result = engine.forecast()

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Forecast Completed")

            st.metric("Electricity Price (USD/kWh)", result["price_per_kwh"])
            st.metric("Total National Energy Cost", f"${result['total_energy_cost_usd']:,.2f}")
            st.metric("FBC Projected Savings", f"${result['fbc_projected_savings']:,.2f}")

            # PDF Button
            if st.button("📄 Generate PDF Report"):
                report_data = result

                output_file = os.path.join(REPORTS_PATH, f"Energy_Report_{country_code}.pdf")
                pdf_result = generate_fbc_report(
                    "Energy Forecast Report",
                    report_data,
                    output_file
                )

                st.success(pdf_result["status"])
                with open(output_file, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        data=f,
                        file_name=f"Energy_Report_{country_code}.pdf"
                    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption("© 2026 FBC Digital Systems — Real Data Urban Intelligence Platform")
