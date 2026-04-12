#!/usr/bin/env python3
import json
import os
import re
from datetime import datetime

# Standard Gazette Envelope Defaults
AGENT_NAME = "Vault Auditor (Antigravity)"
SKILL_NAME = "intelligence/memory"
VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def run_integrity_scan():
    agents_md_path = os.path.join(VAULT_ROOT, "AGENTS.md")
    findings = []
    flags = []
    status = "ok"

    if not os.path.exists(agents_md_path):
        return "error", ["AGENTS.md not found at root."], ["CRITICAL: Missing AGENTS.md source of truth."]

    with open(agents_md_path, "r") as f:
        content = f.read()

    # 1. Extract official skill list from AGENTS.md
    # Look for the skills/ layout section
    structure_match = re.search(r"└── skills/(.*?)(?=\n---|\n#|$)", content, re.DOTALL)
    if not structure_match:
        return "warn", ["Could not parse Vault Structure in AGENTS.md."], ["Navigation schema missing."]

    structure_content = structure_match.group(0)
    # Extract relative paths like orchestration/changelog
    official_paths = re.findall(r"├── (.*?)[\s│]", structure_content)
    official_paths += re.findall(r"└── (.*?)[\s│]", structure_content)
    
    # Process sub-skills (nested one level deeper)
    nested_paths = re.findall(r"│\s+├── (.*?)[\s│]", structure_content)
    nested_paths += re.findall(r"│\s+└── (.*?)[\s│]", structure_content)
    
    # This regex is a bit brittle, so let's use a simpler heuristic: 
    # Find all lines inside the structure block that mention a directory slash.
    all_paths = []
    for line in structure_content.splitlines():
        match = re.search(r"(\w+/[\w-]+/?)", line)
        if match:
            all_paths.append(match.group(1).rstrip("/"))
    
    unique_official = set(all_paths)
    findings.append(f"Identified {len(unique_official)} official skill domains in AGENTS.md.")

    # 2. Verify Triad Existence for each official skill
    triad_violations = []
    verified_count = 0
    for rel_path in unique_official:
        skill_dir = os.path.join(VAULT_ROOT, "skills", rel_path)
        if not os.path.isdir(skill_dir):
            flags.append(f"Missing Domain: {rel_path} defined in AGENTS.md but directory missing.")
            status = "warn"
            continue

        missing_triad = []
        for file in ["SKILL.md", "audit.md", "report.md"]:
            if not os.path.exists(os.path.join(skill_dir, file)):
                missing_triad.append(file)
        
        if missing_triad:
            triad_violations.append(f"{rel_path} (missing {', '.join(missing_triad)})")
            status = "warn"
        else:
            verified_count += 1
    
    findings.append(f"Triad Compliance: {verified_count}/{len(unique_official)} skills follow the standard.")
    if triad_violations:
        flags.append(f"Triad Violations found in {len(triad_violations)} skills.")
        findings.extend([f"Violation: {v}" for v in triad_violations])

    # 3. Check for physical symlink drift (legacy redirects)
    # Check a few key ones: skills/changelog -> orchestration/changelog
    redirects = {
        "changelog": "orchestration/changelog",
        "handoff": "orchestration/handoff",
        "access": "orchestration/access",
        "memory": "intelligence/memory"
    }
    for legacy, target in redirects.items():
        legacy_path = os.path.join(VAULT_ROOT, "skills", legacy)
        if not os.path.islink(legacy_path):
             findings.append(f"Legacy Redirect Drift: {legacy} is not a symlink.")

    summary = "Watchdog structural integrity scan complete."
    if status == "warn":
        summary = f"Watchdog flagged {len(flags)} structural violations."

    return status, findings, flags, summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="draft")
    args = parser.parse_args()

    status, findings, flags, summary = run_integrity_scan()
    
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
