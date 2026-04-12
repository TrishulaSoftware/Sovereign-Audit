import re
import sys
from pathlib import Path

# --- [TRISHULA_SQA_v5] SOVEREIGN AUDIT CORE v1.0 ---
# ENFORCING: THE OUTWARD MATRIX MANDATE & ZERO-TRUNCATION MANDATE

class SovereignAuditor:
    def __init__(self):
        # Perimeters
        self.internal_lexicon = [
            r'\baegis\b', r'\bjanitor\b', r'\biron box\b', r'\bevo-01\b',
            r'\b.env\b', r'\bbit-lock\b', r'\bmerkle ledger\b', 
            r'\bswarm health\b', r'\bshadow striker\b'
        ]
        
        self.truncation_markers = [
            r'\.\.\.', r'\btruncated\b', r'items truncated', r'brevity'
        ]

    def _count_matrix_nodes(self, content):
        """Identifies Section II and counts the table or list entries."""
        # Find Section II block
        section_ii = re.search(r'\*\*\*\* SECTION II.*?(?=\*\*\*\* SECTION III|$)', content, re.DOTALL)
        if not section_ii:
            return 0, "MISSING_SECTION_II"
            
        # Count items in the Triage Matrix table
        # Looking for rows that looks like | # | Problem | ...
        rows = re.findall(r'^\|\s*\d+\s*\|', section_ii.group(), re.MULTILINE)
        
        # Also count the Analysis items below the table
        analysis_items = re.findall(r'^\d+\.\s+\*\*', section_ii.group(), re.MULTILINE)
        
        return len(rows), len(analysis_items)

    def _check_categorical_purity(self, content):
        """Ensures Section II contains NO internal lexicon/keywords."""
        section_ii = re.search(r'\*\*\*\* SECTION II.*?(?=\*\*\*\* SECTION III|$)', content, re.DOTALL)
        if not section_ii:
            return []
            
        findings = []
        for pattern in self.internal_lexicon:
            if re.search(pattern, section_ii.group(), re.IGNORECASE):
                findings.append(f"CATEGORICAL_CONTAMINATION: Internal keyword '{pattern}' found in External Matrix.")
        return findings

    def _check_truncation(self, content):
        """Enforces the Zero-Truncation Mandate."""
        section_ii = re.search(r'\*\*\*\* SECTION II.*?(?=\*\*\*\* SECTION III|$)', content, re.DOTALL)
        if not section_ii:
            return []

        findings = []
        for marker in self.truncation_markers:
            if re.search(marker, section_ii.group(), re.IGNORECASE):
                findings.append(f"TRUNCATION_VIOLATION: Truncation marker '{marker}' detected in Section II.")
        return findings

    def _check_septip_compliance(self, root_dir):
        """Verifies modular SEPTIP law branches exist for used tools."""
        septip_dir = Path(root_dir) / "doctrine" / "SEPTIP"
        if not septip_dir.exists():
            return ["SEPTIP_VIOLATION: Mission-critical 'doctrine/SEPTIP/' directory is missing."]
        
        # Verify Master Protocol presence
        if not (septip_dir / "Master_Protocol.md").exists():
            return ["SEPTIP_VIOLATION: Master_Protocol.md is missing from doctrine/SEPTIP/."]
            
        return []

    def audit(self, file_path, root_dir=None):
        """Executes the full Sovereign Audit on the target file."""
        target = Path(file_path)
        if not target.exists():
            print(f"[-] ERROR: Target {file_path} not found.")
            return False
            
        content = target.read_text(encoding="utf-8")
        errors = []

        # 1. Structural Check
        table_count, analysis_count = self._count_matrix_nodes(content)
        if table_count != 10:
            errors.append(f"STRUCTURAL_FAULT: Section II Matrix Table contains {table_count}/10 nodes.")
        if analysis_count != 10:
            errors.append(f"STRUCTURAL_FAULT: Section II Triage Analysis contains {analysis_count}/10 nodes.")

        # 2. Categorical Purity
        purity_faults = self._check_categorical_purity(content)
        errors.extend(purity_faults)

        # 3. Truncation Check
        truncation_faults = self._check_truncation(content)
        errors.extend(truncation_faults)

        # 4. SEPTIP Compliance (if root_dir provided)
        if root_dir:
            septip_faults = self._check_septip_compliance(root_dir)
            errors.extend(septip_faults)

        if errors:
            print(f"!!! [SOVEREIGN_AUDIT_REJECTION] - {target.name} FAILED !!!")
            for e in errors:
                print(f"[-] {e}")
            return False

        print(f"[+] {target.name} verified: 100% compliant with the Outward Matrix Mandate.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python core.py <target_file> [root_dir]")
        sys.exit(1)
        
    target_file = sys.argv[1]
    root_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    auditor = SovereignAuditor()
    if not auditor.audit(target_file, root_dir=root_dir):
        sys.exit(403) # Sovereign Rejection
    sys.exit(0)
