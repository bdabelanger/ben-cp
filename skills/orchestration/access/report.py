#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime, timedelta

# Standard Gazette Envelope Defaults
AGENT_NAME = "Access Auditor (Roz)"
SKILL_NAME = "orchestration/access"
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def run_access_audit():
    findings = []
    flags = []
    status = "ok"

    # 1. Separation Policy Scan
    # Scan skills/ for forbidden file types (*.py, *.log, *.sh, *.json)
    # Approved exceptions: report_spec.json, report.py
    skills_dir = os.path.join(VAULT_ROOT, "skills")
    forbidden_extensions = {".py", ".sh", ".log", ".json"}
    approved_files = {"report_spec.json", "report.py", "package.json"}
    
    violations = []
    for root, dirs, files in os.walk(skills_dir):
        # Skip agent-roots and other specialized folders if needed
        if "agent-roots" in root: continue
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in forbidden_extensions and f not in approved_files:
                rel_path = os.path.relpath(os.path.join(root, f), VAULT_ROOT)
                violations.append(rel_path)
    
    if violations:
        status = "warn"
        flags.append(f"Separation Policy: {len(violations)} architectural violations found in skills/.")
        findings.extend([f"Violation: Unauthorized file at {v}" for v in violations])
    else:
        findings.append("Separation Policy: No unauthorized files found in skills/.")

    # 2. Deletion & Overwrite Watch
    # Scan recent artifacts for "delete" or "overwrite" language
    outputs_dir = os.path.join(VAULT_ROOT, "outputs")
    keywords = [r"\bdelet\w+", r"\bremov\w+", r"\boverwrit\w+", r"\brm -rf\b"]
    
    artifact_violations = []
    cutoff = datetime.now() - timedelta(days=1)
    
    if os.path.exists(outputs_dir):
        for root, dirs, files in os.walk(outputs_dir):
            for f in files:
                if f.endswith(".md"):
                    fpath = os.path.join(root, f)
                    if datetime.fromtimestamp(os.path.getmtime(fpath)) > cutoff:
                        with open(fpath, "r", errors="ignore") as content:
                            text = content.read().lower()
                            # Basic protection: check if it's talking about DELETING a file
                            if any(re.search(k, text) for k in keywords):
                                # Filter out "deleted notes.md" as it's allowed
                                if "deleted notes.md" not in text:
                                    rel_path = os.path.relpath(fpath, VAULT_ROOT)
                                    artifact_violations.append(rel_path)

    if artifact_violations:
        status = "warn"
        flags.append(f"Persistence Watch: Destructive operations proposed/executed in {len(artifact_violations)} sessions.")
        findings.extend([f"Watch: Potential deletion/overwrite in {v}" for v in artifact_violations])
    else:
        findings.append("Persistence Watch: No destructive intent detected in recent sessions.")

    summary = "Access and persistence audit complete."
    if status == "warn":
        summary = f"Access Auditor flagged {len(flags)} violations of vault policy."

    return status, findings, flags, summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.parse_argument("--phase", default="draft")
    args = parser.parse_args()

    status, findings, flags, summary = run_access_audit()
    
    envelope = {
        "agent": AGENT_NAME,
        "skill": SKILL_NAME,
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "summary": summary,
        "findings": findings,
        "flags": flags
    }
    
    print(json.dumps(envelope, indent=2))
