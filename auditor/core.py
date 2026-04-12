import re
import sys
import hashlib
import json
import time
from pathlib import Path

# Add parent to sys.path if running as standalone to handle relative imports
if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).parent.parent))
    from auditor.cache import AuditCache
else:
    try:
        from .cache import AuditCache
    except ImportError:
        from auditor.cache import AuditCache

# --- [TRISHULA_SQA_v5] SOVEREIGN AUDIT CORE v1.1 ---
# ENFORCING: THE OUTWARD MATRIX MANDATE & ZERO-TRUNCATION MANDATE
# SEPTIP: INTEGRATED SCAN CACHE [v1.1 UPDATE]

class SovereignAuditor:
    def __init__(self, cache_file=None):
        self.cache = AuditCache(cache_file)
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
        section_ii_match = re.search(r'\*\*\*\* SECTION II.*?(?=\*\*\*\* SECTION III|$)', content, re.DOTALL)
        if not section_ii_match:
            return []
            
        # Refinement: Strip Markdown comments to allow instructional metadata
        clean_content = re.sub(r'<!--.*?-->', '', section_ii_match.group(), flags=re.DOTALL)
            
        findings = []
        for pattern in self.internal_lexicon:
            if re.search(pattern, clean_content, re.IGNORECASE):
                findings.append(f"CATEGORICAL_CONTAMINATION: Internal keyword '{pattern}' found in External Matrix.")
        return findings

    def _check_truncation(self, content):
        """Enforces the Zero-Truncation Mandate."""
        section_ii_match = re.search(r'\*\*\*\* SECTION II.*?(?=\*\*\*\* SECTION III|$)', content, re.DOTALL)
        if not section_ii_match:
            return []

        # Refinement: Strip Markdown comments before truncation check
        clean_content = re.sub(r'<!--.*?-->', '', section_ii_match.group(), flags=re.DOTALL)

        findings = []
        for marker in self.truncation_markers:
            if re.search(marker, clean_content, re.IGNORECASE):
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
            
        # Verify Docker Law Branch compliance
        errors = self._scan_for_docker_violations(root_dir)
        return errors

    def _scan_for_docker_violations(self, root_dir):
        """Mandatory SEPTIP check: All Docker contexts MUST have .dockerignore."""
        import os
        violations = []
        root_path = Path(root_dir)
        
        # Optimized walk with directory pruning, depth limit, AND GIT CACHE
        ignore_dirs = {".git", "node_modules", "venv", ".venv", "env", ".env", "Aegis-Systems", "The-Scout"}
        max_depth = 3
        
        root_depth = str(root_path.resolve()).count(os.sep)
        
        for root, dirs, files in os.walk(root_dir):
            current_path = Path(root)
            current_depth = str(current_path.resolve()).count(os.sep) - root_depth
            
            if current_depth > max_depth:
                dirs[:] = []
                continue

            # Prune directories in-place
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            # Cache Check: If a directory in 'dirs' is a known git splinter, check cache
            for d in list(dirs):
                splinter_path = current_path / d
                if (splinter_path / ".git").exists():
                    if self.cache.is_dir_cached(splinter_path):
                        # print(f"[+] CACHE HIT: Skipping scan for {d}")
                        dirs.remove(d) 
                    else:
                        # Will enter and scan, then update cache at end
                        pass

            if "Dockerfile" in files:
                context_dir = Path(root)
                if not (context_dir / ".dockerignore").exists():
                    violations.append(f"SEPTIP_VIOLATION [DOCKER_CLI]: Missing .dockerignore in {context_dir.relative_to(root_path)}")
        
        # Final pass: Update cache for all direct splinters in root_dir
        if root_path.exists():
            for d in os.listdir(root_dir):
                splinter_path = root_path / d
                if (splinter_path / ".git").exists():
                    self.cache.update_cache(splinter_path)
                
        return violations

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
