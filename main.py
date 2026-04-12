import sys
from pathlib import Path
from auditor.core import SovereignAuditor
from auditor.merkler import AuditMerkleLedger

# --- [TRISHULA_SQA_v5] SOVEREIGN AUDIT CLI v1.0 ---

def run_sovereign_audit(target_file):
    print(f"[*] INITIALIZING SOVEREIGN AUDIT: {target_file}")
    
    auditor = SovereignAuditor()
    merkler = AuditMerkleLedger()
    
    # 1. Verification Phase
    if not auditor.audit(target_file):
        print("!!! DOCTRINE VIOLATION DETECTED. AUDIT REJECTED. !!!")
        sys.exit(403)
        
    # 2. Persistence Phase
    merkler.sign_verification(target_file)
    
    print("--- AUDIT COMPLETE ---")
    print("[RESULT] SUCCESS: Manifest is bit-locked and doctrine-compliant.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <target_file>")
        sys.exit(1)
        
    run_sovereign_audit(sys.argv[1])
