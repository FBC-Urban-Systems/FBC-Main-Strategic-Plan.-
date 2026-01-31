# =========================================================
# PATH: /data_core.py
# DESCRIPTION: Unified Global Data Core
# VERSION: v2.0.0 — REAL DATA LOCKED • AUDIT GRADE
# ROLE: Immutable Single Source of Truth for All Simulations
# =========================================================

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple

# =========================================================
# DATABASE CONFIGURATION
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fbc_data_core.db")


# =========================================================
# DATABASE INITIALIZATION
# =========================================================
def init_data_core() -> None:
    """
    Initializes the global data core schema.
    Safe to call multiple times (idempotent).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                city TEXT NOT NULL,
                revenue_gain REAL NOT NULL,
                energy_savings REAL NOT NULL,
                risk_score REAL NOT NULL
            )
        """)
        conn.commit()


# =========================================================
# WRITE OPERATIONS (ATOMIC)
# =========================================================
def store_simulation_result(
    city: str,
    revenue_gain: float,
    energy_savings: float,
    risk_score: float
) -> None:
    """
    Persists a single simulation record atomically.
    """

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO simulation_results
            (timestamp, city, revenue_gain, energy_savings, risk_score)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat() + "Z",
                city,
                float(revenue_gain),
                float(energy_savings),
                float(risk_score),
            )
        )
        conn.commit()


# =========================================================
# READ OPERATIONS
# =========================================================
def fetch_all_results() -> List[Tuple]:
    """
    Returns all simulation records ordered by newest first.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM simulation_results ORDER BY id DESC"
        )
        return cursor.fetchall()


def fetch_results_as_dict() -> List[Dict]:
    """
    Returns all simulation records as structured dictionaries.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM simulation_results ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


# =========================================================
# BOOTSTRAP ON IMPORT
# =========================================================
init_data_core()
