# ==========================================
# PATH: Projects/Project-III-Security-Ledger/secure_vault.py
# DESCRIPTION: FBC Persistent Security & Logging Engine
# ==========================================

import hashlib
import datetime
import pandas as pd
import os

class FBCSecureVault:
    def __init__(self):
        # Master Log File Path
        self.log_file = "audit_trail_master.csv"

    def generate_proof(self, project_id, client_id, value):
        """Generates a SHA-256 hash and logs the transaction to a CSV database."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a unique string for the hash
        raw_string = f"{project_id}-{client_id}-{value}-{timestamp}"
        secure_hash = hashlib.sha256(raw_string.encode()).hexdigest()
        
        # Data to be logged
        log_entry = {
            "Timestamp": timestamp,
            "Project": project_id,
            "Client": client_id,
            "Value": float(value),
            "Hash": secure_hash
        }
        
        # Persistence Logic: Save to CSV
        try:
            df = pd.DataFrame([log_entry])
            if not os.path.isfile(self.log_file):
                df.to_csv(self.log_file, index=False)
            else:
                df.to_csv(self.log_file, mode='a', header=False, index=False)
            status = "LOGGED_SUCCESSFULLY"
        except Exception as e:
            status = f"LOGGING_ERROR: {str(e)}"
            
        return {
            "audit_hash": secure_hash,
            "status": status,
            "timestamp": timestamp
        }

    def get_all_logs(self):
        """Retrieves the entire transaction history."""
        if os.path.exists(self.log_file):
            return pd.read_csv(self.log_file)
        return pd.DataFrame()
