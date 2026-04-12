import os
import json
import subprocess
from pathlib import Path

class AuditCache:
    """Git-based Scan Cache for Sovereign-Audit."""
    
    def __init__(self, cache_file=None):
        if cache_file is None:
            # Default to local cache in the auditor dir
            self.cache_path = Path(__file__).parent / "scan_cache.json"
        else:
            self.cache_path = Path(cache_file)
            
        self.cache = self._load()

    def _load(self):
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self):
        with open(self.cache_path, "w") as f:
            json.dump(self.cache, f, indent=4)

    def get_git_head(self, directory):
        """Returns the HEAD hash of a git repository."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=directory,
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except Exception:
            return None

    def is_dir_cached(self, directory):
        """Checks if the directory's current Git HEAD matches the cached state."""
        current_head = self.get_git_head(directory)
        if not current_head:
            return False # Not a git repo or error
            
        cached_head = self.cache.get(str(Path(directory).resolve()))
        return current_head == cached_head

    def update_cache(self, directory):
        """Updates the cache with the current Git HEAD of the directory."""
        current_head = self.get_git_head(directory)
        if current_head:
            self.cache[str(Path(directory).resolve())] = current_head
            self._save()

if __name__ == "__main__":
    # Test
    cache = AuditCache()
    print(f"Cache location: {cache.cache_path}")
    print(f"Cached state: {cache.cache}")
