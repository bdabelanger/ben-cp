#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "intelligence", "core", "skills"))

def main():
    violations = []
    # Check for scripts in skills/
    for ext in ["*.py", "*.sh", "*.json"]:
        if ext == "*.json":
            # Filter out report_spec.json as it is permitted metadata
            files = [f for f in glob.glob(os.path.join(SKILLS_DIR, "**", ext), recursive=True) if "report_spec.json" not in f]
        else:
            files = glob.glob(os.path.join(SKILLS_DIR, "**", ext), recursive=True)
        
        for f in files:
            violations.append(f"Separation Violation: {os.path.relpath(f, SKILLS_DIR)}")
    
    status = "ok" if not violations else "warn"
    summary = "Access Policy Audit: PASS" if not violations else f"Access Policy Audit: {len(violations)} violations flagged."
    
    envelope = {
        "skill": "orchestration/access",
        "preferred_agent": "Access Auditor",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "summary": summary,
        "findings": [
            "Scanning intelligence/core/skills/ directory for prohibited file types (Scripts, Manifests, Dynamic Data)."
        ],
        "flags": violations
    }
    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
