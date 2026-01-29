# ==========================================
# PATH: /core_kernel.py
# DESCRIPTION: FBC Universal Path Integrator & Master Kernel
# VERSION: v2.7-Stable-Production
# ==========================================

import sys
import os

def initialize_fbc_os():
    """
    Dynamically injects all project directories into the system path.
    This ensures that imports work regardless of where the script is executed.
    """
    # Get the root directory of the repository
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # List of all strategic project sectors
    PROJECT_SECTORS = [
        "Projects/Project-I-Urban-Revenue",
        "Projects/Project-II-Private-Districts",
        "Projects/Project-III-Traffic-Intelligence",
        "Projects/Project-III-Security-Ledger",
        "Projects/Project-IV-City-OS",
        "Projects/Project-V-Digital-Earth",
        "Projects/Project-VI-Global-Dominance"
    ]
    
    print("--- [KERNEL] Initializing FBC Global Infrastructure ---")
    
    added_count = 0
    for sector in PROJECT_SECTORS:
        full_path = os.path.join(BASE_DIR, sector)
        if os.path.exists(full_path):
            if full_path not in sys.path:
                sys.path.append(full_path)
                added_count += 1
        else:
            print(f"⚠️ Warning: Sector path not found: {sector}")

    print(f"--- [KERNEL] Master Sync Complete. {added_count} Sectors Linked ✅ ---")

if __name__ == "__main__":
    initialize_fbc_os()
    
    # Verification of core engines
    try:
        # These will now work from any folder thanks to the dynamic path injection
        print("--- [KERNEL] Verifying Engine Integrity... ---")
        # Note: Imports are done inside try to catch missing files
        from revenue_optimizer import RevenueOptimizer
        from secure_vault import FBCSecureVault
        
        vault = FBCSecureVault()
        print("--- [KERNEL] System Integrity: SECURED & OPERATIONAL 🛡️ ---")
    except ImportError as e:
        print(f"--- [KERNEL] Critical Failure: {e} ---")
