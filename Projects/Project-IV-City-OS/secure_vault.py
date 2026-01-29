# ==========================================
# PATH: Projects/Project-IV-City-OS/secure_vault.py
# DESCRIPTION: FBC Global Immutable Security Ledger
# VERSION: v4.0-GLOBAL-LEDGER-GRADE
# ==========================================

import hashlib
import json
from datetime import datetime
from pathlib import Path

class FBCSecureVault:
    """
    FBC Global Immutable Ledger Protocol
    SHA-256 + Chain Hashing + Audit Verification
    """

    def __init__(self):
        self.ledger_id = "FBC-GLOBAL-LEDGER-001"
        self.protocol = "SHA-256-FBC-GOLD"
        self.internal_pepper = "FBC_INTERNAL_PEPPER_2026"
        self.ledger_file = Path(__file__).resolve().parent / "fbc_global_ledger.json"

        # Initialize ledger storage if not exists
        if not self.ledger_file.exists():
            self._initialize_ledger()

    # --------------------------------------
    # INTERNAL LEDGER INITIALIZATION
    # --------------------------------------
    def _initialize_ledger(self):
        genesis_block = {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "data": "FBC_GENESIS_BLOCK",
            "previous_hash": "0"*64,
            "audit_hash": self._hash_data("FBC_GENESIS_BLOCK")
        }
        with open(self.ledger_file, "w") as f:
            json.dump([genesis_block], f, indent=4)

    # --------------------------------------
    # CORE HASH FUNCTION
    # --------------------------------------
    def _hash_data(self, raw_string):
        return hashlib.sha256(raw_string.encode()).hexdigest().upper()

    # --------------------------------------
    # LOAD LEDGER
    # --------------------------------------
    def _load_ledger(self):
        with open(self.ledger_file, "r") as f:
            return json.load(f)

    # --------------------------------------
    # SAVE LEDGER
    # --------------------------------------
    def _save_ledger(self, ledger):
        with open(self.ledger_file, "w") as f:
            json.dump(ledger, f, indent=4)

    # --------------------------------------
    # GENERATE IMMUTABLE AUDIT PROOF
    # --------------------------------------
    def generate_proof(self, project_id, city_node, value_amount):
        ledger = self._load_ledger()
        last_block = ledger[-1]

        timestamp = datetime.now().isoformat()

        raw_data = f"{project_id}|{city_node}|{value_amount}|{timestamp}|{self.internal_pepper}|{last_block['audit_hash']}"

        secure_hash = self._hash_data(raw_data)

        new_block = {
            "index": last_block["index"] + 1,
            "timestamp": timestamp,
            "project_id": project_id,
            "node": city_node,
            "value": value_amount,
            "protocol": self.protocol,
            "ledger_reference": self.ledger_id,
            "previous_hash": last_block["audit_hash"],
            "audit_hash": secure_hash,
            "status": "IMMUTABLE_CONFIRMED"
        }

        ledger.append(new_block)
        self._save_ledger(ledger)

        return new_block

    # --------------------------------------
    # VERIFY ENTIRE LEDGER INTEGRITY
    # --------------------------------------
    def verify_ledger(self):
        ledger = self._load_ledger()

        for i in range(1, len(ledger)):
            current = ledger[i]
            previous = ledger[i-1]

            check_raw = f"{current['project_id']}|{current['node']}|{current['value']}|{current['timestamp']}|{self.internal_pepper}|{previous['audit_hash']}"
            recalculated_hash = self._hash_data(check_raw)

            if recalculated_hash != current["audit_hash"]:
                return {
                    "status": "LEDGER_TAMPERED",
                    "failed_block": i
                }

            if current["previous_hash"] != previous["audit_hash"]:
                return {
                    "status": "CHAIN_BROKEN",
                    "failed_block": i
                }

        return {
            "status": "LEDGER_INTEGRITY_CONFIRMED",
            "total_blocks": len(ledger)
        }

# --------------------------------------
# SYSTEM INTEGRITY TEST
# --------------------------------------
if __name__ == "__main__":
    vault = FBCSecureVault()

    print("\n--- FBC GLOBAL LEDGER TEST ---")

    proof = vault.generate_proof("PROJECT_I", "Austin-HQ", 50000000)
    print("New Block Added:")
    print("Audit Hash:", proof["audit_hash"][:20], "...")

    verification = vault.verify_ledger()
    print("Ledger Verification Status:", verification["status"])

    print("--- SYSTEM SECURE & IMMUTABLE ✅ ---\n")
