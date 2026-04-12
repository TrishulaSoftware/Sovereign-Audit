# [WORKFLOWS] - SOVEREIGN-AUDIT

### 1. SENTINEL_WELD
Runs the `auditor/core.py` against all local documentation changes during every `git push`. Prevents documentation decay.

### 2. ADVERSARIAL_CRUCIBLE
Simulates a non-compliant agent that intentionally truncates nodes or mixes perimeters. If the auditor fails to reject the simulation, the build is marked as **COMPROMISED**.

---

# [INSTALLATION] - SOVEREIGN-AUDIT

### PREREQUISITES
- Python 3.10+
- Access to the Trishula Sovereign Vault (Local for now)

### SETUP
1. Clone the repository:
   ```bash
   git clone git@ascension:trishulasoftware/Sovereign-Audit.git
   ```
2. No external dependencies required (Standard Library only for MC/DC Determinism).

---

# [TROUBLESHOOTING] - SOVEREIGN-AUDIT

### FAULT: [AUDIT_REJECTION]
- **Cause**: Node count in Section II is not exactly 10, or "brevity/..." markers were detected.
- **Fix**: Re-render the SITREP and ensure the **Zero-Truncation Mandate** is followed. Verify categorical separation.

### FAULT: [LEDGER_LOCK_FAILURE]
- **Cause**: Permission issues on `.audit_ledger.json`.
- **Fix**: Ensure write access to the root directory.
