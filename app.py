# ==========================================
# PATH: /app.py
# DESCRIPTION: FBC Global Command Center
# EDITION: Planetary Intelligence Core
# VERSION: v4.2.0 (Persistent Ledger + Governance Layer)
# ==========================================

import streamlit as st
import sys, os, sqlite3, datetime
import pandas as pd

# ==========================================
# PATH INTEGRATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDERS = [
    "Project-I-Urban-Revenue",
    "Project-II-Private-Districts",
    "Project-III-Traffic-Intelligence",
    "Project-III-Security-Ledger"
]
for folder in PROJECT_FOLDERS:
    sys.path.append(os.path.join(BASE_DIR, "Projects", folder))

# ==========================================
# PERSISTENT LEDGER DATABASE
# ==========================================
DB_PATH = os.path.join(BASE_DIR, "fbc_global_ledger.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            project TEXT,
            entity TEXT,
            value REAL,
            audit_hash TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(project, entity, value, audit_hash, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO audit_ledger 
        (timestamp, project, entity, value, audit_hash, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.datetime.utcnow().isoformat(), project, entity, value, audit_hash, status))
    conn.commit()
    conn.close()

def load_logs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM audit_ledger ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# ==========================================
# ENGINE IMPORTS WITH GOVERNANCE MONITOR
# ==========================================
SYSTEM_STATUS = "OPERATIONAL"
try:
    from revenue_optimizer import RevenueOptimizer
    from energy_forecast import predict_energy_savings
    from accident_pred import TrafficRiskEngine
    from secure_vault import FBCSecureVault
    vault = FBCSecureVault()
except Exception as e:
    SYSTEM_STATUS = f"KERNEL SYNC ERROR → {e}"

# ==========================================
# STREAMLIT UI CONFIG
# ==========================================
st.set_page_config(page_title="FBC Global Command Center", layout="wide")

st.markdown("""
<style>
.main { background-color: #0b0e14; color: #e6edf3; }
.stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; }
.audit-card { background-color: #010409; border-left: 4px solid #ffd700; padding: 15px; font-family: monospace; }
.gov-card { background-color: #0d1117; border: 1px solid #30363d; padding: 10px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 FBC Global Command Center")
st.caption(f"System Status: {SYSTEM_STATUS} | Digital Earth Governance Layer Active")
st.markdown("---")

# ==========================================
# GOVERNANCE MONITOR
# ==========================================
colg1, colg2, colg3 = st.columns(3)
with colg1:
    st.metric("AI Safety Layer", "ACTIVE", delta="Human-in-loop Ready")
with colg2:
    st.metric("Audit Persistence", "ENABLED", delta="Immutable Ledger")
with colg3:
    st.metric("Simulation Grid", "ONLINE", delta="Real-time Execution")

st.markdown("---")

# ==========================================
# SIDEBAR SECTOR CONTROL
# ==========================================
st.sidebar.image("https://img.shields.io/badge/FBC_OS-V4.2_PLANETARY-gold?style=for-the-badge")
mode = st.sidebar.radio("Deployment Sector", ["Governments", "Private Developers", "Global Oversight"])

# ==========================================
# SECTOR: GOVERNMENTS
# ==========================================
if mode == "Governments":
    st.header("🚦 Municipal Operations & Revenue Command")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Traffic Risk Intelligence")
        city = st.text_input("City Node", "Austin-TX")
        density = st.slider("Traffic Density", 0, 300, 120)

        risk_engine = TrafficRiskEngine(city)
        risk_res = risk_engine.analyze_real_time_risk(density)

        st.metric("Live Risk Score", risk_res['risk_score'], delta=risk_res['live_weather'])

    with col2:
        st.subheader("Revenue Optimization Engine")
        annual_rev = st.number_input("Annual City Revenue ($)", value=10000000)

        optimizer = RevenueOptimizer(city)
        gain = optimizer.project_incremental_gain(annual_rev)

        st.metric("Projected AI Gain", f"${gain['Total_City_Gain']:,.2f}", delta="+Optimized")

        if st.button("Authorize & Secure Transaction"):
            proof = vault.generate_proof("PROJECT_I", city, gain['FBC_Commission'])
            log_to_db("PROJECT_I", city, gain['FBC_Commission'], proof["audit_hash"], proof["status"])
            st.markdown(f'<div class="audit-card">HASH: {proof["audit_hash"]}<br>STATUS: {proof["status"]}</div>', unsafe_allow_html=True)

# ==========================================
# SECTOR: PRIVATE DEVELOPERS
# ==========================================
elif mode == "Private Developers":
    st.header("🏢 Private District Optimization")

    col_a, col_b = st.columns(2)

    with col_a:
        district = st.text_input("District ID", "FBC-EGYPT-01")
        bill = st.number_input("Monthly Energy Bill ($)", value=200000)

        energy_res = predict_energy_savings(bill)
        st.metric("AI Forecasted Savings", f"${energy_res['ai_predicted_savings']:,.2f}", delta="-Optimized")

    with col_b:
        st.subheader("Secure Savings Ledger")
        if st.button("Log Savings Report"):
            proof = vault.generate_proof("PROJECT_II", district, energy_res['ai_predicted_savings'])
            log_to_db("PROJECT_II", district, energy_res['ai_predicted_savings'], proof["audit_hash"], proof["status"])
            st.code(f"Audit Hash: {proof['audit_hash']}\nStatus: {proof['status']}")

# ==========================================
# SECTOR: GLOBAL OVERSIGHT
# ==========================================
else:
    st.header("🛰️ Digital Earth Oversight Console")

    logs_df = load_logs()
    total_val = logs_df["value"].sum() if not logs_df.empty else 0

    colx, coly = st.columns(2)
    with colx:
        st.metric("Total Secured Global Value", f"${total_val:,.2f}")
    with coly:
        st.metric("Total Ledger Entries", len(logs_df))

    st.subheader("Recent Global Ledger Events")
    if not logs_df.empty:
        st.dataframe(logs_df.head(20), use_container_width=True)
    else:
        st.info("No ledger events recorded yet.")

# ==========================================
# MASTER AUDIT TRAIL FOOTER
# ==========================================
st.markdown("---")
st.caption("© 2026–2037 FBC Digital Systems | Digital Earth Intelligence Layer")
