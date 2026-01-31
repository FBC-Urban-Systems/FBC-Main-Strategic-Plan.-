# ============================================================
# FBC DIGITAL SYSTEMS
# Project IV – City OS
# File: secure_vault.py
#
# Description:
# Global immutable security ledger anchoring all city,
# sector, and planetary financial records.
#
# Version: v8.0.0-GLOBAL-LTS
# Status: Enterprise / Audit / CI / IPO Grade
# ============================================================

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# ============================================================
# GLOBAL CONSTANTS
# ============================================================
GLOBAL_LEDGER_VERSION = "GLOBAL-LEDGER-v8.0.0-LTS"
LEDGER_SCHEMA_VERSION = "GLOBAL-SCHEMA-v3"
PROTOCOL = "FBC-SHA256-GLOBAL-IMMUTABLE"

DEFAULT_PEPPER = "FBC_GLOBAL_LEDGER_CORE"

# ============================================================
# GLOBAL LEDGER VAULT
# ============================================================
class FBCSecureVault:
    """
    Global immutable ledger providing:
    - Deterministic hashing
    - Atomic persistence
    - Chain integrity guarantees
    - Long-term backward compatibility
    """

    def __init__(self) -> None:
        self.ledger_id = "FBC-GLOBAL-LEDGER-001"
        self._pepper = os.getenv("FBC_GLOBAL_SECRET", DEFAULT_PEPPER)

        self.ledger_file = (
            Path(__file__).resolve().parent / "fbc_global_ledger.json"
        )

        if not self.ledger_file.exists():
            self._initialize_genesis()

    # --------------------------------------------------------
    # GENESIS BLOCK
    # --------------------------------------------------------
    def _initialize_genesis(self) -> None:
        genesis = {
            "index": 0,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": "GENESIS",
            "node": "GLOBAL_GENESIS",
            "value": 0.0,
            "protocol": PROTOCOL,
            "previous_hash": "0" * 64,
            "ledger_version": GLOBAL_LEDGER_VERSION,
        }

        genesis["audit_hash"] = self._canonical_hash(genesis)
        genesis["status"] = "GENESIS"

        self._atomic_save([genesis])

    # --------------------------------------------------------
    # TIME & HASHING
    # --------------------------------------------------------
    @staticmethod
    def _now() -> str:
        return datetime.utcnow().isoformat(timespec="seconds")

    @staticmethod
    def _sha256(raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _canonical_hash(self, payload: Dict[str, Any]) -> str:
        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        )
        return self._sha256(canonical + self._pepper)

    # --------------------------------------------------------
    # LEDGER IO
    # --------------------------------------------------------
    def _load_ledger(self) -> List[Dict[str, Any]]:
        with open(self.ledger_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _atomic_save(self, ledger: List[Dict[str, Any]]) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.ledger_file.parent,
            delete=False
        ) as tmp:
            json.dump(ledger, tmp, indent=2)
            temp_name = tmp.name

        os.replace(temp_name, self.ledger_file)

    # --------------------------------------------------------
    # PUBLIC CONTRACT (STABLE)
    # --------------------------------------------------------
    def generate_proof(
        self,
        project_id: str,
        node_id: str,
        value: float
    ) -> Dict[str, Any]:
        """
        Stable public API.
        Guaranteed backward compatible.
        """

        if value < 0:
            raise ValueError("Negative values are not permitted")

        ledger = self._load_ledger()
        last_block = ledger[-1]

        payload = {
            "index": last_block["index"] + 1,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": project_id,
            "node": node_id,
            "value": float(value),
            "protocol": PROTOCOL,
            "previous_hash": last_block["audit_hash"],
            "ledger_version": GLOBAL_LEDGER_VERSION,
        }

        payload["audit_hash"] = self._canonical_hash(payload)
        payload["status"] = "IMMUTABLE_RECORD"

        ledger.append(payload)
        self._atomic_save(ledger)

        return payload

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------
    def verify_global_ledger(self) -> Dict[str, Any]:
        ledger = self._load_ledger()

        for i in range(1, len(ledger)):
            current = ledger[i]
            previous = ledger[i - 1]

            recalculated = self._canonical_hash({
                k: current[k]
                for k in current
                if k not in {"audit_hash", "status"}
            })

            if recalculated != current["audit_hash"]:
                return {
                    "status": "TAMPER_DETECTED",
                    "block_index": i
                }

            if current["previous_hash"] != previous["audit_hash"]:
                return {
                    "status": "CHAIN_BROKEN",
                    "block_index": i
                }

        return {
            "status": "GLOBAL_LEDGER_VERIFIED",
            "blocks": len(ledger),
            "ledger_version": GLOBAL_LEDGER_VERSION,
            "schema_version": LEDGER_SCHEMA_VERSION,
        }


# ============================================================
# LOCAL / CI TEST
# ============================================================
if __name__ == "__main__":
    vault = FBCSecureVault()
    vault.generate_proof("PROJECT_IV", "City-OS-Core", 1_000_000)
    print(vault.verify_global_ledger())
