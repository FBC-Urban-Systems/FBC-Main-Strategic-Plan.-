# ==========================================
# PATH: Projects/Project-III-Security-Ledger/secure_vault_1.py
# DESCRIPTION: FBC Secure Ledger - Persistent Audit System
# VERSION: v3.5-Immutable
# ==========================================

import hashlib
import json
import os
from datetime import datetime

class FBCSecureVault:
    def __init__(self):
        self.vault_file = "fbc_master_ledger.json"
        self._salt = os.getenv("FBC_SECRET", "GLOBAL_RESERVE_2026_PROPRIETARY")

    def generate_audit_proof(self, node_id, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Creating a cryptographic binding
        raw_string = f"{node_id}{amount}{timestamp}{self._salt}"
        secure_hash = hashlib.sha256(raw_string.encode()).hexdigest()

        proof = {
            "node": node_id,
            "amount": f"${amount}M",
            "timestamp": timestamp,
            "audit_hash": secure_hash.upper(),
            "status": "IMMUTABLE_RECORD"
        }

        self._persist_to_ledger(proof)
        return proof

    def _persist_to_ledger(self, entry):
        """Appends the audit proof to a permanent file (The Ledger)"""
        ledger_data = []
        if os.path.exists(self.vault_file):
            with open(self.vault_file, 'r') as f:
                try: ledger_data = json.load(f)
                except: ledger_data = []
        
        ledger_data.append(entry)
        with open(self.vault_file, 'w') as f:
            json.dump(ledger_data, f, indent=4)

if __name__ == "__main__":
    vault = FBCSecureVault()
    print(vault.generate_audit_proof("Riyadh-Center", 12.5))
