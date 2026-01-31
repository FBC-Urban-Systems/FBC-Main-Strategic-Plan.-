# ==========================================
# PATH: Projects/Project_III_Security_Ledger/secure_vault.py
# DESCRIPTION: Enterprise-Grade Immutable Security Ledger
# VERSION: v4.0.1-ENTERPRISE-IMMUTABLE-LEDGER
# DATA MODE: REAL (CI-SAFE / PROD-READY)
# ==========================================

import hashlib
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class FBCSecureVault:
    """
    Enterprise-Grade Immutable Security Ledger (Sector Level)

    Guarantees:
    - Backward-compatible public contracts
    - Deterministic immutable hashing
    - Atomic disk writes
    - Schema versioning
    - CI-safe & production-ready
    """

    VAULT_VERSION = "SECURE-VAULT-v4.0.1"
    LEDGER_SCHEMA_VERSION = "LEDGER-SCHEMA-v1"
    PROTOCOL = "FBC-SHA256-IMMUTABLE"

    def __init__(self) -> None:
        base_path = Path(__file__).resolve().parent

        self.ledger_file = base_path / "fbc_sector_ledger.json"
        self.global_ledger_path = (
            base_path.parents[1] / "Project_IV_City_OS" / "fbc_global_ledger.json"
        )

        self._salt = os.getenv(
            "FBC_SECRET",
            "FBC_GLOBAL_RESERVE_IMMUTABLE_CORE"
        )

        if not self.ledger_file.exists():
            self._initialize_genesis()

    # --------------------------------------------------
    # GENESIS BLOCK
    # --------------------------------------------------
    def _initialize_genesis(self) -> None:
        genesis = {
            "index": 0,
            "timestamp": self._now(),
            "schema": self.LEDGER_SCHEMA_VERSION,
            "project_id": "GENESIS",
            "node": "SECTOR_GENESIS",
            "amount": 0.0,
            "protocol": self.PROTOCOL,
            "previous_hash": "0" * 64,
            "audit_hash": self._hash("GENESIS"),
            "status": "GENESIS",
            "vault_version": self.VAULT_VERSION
        }
        self._atomic_save([genesis])

    # --------------------------------------------------
    # CORE UTILITIES
    # --------------------------------------------------
    @staticmethod
    def _now() -> str:
        return datetime.utcnow().isoformat(timespec="seconds")

    def _hash(self, raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _canonical_hash(self, payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return self._hash(canonical + self._salt)

    # --------------------------------------------------
    # LEDGER IO (ATOMIC)
    # --------------------------------------------------
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
            json.dump(ledger, tmp, indent=4)
            temp_name = tmp.name
        os.replace(temp_name, self.ledger_file)

    # --------------------------------------------------
    # PUBLIC CONTRACT (STABLE)
    # --------------------------------------------------
    def generate_proof(
        self,
        project_id: str,
        node_id: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Stable public API.
        Required by engine contracts & CI tests.
        """
        return self.generate_audit_proof(project_id, node_id, amount)

    def generate_audit_proof(
        self,
        project_id: str,
        node_id: str,
        amount: float
    ) -> Dict[str, Any]:

        if amount < 0:
            raise ValueError("Negative values are not permitted")

        ledger = self._load_ledger()
        last = ledger[-1]

        block = {
            "index": last["index"] + 1,
            "timestamp": self._now(),
            "schema": self.LEDGER_SCHEMA_VERSION,
            "project_id": project_id,
            "node": node_id,
            "amount": float(amount),
            "protocol": self.PROTOCOL,
            "previous_hash": last["audit_hash"],
            "vault_version": self.VAULT_VERSION
        }

        block["audit_hash"] = self._canonical_hash(block)
        block["status"] = "IMMUTABLE_RECORD"

        ledger.append(block)
        self._atomic_save(ledger)

        self._mirror_global_safe(block)
        return block

    # --------------------------------------------------
    # OPTIONAL GLOBAL MIRROR
    # --------------------------------------------------
    def _mirror_global_safe(self, block: Dict[str, Any]) -> None:
        if not self.global_ledger_path.exists():
            return

        try:
            with open(self.global_ledger_path, "r", encoding="utf-8") as f:
                global_ledger = json.load(f)
        except Exception:
            return

        previous_hash = global_ledger[-1]["audit_hash"] if global_ledger else "0" * 64

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
                json.dump(global_ledger, f, indent=4)
        except Exception:
            pass

    # --------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------
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
                return {"status": "TAMPER_DETECTED", "block": i}

            if current["previous_hash"] != previous["audit_hash"]:
                return {"status": "CHAIN_BROKEN", "block": i}

        return {
            "status": "LEDGER_VERIFIED",
            "blocks": len(ledger),
            "vault_version": self.VAULT_VERSION
        }


# --------------------------------------------------
# CI / LOCAL TEST
# --------------------------------------------------
if __name__ == "__main__":
    vault = FBCSecureVault()
    vault.generate_proof("PROJECT_III", "AuditNode-01", 100.5)
    print(vault.verify_sector_ledger())
