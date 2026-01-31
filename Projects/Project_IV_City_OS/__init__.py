# ============================================================
# FBC DIGITAL SYSTEMS
# Project IV – City Operating System
#
# File: __init__.py
#
# Description:
# Official Public Interface & Governance Boundary
# for FBC City OS Layer
#
# Version: v6.1.0-CITY-OS-MAX-LTS
# Classification: Enterprise / Government / Board Grade
# ============================================================

"""
FBC City Operating System (City OS)

This package represents the sovereign execution layer
of the FBC Urban Intelligence Stack.

Public API only.
Internal modules are governed by Kernel policy.
"""

# ------------------------------------------------------------
# VERSIONING & SYSTEM IDENTITY
# ------------------------------------------------------------
__version__ = "v6.1.0-CITY-OS-MAX-LTS"
__system_layer__ = "PROJECT_IV_CITY_OS"
__classification__ = "ENTERPRISE_MAX"
__audit_ready__ = True

# ------------------------------------------------------------
# PUBLIC API (EXPLICIT EXPORTS ONLY)
# ------------------------------------------------------------
from .core_kernel import FBCKernel
from .secure_vault import FBCSecureVault

__all__ = [
    "FBCKernel",
    "FBCSecureVault",
    "__version__",
    "__system_layer__",
    "__classification__",
    "__audit_ready__"
]

# ------------------------------------------------------------
# IMPORT SAFETY ASSERTION (RUNTIME SAFE)
# ------------------------------------------------------------
def _verify_public_surface():
    allowed = set(__all__)
    exposed = set(globals().keys())

    illegal = exposed - allowed - {
        "__name__", "__doc__", "__package__", "__loader__",
        "__spec__", "__file__", "__builtins__"
    }

    if illegal:
        raise RuntimeError(
            f"City OS package integrity violation. "
            f"Illegal symbols exposed: {illegal}"
        )

_verify_public_surface()
