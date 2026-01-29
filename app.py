# =====================================================
# FBC URBAN AI – FIRST PUBLIC WEB APP MVP
# Simple Revenue & Energy Simulation Interface
# =====================================================

import streamlit as st

# Import AI Engines
from Projects.Project_I_Urban_Revenue.revenue_optimizer import RevenueOptimizer
from Projects.Project_II_Private_Districts.energy_forecast import EnergyForecaster

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="FBC Urban AI Simulator",
    page_icon="🏙️",
    layout="centered"
)

# -----------------------------------------------------
# Header
# -----------------------------------------------------
st.title("🏙️ FBC Urban AI Simulator")
st.markdown("""
**First Public AI Prototype of FBC Urban Systems**  
Simulate **City Revenue Optimization** and **Energy Forecasting** in real-time.
""")

st.divider()

# -----------------------------------------------------
# User Inputs
# -----------------------------------------------------
city = st.text_input("🌍 City Name", "Cairo")

population = st.number_input(
    "👥 Population",
    min_value=100000,
    max_value=50000000,
    value=5000000,
    step=100000
)

energy_price = st.number_input(
    "⚡ Energy Price per kWh ($)",
    min_value=0.01,
    max_value=1.00,
    value=0.12,
    step=0.01
)

# -----------------------------------------------------
# Run Simulation Button
# -----------------------------------------------------
run = st.button("🚀 Run Simulation")

# -----------------------------------------------------
# Simulation Logic
# -----------------------------------------------------
if run:
    with st.spinner("Running AI Simulation..."):

        revenue_engine = RevenueOptimizer()
        energy_engine = EnergyForecaster()

        projected_revenue = revenue_engine.simulate(city, population)
        projected_energy_cost = energy_engine.forecast(city, population, energy_price)

    st.success("Simulation Completed Successfully ✅")

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        label="💰 Projected Annual Revenue ($)",
        value=f"{projected_revenue:,.0f}"
    )

    col2.metric(
        label="🔋 Projected Annual Energy Cost ($)",
        value=f"{projected_energy_cost:,.0f}"
    )

    st.divider()

    st.markdown("### 📊 AI Interpretation")

    st.write(f"""
For **{city}**, with a population of **{population:,}**,  
the FBC AI projects an optimized annual revenue of  
**${projected_revenue:,.0f}**

and an estimated annual energy operational cost of  
**${projected_energy_cost:,.0f}**.
""")

    st.info("🔒 This is an MVP prototype. Payment & PDF reports will be added next.")

# -----------------------------------------------------
# Footer
# -----------------------------------------------------
st.divider()
st.caption("© 2026 FBC Urban Systems – AI for Next Generation Cities")
