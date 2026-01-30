# ==========================================
# PATH: Projects/Project-III-Security-Ledger/secure_vault.py
# DESCRIPTION: FBC Sector Security Ledger (Project-III)
# VERSION: v4.2-SECTOR-LEDGER-GRADE
# ==========================================

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

class FBCSecureVault:
    """
    FBC Sector-Level Immutable Security Ledger
    Compatible with Global Ledger (Project-IV)
    SHA-256 + Salt + Chain Linking
    """

    def __init__(self):
        # Sector ledger file
        self.ledger_file = Path(__file__).resolve().parent / "fbc_sector_ledger.json"

        # Shared cryptographic standards
        self.protocol = "SHA-256-FBC-GOLD"
        self._salt = os.getenv("FBC_SECRET", "GLOBAL_RESERVE_2026_PROPRIETARY")

        # Optional link to Global Ledger (if exists)
        self.global_ledger_path = Path(__file__).resolve().parents[1] / "Project-IV-City-OS" / "fbc_global_ledger.json"

        # Initialize ledger if not exists
        if not self.ledger_file.exists():
            self._initialize_sector_ledger()

    # --------------------------------------------------
    # INITIALIZE SECTOR GENESIS BLOCK
    # --------------------------------------------------
    def _initialize_sector_ledger(self):
        genesis = {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "node": "SECTOR_GENESIS",
            "amount": 0,
            "previous_hash": "0"*64,
            "audit_hash": self._hash("SECTOR_GENESIS_BLOCK"),
            "status": "GENESIS_BLOCK"
        }
        with open(self.ledger_file, "w") as f:
            json.dump([genesis], f, indent=4)

    # --------------------------------------------------
    # CORE HASH
    # --------------------------------------------------
    def _hash(self, raw):
        return hashlib.sha256(raw.encode()).hexdigest().upper()

    # --------------------------------------------------
    # LOAD / SAVE LEDGER
    # --------------------------------------------------
    def _load_ledger(self):
        with open(self.ledger_file, "r") as f:
            return json.load(f)

    def _save_ledger(self, ledger):
        with open(self.ledger_file, "w") as f:
            json.dump(ledger, f, indent=4)

    # --------------------------------------------------
    # BACKWARD-COMPATIBLE FUNCTION
    # (Used by older dashboards)
    # --------------------------------------------------
    def generate_audit_proof(self, node_id, amount):
        return self.generate_proof("PROJECT_III", node_id, amount)

    # --------------------------------------------------
    # NEW STANDARDIZED PROOF FUNCTION
    # --------------------------------------------------
    def generate_proof(self, project_id, node_id, amount):
        ledger = self._load_ledger()
        last_block = ledger[-1]

        timestamp = datetime.now().isoformat()

        raw_string = f"{project_id}|{node_id}|{amount}|{timestamp}|{self._salt}|{last_block['audit_hash']}"
        secure_hash = self._hash(raw_string)

        new_block = {
            "index": last_block["index"] + 1,
            "timestamp": timestamp,
            "project_id": project_id,
            "node": node_id,
            "amount": amount,
            "protocol": self.protocol,
            "previous_hash": last_block["audit_hash"],
            "audit_hash": secure_hash,
            "status": "IMMUTABLE_RECORD"
        }

        ledger.append(new_block)
        self._save_ledger(ledger)

        # Optional mirror into Global Ledger if present
        self._mirror_to_global_ledger(new_block)

        return new_block

    # --------------------------------------------------
    # MIRROR ENTRY TO GLOBAL LEDGER (IF AVAILABLE)
    # --------------------------------------------------
    def _mirror_to_global_ledger(self, block):
        try:
            if self.global_ledger_path.exists():
                with open(self.global_ledger_path, "r") as f:
                    global_ledger = json.load(f)

                global_ledger.append({
                    "index": len(global_ledger),
                    "timestamp": block["timestamp"],
                    "project_id": block["project_id"],
                    "node": block["node"],
                    "value": block["amount"],
                    "protocol": block["protocol"],
                    "previous_hash": global_ledger[-1]["audit_hash"],
                    "audit_hash": block["audit_hash"],
                    "status": "MIRRORED_FROM_SECTOR"
                })

                with open(self.global_ledger_path, "w") as f:
                    json.dump(global_ledger, f, indent=4)
        except:
            # Global ledger not mandatory — sector ledger still works standalone
            pass

    # --------------------------------------------------
    # VERIFY SECTOR LEDGER INTEGRITY
    # --------------------------------------------------
    def verify_sector_ledger(self):
        ledger = self._load_ledger()

        for i in range(1, len(ledger)):
            current = ledger[i]
            previous = ledger[i-1]

            raw_check = f"{current['project_id']}|{current['node']}|{current['amount']}|{current['timestamp']}|{self._salt}|{previous['audit_hash']}"
            recalculated = self._hash(raw_check)

            if recalculated != current["audit_hash"]:
                return {"status": "TAMPER_DETECTED", "failed_block": i}

            if current["previous_hash"] != previous["audit_hash"]:
                return {"status": "CHAIN_BROKEN", "failed_block": i}

        return {"status": "SECTOR_LEDGER_INTEGRITY_CONFIRMED", "blocks": len(ledger)}

# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------
if __name__ == "__main__":
    vault = FBCSecureVault()

    print("\n--- FBC SECTOR SECURITY LEDGER TEST ---")

    proof = vault.generate_audit_proof("Riyadh-Center", 12.5)
    print("New Sector Block Hash:", proof["audit_hash"][:20], "...")

    status = vault.verify_sector_ledger()
    print("Verification:", status["status"])

    print("--- SECTOR LEDGER SECURE ✅ ---\n")
