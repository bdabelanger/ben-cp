#!/usr/bin/env python3
"""drift.py — Detect unplanned directory growth against sanctioned structure."""
import os, json, re
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')

QUARANTINE_NAMES = {'docs', 'temp', 'scratch', 'tmp', 'wip', 'old', 'backup'}
IGNORE_DIRS = {'dist', 'node_modules', 'src', 'reports'}

def load_sanctioned_dirs():
    """Extract directory names from the vault structure block in AGENTS.md."""
    agents_path = os.path.join(VAULT_ROOT, 'AGENTS.md')
    if not os.path.exists(agents_path):
        return set()
    with open(agents_path, errors='replace') as f:
        content = f.read()
    # Extract the code block containing the directory tree
    m = re.search(r'```\s*\nben-cp/(.*?)```', content, re.DOTALL)
    if not m:
        return set()
    tree = m.group(1)
    # Pull out all directory names from the tree (lines ending with /)
    names = re.findall(r'[├└─ ]*(\w[\w\-\.]*?)/', tree)
    return set(names)

def scan_root_dirs():
    sanctioned = load_sanctioned_dirs()
    findings = []
    try:
        entries = os.listdir(VAULT_ROOT)
    except OSError:
        return findings
    for entry in entries:
        if entry.startswith('.') or entry in IGNORE_DIRS:
            continue
        full = os.path.join(VAULT_ROOT, entry)
        if not os.path.isdir(full):
            continue
        if entry.lower() in QUARANTINE_NAMES:
            findings.append({"path": entry, "severity": "QUARANTINE", "reason": "forbidden_name"})
        elif entry not in sanctioned:
            findings.append({"path": entry, "severity": "WARN", "reason": "unsanctioned_root_dir"})
    return findings

def scan_intelligence_dirs():
    intel_dir = os.path.join(VAULT_ROOT, 'intelligence')
    findings = []
    if not os.path.isdir(intel_dir):
        return findings
    for root, dirs, _ in os.walk(intel_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for d in dirs:
            if d.lower() in QUARANTINE_NAMES:
                rel = os.path.relpath(os.path.join(root, d), VAULT_ROOT)
                findings.append({"path": rel, "severity": "QUARANTINE", "reason": "forbidden_name"})
    return findings

def run():
    root_findings = scan_root_dirs()
    intel_findings = scan_intelligence_dirs()
    all_findings = root_findings + intel_findings

    report = {
        "sensor": "drift",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_findings": len(all_findings),
            "quarantine": sum(1 for f in all_findings if f["severity"] == "QUARANTINE"),
            "warnings": sum(1 for f in all_findings if f["severity"] == "WARN"),
        },
        "findings": all_findings,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'drift_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ drift → {out}")
    return report

if __name__ == '__main__':
    run()
