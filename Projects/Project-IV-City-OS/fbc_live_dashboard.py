import streamlit as st
import pandas as pd
import time

# FBC Branding
st.set_page_config(page_title="FBC Global Dashboard", layout="wide")
st.title("🏙️ FBC Digital Systems - Global Command Center")
st.sidebar.image("https://via.placeholder.com/150", caption="FBC Intelligence") # يمكن استبدالها بلوجو الشركة لاحقاً

# Sidebar Controls
st.sidebar.header("System Controls")
city_target = st.sidebar.slider("Expansion Target (Cities)", 1, 80, 5)

# 1. First Cities Data (The North America Fleet)
st.subheader("📍 Phase I: North America Deployment")
city_data = pd.DataFrame({
    'City': ['Austin', 'Toronto', 'New York (Private District)', 'Vancouver', 'Miami'],
    'Status': ['Active', 'Active', 'Operational', 'Standby', 'Pending'],
    'Revenue_Growth': [24.5, 18.2, 31.0, 0, 0]
})
st.table(city_data)

# 2. Live Financial Pulse
st.subheader("📊 Financial Real-time Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Target Valuation", "$35 Billion", "Phase III")
col2.metric("LTV/CAC Ratio", "42x", "Above Target")
col3.metric("Current ARR", f"${city_target * 10}M", "Projected")

# 3. Expansion Visualization
st.subheader("📈 Growth Trajectory")
chart_data = pd.DataFrame({
    'Year': range(2027, 2038),
    'Valuation_B': [1.2, 5.0, 8.5, 12.0, 15.5, 19.0, 22.5, 26.0, 29.5, 33.0, 35.0]
})
st.line_chart(chart_data.set_index('Year'))

st.success("System Status: Optimal. Ready for Seed Round Presentation.")
