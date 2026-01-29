# ==========================================
# PATH: /data_core.py
# DESCRIPTION: Unified Global Data Core
# VERSION: v1.0.0
# ROLE: Single Source of Truth for all FBC Data
# ==========================================

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "fbc_data_core.db")

def init_data_core():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            city TEXT,
            revenue_gain REAL,
            energy_savings REAL,
            risk_score REAL
        )
    """)
    conn.commit()
    conn.close()

def store_simulation_result(city, revenue_gain, energy_savings, risk_score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO simulation_results
        (timestamp, city, revenue_gain, energy_savings, risk_score)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.utcnow().isoformat(), city, revenue_gain, energy_savings, risk_score))
    conn.commit()
    conn.close()

def fetch_all_results():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM simulation_results ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# Initialize on import
init_data_core()
