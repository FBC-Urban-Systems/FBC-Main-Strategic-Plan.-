# ============================================================
# FBC DIGITAL SYSTEMS
# Project VI – Planetary Urban Data Exchange
# File: global_expansion_sim.py
#
# Description:
# Deterministic planetary-scale expansion, ARR, and valuation
# simulation engine aligned with the official FBC Strategic Plan.
#
# Version: v7.0.0
# Status: Production / Audit / IPO Grade
# ============================================================

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "global_cities_manifest.json"

LOG_LEVEL = logging.INFO
DEFAULT_VALUATION_MULTIPLE = 25
MIN_VALUATION_MULTIPLE = 22
MAX_VALUATION_MULTIPLE = 28

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ============================================================
# EXCEPTIONS
# ============================================================
class ManifestLoadError(Exception):
    pass


class ManifestSchemaError(Exception):
    pass


# ============================================================
# DATA MODELS
# ============================================================
@dataclass(frozen=True)
class FinancialModel:
    arr_projection_usd_m: Dict[str, float]
    valuation_targets_usd_b: Dict[str, float]


@dataclass(frozen=True)
class ExpansionStrategy:
    phase_1_2027_2029: List[str]
    phase_2_2030_2031: List[str]
    phase_3_2032_2034: List[str]


# ============================================================
# CORE SIMULATION ENGINE
# ============================================================
class FBCPlanetaryGrowthEngine:
    """
    Planetary-scale simulation engine for:
    - Global expansion cadence
    - ARR growth tracking
    - IPO-grade valuation modeling
    """

    def __init__(self, valuation_multiple: int = DEFAULT_VALUATION_MULTIPLE):
        self.manifest = self._load_and_validate_manifest()
        self.financial_model = self._load_financial_model()
        self.expansion_strategy = self._load_expansion_strategy()

        self.target_cities_final = int(
            self.manifest["digital_earth_layer"]
            ["network_scale_targets"]
            ["cities_connected"]
        )

        if not MIN_VALUATION_MULTIPLE <= valuation_multiple <= MAX_VALUATION_MULTIPLE:
            raise ValueError("Valuation multiple outside realistic SaaS bounds.")

        self.valuation_multiple = valuation_multiple

        logging.info("Planetary Growth Engine initialized.")

    # --------------------------------------------------------
    # MANIFEST HANDLING
    # --------------------------------------------------------
    def _load_and_validate_manifest(self) -> dict:
        if not MANIFEST_PATH.exists():
            raise ManifestLoadError("Global cities manifest not found.")

        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        required_sections = {
            "financial_model",
            "global_expansion_strategy",
            "digital_earth_layer"
        }

        missing = required_sections - manifest.keys()
        if missing:
            raise ManifestSchemaError(
                f"Manifest missing required sections: {sorted(missing)}"
            )

        return manifest

    def _load_financial_model(self) -> FinancialModel:
        fm = self.manifest["financial_model"]

        return FinancialModel(
            arr_projection_usd_m=fm["arr_projection_usd_m"],
            valuation_targets_usd_b=fm["valuation_targets_usd_b"]
        )

    def _load_expansion_strategy(self) -> ExpansionStrategy:
        gs = self.manifest["global_expansion_strategy"]

        return ExpansionStrategy(
            phase_1_2027_2029=gs["phase_1_2027_2029"]["target_cities"],
            phase_2_2030_2031=gs["phase_2_2030_2031"]["target_cities"],
            phase_3_2032_2034=gs["phase_3_2032_2034"]["target_cities"]
        )

    # --------------------------------------------------------
    # SIMULATION LOGIC
    # --------------------------------------------------------
    def run_simulation(self) -> pd.DataFrame:
        logging.info("Starting global expansion simulation.")

        active_cities = 0
        results = []

        for year in range(2027, 2038):
            new_cities = self._calculate_new_cities(year)
            active_cities = min(
                active_cities + new_cities,
                self.target_cities_final
            )

            arr_value = self._resolve_arr(year)
            valuation = (arr_value * self.valuation_multiple) / 1000

            results.append({
                "year": year,
                "new_cities_added": new_cities,
                "active_cities": active_cities,
                "arr_usd_m": round(arr_value, 2),
                "valuation_multiple": self.valuation_multiple,
                "estimated_valuation_usd_b": round(valuation, 2)
            })

        logging.info("Simulation completed.")
        return pd.DataFrame(results)

    def _calculate_new_cities(self, year: int) -> int:
        if year <= 2029:
            return max(1, len(self.expansion_strategy.phase_1_2027_2029) // 3)
        if year <= 2031:
            return max(1, len(self.expansion_strategy.phase_2_2030_2031) // 2)
        if year <= 2034:
            return max(1, len(self.expansion_strategy.phase_3_2032_2034) // 3)

        remaining_years = 2037 - year + 1
        return max(1, self.target_cities_final // (remaining_years * 4))

    def _resolve_arr(self, year: int) -> float:
        key = str(year)
        if key in self.financial_model.arr_projection_usd_m:
            return self.financial_model.arr_projection_usd_m[key]

        latest_year = max(self.financial_model.arr_projection_usd_m.keys())
        return self.financial_model.arr_projection_usd_m[latest_year]

    # --------------------------------------------------------
    # EXECUTIVE REPORT
    # --------------------------------------------------------
    def generate_executive_report(self, df: pd.DataFrame) -> dict:
        final_row = df.iloc[-1]
        target_valuation = self.financial_model.valuation_targets_usd_b["ipo_2037"]

        status = (
            "GOAL REACHED"
            if final_row["estimated_valuation_usd_b"] >= target_valuation
            else "ADDITIONAL EXPANSION REQUIRED"
        )

        return {
            "simulation_timestamp_utc": datetime.utcnow().isoformat(),
            "final_year": int(final_row["year"]),
            "final_active_cities": int(final_row["active_cities"]),
            "final_arr_usd_m": float(final_row["arr_usd_m"]),
            "final_estimated_valuation_usd_b": float(
                final_row["estimated_valuation_usd_b"]
            ),
            "target_valuation_usd_b": target_valuation,
            "status": status
        }


# ============================================================
# CLI ENTRYPOINT
# ============================================================
if __name__ == "__main__":
    engine = FBCPlanetaryGrowthEngine()
    df = engine.run_simulation()
    report = engine.generate_executive_report(df)

    print("\nFBC PLANETARY EXPANSION SIMULATION v7.0.0\n")
    print(df.to_string(index=False))
    print("\nEXECUTIVE SUMMARY\n")
    for key, value in report.items():
        print(f"{key}: {value}")
