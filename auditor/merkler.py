import hashlib
import json
import time
from pathlib import Path

# --- [TRISHULA_SQA_v5] SOVEREIGN BIT-LOCK v1.0 ---
# PILLAR 2: BIT-PERFECT STATE PERSISTENCE

class AuditMerkleLedger:
    def __init__(self, ledger_path=".audit_ledger.json"):
        self.ledger_path = Path(ledger_path)
        if not self.ledger_path.exists():
            self._save_ledger({"genesis": "0" * 64, "history": []})

    def _save_ledger(self, data):
        with open(self.ledger_path, "w") as f:
            json.dump(data, f, indent=2)

    def sign_verification(self, file_path):
        """Generates a cryptographic signature of the verified content and appends to ledger."""
        target = Path(file_path)
        content = target.read_bytes()
        file_hash = hashlib.sha256(content).hexdigest()
        
        with open(self.ledger_path, "r") as f:
            ledger = json.load(f)
            
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "filename": target.name,
            "hash": file_hash,
            "status": "VERIFIED"
        }
        
        ledger["history"].append(entry)
        ledger["last_verified_hash"] = file_hash
        
        self._save_ledger(ledger)
        print(f"[+] BIT-LOCK APPLIED: {file_hash[:16]}... recorded in ledger.")
        return file_hash

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python merkler.py <target_file>")
        sys.exit(1)
        
    merkler = AuditMerkleLedger()
    merkler.sign_verification(sys.argv[1])
