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
    # Look for any skill path in the Vault Structure section (line 104+)
    structure_start = content.find("## Vault Structure")
    if structure_start == -1:
        return "warn", ["Could not find Vault Structure in AGENTS.md."], ["Missing section."]
    
    structure_block = content[structure_start:]
    # Find all patterns that look like skills/path/to/thing
    # This also catches parenthetical sub-skills like (Synthesize/Predict)
    all_hits = re.findall(r"(skills/[\w/-]+)", structure_block)
    # Clean up hits and normalize
    unique_official = set()
    for h in all_hits:
        cleaned = h.replace("skills/", "").strip("/").lower()
        if cleaned:
            unique_official.add(cleaned)
    
    findings.append(f"Identified {len(unique_official)} official skill domains in AGENTS.md.")

    # 1b. Orphan Check: Walk physical skills/ and find things NOT in the list
    skills_dir = os.path.join(VAULT_ROOT, "skills")
    physical_dirs = []
    # Directories that are just containers for other skills or known administrative folders
    known_paths = {
        "intelligence", "orchestration", "product", 
        "intelligence/analysis", "intelligence/memory",
        "intelligence/casebook", "orchestration/handoff",
        "shared", "rovo", "styles"
    }
    
    for root, dirs, files in os.walk(skills_dir):
        # We only care about directories that contain a SKILL.md (actual skills)
        if "SKILL.md" in files:
            rel = os.path.relpath(root, skills_dir)
            if rel == ".": continue
            rel_lower = rel.lower()
            if rel_lower not in unique_official and rel_lower not in known_paths:
                if "agent-roots" not in rel:
                    physical_dirs.append(rel_lower)
    
    orphans = set(physical_dirs)
    if orphans:
        status = "warn"
        for o in orphans:
            flags.append(f"Orphan Skill: '{o}' exists on disk but is unmapped in AGENTS.md.")

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
