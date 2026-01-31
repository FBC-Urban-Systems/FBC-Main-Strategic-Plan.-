# ============================================================
# FBC DIGITAL SYSTEMS
# Project III – Security Ledger
# File: secure_vault.py
#
# DESCRIPTION:
# Enterprise-grade immutable security ledger
# with deterministic hashing and audit verification.
#
# VERSION: v5.0.0-ENTERPRISE-LTS
# ============================================================

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

# ============================================================
# ENTERPRISE CONSTANTS
# ============================================================
VAULT_VERSION = "5.0.0-ENTERPRISE-LTS"
LEDGER_SCHEMA_VERSION = "LEDGER-SCHEMA-v2"
PROTOCOL = "FBC-SHA256-IMMUTABLE-AUDIT"
DEFAULT_SALT = "FBC_GLOBAL_RESERVE_IMMUTABLE_CORE"


# ============================================================
# CORE VAULT
# ============================================================
class FBCSecureVault:
    """
    Enterprise LTS immutable security ledger.

    Guarantees:
    - Deterministic hashing
    - Atomic persistence
    - Chain integrity
    - Backward-compatible public API
    """

    def __init__(self, base_path: Path | None = None) -> None:
        root = base_path or Path(__file__).resolve().parent

        self._ledger_path = root / "fbc_sector_ledger.json"
        self._salt = os.getenv("FBC_SECRET", DEFAULT_SALT)

        if not self._ledger_path.exists():
            self._initialize_genesis()

    # --------------------------------------------------------
    # GENESIS
    # --------------------------------------------------------
    def _initialize_genesis(self) -> None:
        genesis = {
            "index": 0,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": "GENESIS",
            "node": "SECTOR_GENESIS",
            "amount": 0.0,
            "protocol": PROTOCOL,
            "previous_hash": "0" * 64,
            "vault_version": VAULT_VERSION,
        }

        genesis["audit_hash"] = self._canonical_hash(genesis)
        genesis["status"] = "GENESIS"

        self._atomic_save([genesis])

    # --------------------------------------------------------
    # TIME & HASHING
    # --------------------------------------------------------
    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    @staticmethod
    def _sha256(raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _canonical_hash(self, payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return self._sha256(canonical + self._salt)

    # --------------------------------------------------------
    # LEDGER IO
    # --------------------------------------------------------
    def _load_ledger(self) -> List[Dict[str, Any]]:
        with open(self._ledger_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _atomic_save(self, ledger: List[Dict[str, Any]]) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self._ledger_path.parent,
            delete=False,
        ) as tmp:
            json.dump(ledger, tmp, indent=2)
            tmp_name = tmp.name

        os.replace(tmp_name, self._ledger_path)

    # --------------------------------------------------------
    # PUBLIC CONTRACT (LTS — DO NOT BREAK)
    # --------------------------------------------------------
    def generate_proof(
        self,
        project_id: str,
        node_id: str,
        amount: float,
    ) -> Dict[str, Any]:
        """
        Stable public API.
        Signature frozen under Enterprise LTS.
        """
        if amount < 0:
            raise ValueError("Negative amounts are not permitted")

        ledger = self._load_ledger()
        last = ledger[-1]

        record = {
            "index": last["index"] + 1,
            "timestamp": self._now(),
            "schema": LEDGER_SCHEMA_VERSION,
            "project_id": project_id,
            "node": node_id,
            "amount": float(amount),
            "protocol": PROTOCOL,
            "previous_hash": last["audit_hash"],
            "vault_version": VAULT_VERSION,
        }

        record["audit_hash"] = self._canonical_hash(record)
        record["status"] = "IMMUTABLE_RECORD"

        ledger.append(record)
        self._atomic_save(ledger)

        return record

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------
    def verify_sector_ledger(self) -> Dict[str, Any]:
        ledger = self._load_ledger()

        for i in range(1, len(ledger)):
            current = ledger[i]
            previous = ledger[i - 1]

            recalculated = self._canonical_hash(
                {k: current[k] for k in current if k not in {"audit_hash", "status"}}
            )

            if recalculated != current["audit_hash"]:
                return {"status": "TAMPER_DETECTED", "block_index": i}

            if current["previous_hash"] != previous["audit_hash"]:
                return {"status": "CHAIN_BROKEN", "block_index": i}

        return {
            "status": "LEDGER_VERIFIED",
            "blocks": len(ledger),
            "vault_version": VAULT_VERSION,
            "schema_version": LEDGER_SCHEMA_VERSION,
        }
