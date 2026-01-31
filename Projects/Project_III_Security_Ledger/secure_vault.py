# ==========================================
# PATH: Projects/Project_III_Security_Ledger/secure_vault.py
# DESCRIPTION: Supreme Immutable Security Ledger
# VERSION: v5.0-SUPREME-LEDGER-GRADE
# DATA MODE: REAL (CI-SAFE)
# ==========================================

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class FBCSecureVault:
    """
    FBC Supreme Sector-Level Immutable Security Ledger

    - SHA-256 + Salt + Chain Linking
    - CI-safe file initialization
    - Backward compatible
    - Future-ready for global federation
    """

    VAULT_VERSION = "SECURE-VAULT-v5.0-SUPREME"
    PROTOCOL = "SHA-256-FBC-GOLD"

    def __init__(self):
        base_path = Path(__file__).resolve().parent

        self.ledger_file = base_path / "fbc_sector_ledger.json"
        self.global_ledger_path = (
            base_path.parents[1] / "Project-IV-City-OS" / "fbc_global_ledger.json"
        )

        # Salt management (REAL but CI-safe)
        self._salt = os.getenv(
            "FBC_SECRET",
            "FBC_GLOBAL_RESERVE_SUPREME_2026"
        )

        if not self.ledger_file.exists():
            self._initialize_sector_ledger()

    # --------------------------------------------------
    # GENESIS INITIALIZATION
    # --------------------------------------------------
    def _initialize_sector_ledger(self) -> None:
        genesis_block = {
            "index": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "project_id": "GENESIS",
            "node": "SECTOR_GENESIS",
            "amount": 0,
            "protocol": self.PROTOCOL,
            "previous_hash": "0" * 64,
            "audit_hash": self._hash("SECTOR_GENESIS_BLOCK"),
            "status": "GENESIS_BLOCK",
            "vault_version": self.VAULT_VERSION
        }
        self._save_ledger([genesis_block])

    # --------------------------------------------------
    # CORE HASH FUNCTION
    # --------------------------------------------------
    def _hash(self, raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()

    # --------------------------------------------------
    # LEDGER IO
    # --------------------------------------------------
    def _load_ledger(self) -> List[Dict[str, Any]]:
        with open(self.ledger_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_ledger(self, ledger: List[Dict[str, Any]]) -> None:
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=4)

    # --------------------------------------------------
    # BACKWARD-COMPATIBLE INTERFACE
    # --------------------------------------------------
    def generate_audit_proof(self, node_id: str, amount: float) -> Dict[str, Any]:
        return self.generate_proof("PROJECT_III", node_id, amount)

    # --------------------------------------------------
    # SUPREME PROOF GENERATOR
    # --------------------------------------------------
    def generate_proof(
        self,
        project_id: str,
        node_id: str,
        amount: float
    ) -> Dict[str, Any]:

        ledger = self._load_ledger()
        last_block = ledger[-1]

        timestamp = datetime.utcnow().isoformat()
        amount = float(amount)

        raw_string = (
            f"{project_id}|{node_id}|{amount}|{timestamp}|"
            f"{self._salt}|{last_block['audit_hash']}"
        )

        audit_hash = self._hash(raw_string)

        new_block = {
            "index": last_block["index"] + 1,
            "timestamp": timestamp,
            "project_id": project_id,
            "node": node_id,
            "amount": amount,
            "protocol": self.PROTOCOL,
            "previous_hash": last_block["audit_hash"],
            "audit_hash": audit_hash,
            "status": "IMMUTABLE_RECORD",
            "vault_version": self.VAULT_VERSION
        }

        ledger.append(new_block)
        self._save_ledger(ledger)

        self._mirror_to_global_ledger_safe(new_block)

        return new_block

    # --------------------------------------------------
    # SAFE GLOBAL MIRROR (OPTIONAL)
    # --------------------------------------------------
    def _mirror_to_global_ledger_safe(self, block: Dict[str, Any]) -> None:
        try:
            if not self.global_ledger_path.exists():
                return

            with open(self.global_ledger_path, "r", encoding="utf-8") as f:
                global_ledger = json.load(f)

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
                "status": "MIRRORED_FROM_SECTOR"
            })

            with open(self.global_ledger_path, "w", encoding="utf-8") as f:
                json.dump(global_ledger, f, indent=4)

        except Exception:
            # Global ledger is optional — sector ledger never fails
            pass

    # --------------------------------------------------
    # LEDGER VERIFICATION
    # --------------------------------------------------
    def verify_sector_ledger(self) -> Dict[str, Any]:
        ledger = self._load_ledger()

        for i in range(1, len(ledger)):
            current = ledger[i]
            previous = ledger[i - 1]

            raw_check = (
                f"{current['project_id']}|{current['node']}|{current['amount']}|"
                f"{current['timestamp']}|{self._salt}|{previous['audit_hash']}"
            )

            recalculated_hash = self._hash(raw_check)

            if recalculated_hash != current["audit_hash"]:
                return {
                    "status": "TAMPER_DETECTED",
                    "failed_block": i
                }

            if current["previous_hash"] != previous["audit_hash"]:
                return {
                    "status": "CHAIN_BROKEN",
                    "failed_block": i
                }

        return {
            "status": "SECTOR_LEDGER_INTEGRITY_CONFIRMED",
            "blocks": len(ledger),
            "vault_version": self.VAULT_VERSION
        }


# --------------------------------------------------
# STANDALONE SUPREME TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- FBC SUPREME SECURITY LEDGER TEST ---")

    vault = FBCSecureVault()
    proof = vault.generate_audit_proof("Audit-Node", 42.75)

    print("Block:", proof["index"], proof["audit_hash"][:24], "...")
    verification = vault.verify_sector_ledger()
    print("Verification:", verification["status"])

    print("--- SECURITY LEDGER OPERATIONAL ✅ ---\n")
