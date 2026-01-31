# ============================================================
# FBC DIGITAL SYSTEMS
# Project III – Security Ledger
# File: secure_vault.py
#
# Description:
# Immutable, deterministic, audit-grade security ledger
# for sector, city, and planetary financial records.
#
# Version: v7.0.0
# Status: Production / CI / Audit / IPO Grade
# ============================================================

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# ============================================================
# CONSTANTS
# ============================================================
VAULT_VERSION = "SECURE-VAULT-v7.0.0"
LEDGER_SCHEMA_VERSION = "LEDGER-SCHEMA-v2"
PROTOCOL = "FBC-SHA256-IMMUTABLE-AUDIT"

DEFAULT_SALT = "FBC_GLOBAL_RESERVE_IMMUTABLE_CORE"

# ============================================================
# DATA MODELS
# ============================================================
@dataclass(frozen=True)
class LedgerBlock:
    index: int
    timestamp: str
    schema: str
    project_id: str
    node: str
    amount: float
    protocol: str
    previous_hash: str
    vault_version: str
    audit_hash: str
    status: str


# ============================================================
# CORE VAULT
# ============================================================
class FBCSecureVault:
    """
    Immutable security ledger providing:
    - Deterministic hashing
    - Atomic persistence
    - Chain integrity guarantees
    - Backward-compatible public contracts
    """

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent

        self.ledger_file = base_path / "fbc_sector_ledger.json"
        self.global_ledger_path = (
            base_path.parents[1]
            / "Project_IV_City_OS"
            / "fbc_global_ledger.json"
        )

        self._salt = os.getenv("FBC_SECRET", DEFAULT_SALT)

        if not self.ledger_file.exists():
            self._initialize_genesis()

    # --------------------------------------------------------
    # GENESIS
    # --------------------------------------------------------
    def _initialize_genesis(self) -> None:
        genesis_payload = {
            "index": 0,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": "GENESIS",
            "node": "SECTOR_GENESIS",
            "amount": 0.0,
            "protocol": PROTOCOL,
            "previous_hash": "0" * 64,
            "vault_version": VAULT_VERSION
        }

        genesis_payload["audit_hash"] = self._canonical_hash(genesis_payload)
        genesis_payload["status"] = "GENESIS"

        self._atomic_save([genesis_payload])

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
        return self._sha256(canonical + self._salt)

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
        amount: float
    ) -> Dict[str, Any]:
        """
        Stable public API.
        Do not change signature without major version bump.
        """
        return self.generate_audit_proof(project_id, node_id, amount)

    def generate_audit_proof(
        self,
        project_id: str,
        node_id: str,
        amount: float
    ) -> Dict[str, Any]:

        if amount < 0:
            raise ValueError("Negative amounts are not permitted")

        ledger = self._load_ledger()
        last_block = ledger[-1]

        payload = {
            "index": last_block["index"] + 1,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": project_id,
            "node": node_id,
            "amount": float(amount),
            "protocol": PROTOCOL,
            "previous_hash": last_block["audit_hash"],
            "vault_version": VAULT_VERSION
        }

        payload["audit_hash"] = self._canonical_hash(payload)
        payload["status"] = "IMMUTABLE_RECORD"

        ledger.append(payload)
        self._atomic_save(ledger)

        self._mirror_global_ledger(payload)
        return payload

    # --------------------------------------------------------
    # GLOBAL MIRROR (BEST-EFFORT)
    # --------------------------------------------------------
    def _mirror_global_ledger(self, block: Dict[str, Any]) -> None:
        if not self.global_ledger_path.exists():
            return

        try:
            with open(self.global_ledger_path, "r", encoding="utf-8") as f:
                global_ledger = json.load(f)
        except Exception:
            return

        previous_hash = (
            global_ledger[-1]["audit_hash"]
            if global_ledger else "0" * 64
        )

        global_ledger.append({
            "index": len(global_ledger),
            "timestamp": block["timestamp"],
            "project_id": block["project_id"],
            "node": block["node"],
            "value": block["amount"],
            "protocol": block["protocol"],
            "previous_hash": previous_hash,
            "audit_hash": block["audit_hash"],
            "status": "MIRRORED"
        })

        try:
            with open(self.global_ledger_path, "w", encoding="utf-8") as f:
                json.dump(global_ledger, f, indent=2)
        except Exception:
            pass

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------
    def verify_sector_ledger(self) -> Dict[str, Any]:
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
            "status": "LEDGER_VERIFIED",
            "blocks": len(ledger),
            "vault_version": VAULT_VERSION,
            "schema_version": LEDGER_SCHEMA_VERSION
        }


# ============================================================
# LOCAL / CI TEST
# ============================================================
if __name__ == "__main__":
    vault = FBCSecureVault()
    vault.generate_proof("PROJECT_III", "AuditNode-01", 100.5)
    print(vault.verify_sector_ledger())
