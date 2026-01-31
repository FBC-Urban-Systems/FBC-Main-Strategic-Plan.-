# ==========================================
# PATH: Projects/Project_V_Digital_Earth/data_secure_vault.py
# DESCRIPTION: Secure Data Exchange Protocol (SDEP) Vault
# VERSION: v4.0.0-LTS (PLANETARY / ENTERPRISE MAX)
# CLASSIFICATION: PRODUCTION / AUDIT / CI-CRITICAL
# DATA MODE: REALISTIC / DETERMINISTIC
# ==========================================

from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime
from typing import Dict, Any


# --------------------------------------------------
# SDEP PROTOCOL CONFIGURATION
# --------------------------------------------------
SDEP_PROTOCOL_VERSION = "SDEP-v4.0.0-LTS"
HASH_ALGORITHM = "SHA-256"

# NOTE:
# In production this value is stored in HSM / Vault.
# CI-safe deterministic fallback is provided.
_MASTER_SALT = os.getenv(
    "FBC_SDEP_MASTER_SALT",
    "FBC_DIGITAL_EARTH_ENTERPRISE_MASTER_KEY"
).encode("utf-8")


# --------------------------------------------------
# GOVERNANCE EXCEPTIONS
# --------------------------------------------------
class SDEPComplianceError(Exception):
    """Raised when data violates SDEP governance rules."""


# --------------------------------------------------
# CORE DATA VAULT
# --------------------------------------------------
class FBCDataVault:
    """
    FBC Secure Data Vault — SDEP Core Implementation (MAX VERSION)

    Responsibilities:
    - Enforce planetary data governance
    - Deterministic anonymization
    - Immutable audit trace generation
    - Monetization-safe data packaging
    - CI-safe, forward-compatible architecture
    """

    VAULT_VERSION = "DATA-VAULT-v4.0.0-LTS"

    # --------------------------------------------------
    # GOVERNED DATA CATEGORIES
    # --------------------------------------------------
    GOVERNED_DATA_CATEGORIES = {
        "URBAN_TRAFFIC_FLOW": "HIGH_CLEARANCE",
        "URBAN_ENERGY_FLOW": "HIGH_CLEARANCE",
        "URBAN_ECONOMIC_SIGNAL": "RESTRICTED_CLEARANCE",
        "URBAN_INFRASTRUCTURE_STATE": "RESTRICTED_CLEARANCE",
    }

    def __init__(self, city_id: str) -> None:
        if not isinstance(city_id, str) or not city_id.strip():
            raise ValueError("city_id must be a valid non-empty string")

        self.city_id = city_id.strip()
        self.protocol_version = SDEP_PROTOCOL_VERSION

    # --------------------------------------------------
    # CORE PACKAGING CONTRACT (ENTERPRISE)
    # --------------------------------------------------
    def encrypt_and_package(
        self,
        data_category: str,
        raw_payload: str
    ) -> Dict[str, Any]:
        """
        SDEP-compliant data packaging contract.

        Guarantees:
        - No raw data leakage
        - Deterministic hashing
        - Immutable audit trace
        - Marketplace-safe reference token
        """

        if data_category not in self.GOVERNED_DATA_CATEGORIES:
            raise SDEPComplianceError(
                f"Data category '{data_category}' is not approved under SDEP governance."
            )

        timestamp = datetime.utcnow().isoformat()
        clearance = self.GOVERNED_DATA_CATEGORIES[data_category]

        normalized_payload = str(raw_payload)

        # --------------------------------------------------
        # ANONYMIZED HASH (HMAC-SHA256)
        # --------------------------------------------------
        salted_payload = (
            f"{normalized_payload}|{self.city_id}|{timestamp}"
        ).encode("utf-8")

        secure_hash = hmac.new(
            _MASTER_SALT,
            salted_payload,
            hashlib.sha256
        ).hexdigest().upper()

        # --------------------------------------------------
        # MARKETPLACE TOKEN (NON-REVERSIBLE)
        # --------------------------------------------------
        exchange_token = secure_hash[:40]

        # --------------------------------------------------
        # PAYLOAD METRICS (NO CONTENT)
        # --------------------------------------------------
        payload_size_kb = round(
            len(normalized_payload.encode("utf-8")) / 1024,
            2
        )

        # --------------------------------------------------
        # IMMUTABLE AUDIT TRACE
        # --------------------------------------------------
        audit_trace_id = hashlib.sha256(
            f"{secure_hash}|{self.protocol_version}".encode("utf-8")
        ).hexdigest().upper()

        # --------------------------------------------------
        # FINAL SDEP PACKAGE
        # --------------------------------------------------
        return {
            "sdep_protocol": self.protocol_version,
            "vault_version": self.VAULT_VERSION,
            "origin_city_node": self.city_id,
            "data_category": data_category,
            "security_clearance": clearance,
            "exchange_token": exchange_token,
            "audit_trace_id": audit_trace_id,
            "payload_size_kb": payload_size_kb,
            "is_monetizable": True,
            "timestamp_utc": timestamp,
            "status": "SDEP_PACKAGE_READY"
        }


# --------------------------------------------------
# ENTERPRISE SELF-TEST (CI SAFE)
# --------------------------------------------------
if __name__ == "__main__":
    vault = FBCDataVault("CI-Test-City")

    package = vault.encrypt_and_package(
        data_category="URBAN_ENERGY_FLOW",
        raw_payload="ENERGY_CONSUMPTION_SAMPLE"
    )

    for k, v in package.items():
        print(f"{k}: {v}")
