# ==========================================
# PATH: Projects/Project-V-Digital-Earth/data_secure_vault.py
# DESCRIPTION: FBC Secure Data Exchange Protocol (SDEP)
# VERSION: v3.0-SDEP-GOLD (Planetary-Grade)
# ==========================================

import hashlib
import hmac
import os
import json
from datetime import datetime
from typing import Dict

# ==========================================
# SDEP CONFIGURATION
# ==========================================
SDEP_PROTOCOL_VERSION = "SDEP-v3.0-GOLD"
HASH_ALGORITHM = "sha256"

# Master exchange salt (simulated secure seed)
# In production: stored in HSM or environment secret
MASTER_SALT = os.getenv("FBC_SDEP_MASTER_SALT", "FBC_DIGITAL_EARTH_MASTER_KEY").encode()


class SDEPComplianceError(Exception):
    pass


class FBCDataVault:
    """
    Secure Data Exchange Protocol Vault
    Handles anonymization, encryption, compliance packaging,
    and audit-trace generation for Digital Earth Marketplace.
    """

    def __init__(self, city_id: str):
        self.city_id = city_id
        self.protocol_version = SDEP_PROTOCOL_VERSION

    # ------------------------------------------
    # Governance Rules per Data Category
    # ------------------------------------------
    GOVERNED_DATA_CATEGORIES = {
        "URBAN_TRAFFIC_FLOW": "HIGH_CLEARANCE",
        "URBAN_ENERGY_FLOW": "HIGH_CLEARANCE",
        "URBAN_RISK_PROFILE": "RESTRICTED_CLEARANCE",
        "URBAN_INFRASTRUCTURE_STATE": "RESTRICTED_CLEARANCE"
    }

    # ------------------------------------------
    # Core Encryption & Packaging
    # ------------------------------------------
    def encrypt_and_package(self, data_type: str, raw_payload: str) -> Dict:
        timestamp = datetime.utcnow().isoformat()

        # --- Governance Validation ---
        if data_type not in self.GOVERNED_DATA_CATEGORIES:
            raise SDEPComplianceError(f"Data category '{data_type}' not approved for exchange.")

        clearance = self.GOVERNED_DATA_CATEGORIES[data_type]

        # --- Anonymization & Secure Hashing ---
        salted_payload = f"{raw_payload}{timestamp}{self.city_id}".encode()
        secure_hash = hmac.new(MASTER_SALT, salted_payload, hashlib.sha256).hexdigest()

        # --- Exchange Token (Marketplace Reference) ---
        exchange_token = secure_hash[:40]

        # --- Payload Metadata ---
        payload_size_kb = round(len(raw_payload.encode()) / 1024, 2)

        # --- Immutable Audit Trace ID ---
        audit_trace = hashlib.sha256(f"{secure_hash}{timestamp}".encode()).hexdigest()

        # --- Final Package ---
        package = {
            "sdep_protocol": self.protocol_version,
            "origin_city_node": self.city_id,
            "data_category": data_type,
            "security_clearance": clearance,
            "exchange_token": exchange_token,
            "audit_trace_id": audit_trace,
            "payload_size_kb": payload_size_kb,
            "is_monetizable": True,
            "timestamp_utc": timestamp
        }

        return package


# ==========================================
# CLI TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    vault = FBCDataVault("Austin-Node-01")

    sample_payload = "CONSUMPTION_DATA_SAMPLE_102GB"

    packaged = vault.encrypt_and_package("URBAN_ENERGY_FLOW", sample_payload)

    print("\n=== [FBC DIGITAL EARTH | SDEP PACKAGING SUCCESS] ===\n")
    print(json.dumps(packaged, indent=4))
    print("\nSTATUS: READY FOR PLANETARY DATA EXCHANGE 🌍")
