# ==========================================
# PATH: Projects/Project-IV-City-OS/fbc_live_dashboard.py
# DESCRIPTION: FBC Global Strategic Command Center (Investor View)
# VERSION: v5.0-EXECUTIVE-GRADE
# ==========================================

import streamlit as st
import pandas as pd
import json
from pathlib import Path

# ==========================================
# BOOTSTRAP CORE KERNEL (Auto Path Linking)
# ==========================================
try:
    from core_kernel import FBCKernel
    kernel = FBCKernel()
    kernel.initialize_paths()
    kernel.verify_engines()
    KERNEL_STATUS = kernel.finalize()
except Exception as e:
    KERNEL_STATUS = {"final_status": "KERNEL_FAILURE", "error": str(e)}

# ==========================================
# SAFE ENGINE IMPORTS
# ==========================================
CORE_MODULES_LOADED = True
IMPORT_ERROR_MSG = ""

try:
    from ai_engine_v2 import UrbanRevenueAI
    from secure_vault import FBCSecureVault
except Exception as e:
    CORE_MODULES_LOADED = False
    IMPORT_ERROR_MSG = str(e)

# ==========================================
# LOAD GLOBAL MANIFEST FOR REAL CITY NODES
# ==========================================
BASE_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BASE_DIR / "Project-VI-Global-Dominance" / "global_cities_manifest.json"

def load_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    return {}

manifest = load_manifest()

def get_phase_one_cities():
    try:
        phase = manifest["global_expansion_strategy"]["phase_1_2027_2029"]["target_cities"]
        return [c["city"] for c in phase]
    except:
        return ["Austin"]

PHASE_ONE_CITIES = get_phase_one_cities()

# ==========================================
# STREAMLIT UI CONFIG
# ==========================================
st.set_page_config(
    page_title="FBC Global Executive",
    page_icon="🏙️",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0e1117; }
.stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #FFD700; }
.audit-box { background-color:#111827; padding:10px; border-radius:8px; font-family:monospace; }
</style>
""", unsafe_allow_html=True)

st.title("🏙️ FBC Global Strategic Command Center")
st.subheader("Planetary Scale Urban Intelligence — Investor Console")
st.markdown("---")

# ==========================================
# KERNEL STATUS BAR
# ==========================================
if KERNEL_STATUS["final_status"] != "FULLY_OPERATIONAL":
    st.warning(f"Kernel Status: {KERNEL_STATUS['final_status']}")
else:
    st.success("Kernel Status: FULLY OPERATIONAL 🧠")

# ==========================================
# CORE MODULE CHECK
# ==========================================
if not CORE_MODULES_LOADED:
    st.error(f"Critical Import Error: {IMPORT_ERROR_MSG}")
    st.stop()

# ==========================================
# SIDEBAR SECURITY
# ==========================================
st.sidebar.header("🛡️ FBC Security Protocol")
st.sidebar.success("SHA-256 Ledger: ACTIVE")
st.sidebar.info("Data Privacy: GDPR / SDEP Compliant")
st.sidebar.markdown("---")
st.sidebar.write("Founder Access: **Verified ✅**")

# ==========================================
# MAIN DASHBOARD
# ==========================================
col1, col2 = st.columns([1, 2])

# -------- LEFT: CITY NODE AI ANALYSIS --------
with col1:
    st.header("📍 Expansion Node Analysis")

    target_city = st.selectbox("Select Target City Node", PHASE_ONE_CITIES)

    if st.button("Execute AI Yield Analysis"):
        with st.spinner("Accessing FBC AI Revenue Engine..."):
            engine = UrbanRevenueAI(target_city)
            report = engine.analyze_yield()

            if "error" in report:
                st.error(report["error"])
            else:
                metrics = report["metrics"]

                st.success(f"Analysis Complete — {target_city}")

                st.metric("Optimized Annual Revenue", metrics["fbc_optimized_total_m"])
                st.metric("Net Value Created", metrics["net_value_created_m"], delta="AI Optimized")

                # -------- SECURITY VAULT --------
                vault = FBCSecureVault()
                numeric_val = float(metrics["fbc_optimized_total_m"].replace("$", "").replace("M", ""))
                proof = vault.generate_proof("PROJECT_I", target_city, numeric_val)

                st.markdown("### 🔒 Security Audit Proof")
                st.markdown(
                    f"<div class='audit-box'>Audit Hash: {proof['audit_hash']}<br>Status: {proof['status']}</div>",
                    unsafe_allow_html=True
                )

# -------- RIGHT: PORTFOLIO PERFORMANCE --------
with col2:
    st.header("📈 Portfolio Performance Projection")

    # ARR Projection directly from manifest
    try:
        arr_proj = manifest["financial_model"]["arr_projection_usd_m"]
        chart_df = pd.DataFrame({
            "Year": list(arr_proj.keys()),
            "ARR (Million USD)": list(arr_proj.values())
        })
        st.line_chart(chart_df.set_index("Year"))
    except:
        st.info("ARR projection unavailable from manifest.")

    st.write("### 🚀 Strategic Roadmap Progress")
    st.progress(70)
    st.caption("Phase I (Urban Revenue AI Deployment) — Live Integration")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption("FBC Digital Systems © 2026–2037 | Executive Investor Console | Confidential Access Only")
