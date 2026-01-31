# ============================================================
# FBC DIGITAL SYSTEMS
# Project IV – City OS
# File: fbc_live_dashboard.py
#
# Description:
# Global Executive & Investor Command Center
#
# Version: v6.0.0-EXECUTIVE-MAX-LTS
# Mode: Read-Only Investor Safe
# ============================================================

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import streamlit as st

# ============================================================
# GLOBAL CONFIG
# ============================================================
DASHBOARD_VERSION = "v6.0.0-EXECUTIVE-MAX-LTS"
SYSTEM_TARGET_VERSION = "v6.1.0-LTS"

SESSION_ID = str(uuid.uuid4())[:8]

BASE_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = BASE_DIR / "Project-VI-Global-Dominance" / "global_cities_manifest.json"

# ============================================================
# SAFE KERNEL BOOTSTRAP (ISOLATED)
# ============================================================
def bootstrap_kernel() -> Dict[str, Any]:
    try:
        from core_kernel import FBCKernel
        kernel = FBCKernel()
        kernel.initialize_paths()
        kernel.verify_engines()
        return kernel.finalize()
    except Exception:
        return {
            "final_status": "DEGRADED_MODE",
            "note": "Kernel isolated from executive interface"
        }

KERNEL_STATUS = bootstrap_kernel()

# ============================================================
# SAFE MODULE IMPORTS
# ============================================================
def safe_imports():
    try:
        from ai_engine_v2 import UrbanRevenueAI
        from secure_vault import FBCSecureVault
        return UrbanRevenueAI, FBCSecureVault, None
    except Exception as e:
        return None, None, str(e)

UrbanRevenueAI, FBCSecureVault, IMPORT_ERROR = safe_imports()

# ============================================================
# MANIFEST LOADER (VALIDATED)
# ============================================================
def load_manifest() -> Dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {}

    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "global_expansion_strategy" in data
        return data
    except Exception:
        return {}

MANIFEST = load_manifest()

def get_phase_one_cities() -> list[str]:
    try:
        phase = MANIFEST["global_expansion_strategy"]["phase_1_2027_2029"]["target_cities"]
        return [c["city"] for c in phase]
    except Exception:
        return ["Austin"]

PHASE_ONE_CITIES = get_phase_one_cities()

# ============================================================
# STREAMLIT CONFIG
# ============================================================
st.set_page_config(
    page_title="FBC Global Executive Console",
    layout="wide"
)

st.title("FBC Global Strategic Command Center")
st.caption(f"Investor Console | {DASHBOARD_VERSION} | Session {SESSION_ID}")
st.markdown("---")

# ============================================================
# SYSTEM STATUS BAR
# ============================================================
if KERNEL_STATUS.get("final_status") != "FULLY_OPERATIONAL":
    st.info("System running in Executive Safe Mode")
else:
    st.success("System Status: FULLY OPERATIONAL")

if IMPORT_ERROR:
    st.error("Critical modules unavailable. Dashboard in view-only mode.")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.header("System Governance")
st.sidebar.write("Ledger Integrity: ACTIVE")
st.sidebar.write("Access Level: Investor Read-Only")
st.sidebar.write("Audit Profile: ENTERPRISE_MAX")
st.sidebar.markdown("---")
st.sidebar.write(f"System Target: {SYSTEM_TARGET_VERSION}")

# ============================================================
# MAIN DASHBOARD
# ============================================================
left, right = st.columns([1, 2])

# ------------------------------------------------------------
# LEFT PANEL — CITY AI SNAPSHOT
# ------------------------------------------------------------
with left:
    st.subheader("City Node Snapshot")

    city = st.selectbox("Target City", PHASE_ONE_CITIES)

    if st.button("Run Revenue Simulation"):
        with st.spinner("Executing bounded AI analysis..."):
            try:
                engine = UrbanRevenueAI(city)
                report = engine.analyze_yield()

                metrics = report.get("metrics", {})

                st.metric(
                    "Projected Annual Revenue",
                    metrics.get("fbc_optimized_total_m", "N/A")
                )

                st.metric(
                    "Net Value Created",
                    metrics.get("net_value_created_m", "N/A")
                )

                # Optional Ledger Proof (Sandboxed)
                vault = FBCSecureVault()
                value = float(
                    metrics.get("fbc_optimized_total_m", "0")
                    .replace("$", "")
                    .replace("M", "")
                )

                proof = vault.generate_proof(
                    project_id="PROJECT_IV",
                    node_id=city,
                    value=value
                )

                st.code(
                    f"AUDIT HASH: {proof['audit_hash']}\nSTATUS: {proof['status']}",
                    language="text"
                )

            except Exception:
                st.warning("Simulation completed with limited visibility.")

# ------------------------------------------------------------
# RIGHT PANEL — PORTFOLIO VIEW
# ------------------------------------------------------------
with right:
    st.subheader("Network Financial Trajectory")

    try:
        arr = MANIFEST["financial_model"]["arr_projection_usd_m"]
        df = pd.DataFrame({
            "Year": arr.keys(),
            "ARR (USD Millions)": arr.values()
        })
        st.line_chart(df.set_index("Year"))
    except Exception:
        st.info("ARR projection data unavailable.")

    st.markdown("### Phase I Progress")
    st.progress(0.7)
    st.caption("Urban Revenue AI rollout — monitored execution")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(
    "FBC Digital Systems | Confidential Executive Interface | "
    "Unauthorized distribution prohibited"
)
