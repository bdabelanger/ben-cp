#!/usr/bin/env python3
import json
import os
import re
import subprocess
from datetime import datetime

# Standard Gazette Envelope Defaults
AGENT_NAME = "Changelog Auditor (Yukon Cornelius)"
SKILL_NAME = "orchestration/changelog"
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def run_audit():
    changelog_path = os.path.join(VAULT_ROOT, "changelog.md")
    findings = []
    flags = []
    status = "ok"

    if not os.path.exists(changelog_path):
        return "error", ["Changelog not found at root."], ["CRITICAL: Missing root changelog.md"]

    with open(changelog_path, "r") as f:
        content = f.read()

    # 1. Parse latest version block
    # Matches ## [1.18.1] ... (2026-04-12) followed by bullet points
    latest_block_match = re.search(r"## \[(.*?)\] — (.*?) \((.*?)\)\n\n(.*?)(?=\n##|$)", content, re.DOTALL)
    
    if not latest_block_match:
        return "warn", ["Could not parse latest changelog block structure."], ["Format violation in root changelog."]

    version, title, date, version_content = latest_block_match.groups()
    findings.append(f"Latest Version: {version} ({date})")
    
    # 2. Extract file paths
    # Matches patterns like - `path` or - [path](...)
    # We capture the potential path and filter out category headers in Python
    raw_hits = re.findall(r"- [\[`]?([\w/.*-]+)[\]`]?[\s\n]", version_content)
    
    unique_paths = set()
    for p in raw_hits:
        # Clean up and normalize
        p = p.strip("`[]").strip()
        # Ignore category headers (starting with **) or generic text
        if p and not p.startswith("*") and not p.startswith("["):
            unique_paths.add(p)

    # 3. Verify existence
    missing_files = []
    for p in unique_paths:
        full_path = os.path.join(VAULT_ROOT, p)
        if not os.path.exists(full_path):
            missing_files.append(p)
    
    if missing_files:
        status = "warn"
        for f in missing_files:
            flags.append(f"Ghost Track: {f} mentioned in log but missing on disk.")
    else:
        findings.append(f"Verified {len(unique_paths)} file paths mentioned in v{version}.")

    # 4. Check for undocumented changes (Git Drift)
    try:
        # Get files changed in the last 24 hours
        git_cmd = ["git", "log", "--since='24 hours ago'", "--name-only", "--pretty=format:"]
        result = subprocess.run(git_cmd, cwd=VAULT_ROOT, capture_output=True, text=True)
        changed_files = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        
        undocumented = changed_files - unique_paths
        # Filter out noise like .DS_Store or internal tools if needed
        undocumented = {f for f in undocumented if not f.startswith(".") and os.path.exists(os.path.join(VAULT_ROOT, f))}
        
        if undocumented:
            status = "warn"
            for f in undocumented:
                flags.append(f"Snowed In: {f} modified in Git but undocumented in latest log.")
        else:
            findings.append("No git-to-log drift detected in the last 24 hours.")
            
    except Exception as e:
        findings.append(f"Git audit skipped: {str(e)}")

    summary = f"Lumberjack audit of v{version} complete."
    if status == "warn":
        summary = f"Audit flagged {len(flags)} integrity issues in v{version}."
    
    return status, findings, flags, summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="draft")
    args = parser.parse_args()

    status, findings, flags, summary = run_audit()
    
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
