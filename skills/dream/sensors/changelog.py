#!/usr/bin/env python3
"""changelog.py — Verify version and history integrity."""
import os, json, re, subprocess
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

def parse_root_changelog():
    path = os.path.join(VAULT_ROOT, 'changelog.md')
    if not os.path.exists(path):
        return [], []

    with open(path, errors='replace') as f:
        content = f.read()

    issues = []
    # Extract version numbers
    versions = re.findall(r'##\s+v?(\d+)\.(\d+)(?:\.(\d+))?', content)
    tuples = [(int(a), int(b), int(c or 0)) for a, b, c in versions]

    for i in range(1, len(tuples)):
        prev, curr = tuples[i-1], tuples[i]
        # Versions should be in descending order (newest first) or ascending
        # Detect non-sequential gaps (e.g. v1.0 → v1.3, skipping v1.1, v1.2)
        major_diff = abs(curr[0] - prev[0])
        minor_diff = abs(curr[1] - prev[1])
        if major_diff == 0 and minor_diff > 1:
            issues.append({
                "issue": "version_gap",
                "from": f"v{prev[0]}.{prev[1]}.{prev[2]}",
                "to": f"v{curr[0]}.{curr[1]}.{curr[2]}",
            })
        if major_diff > 1:
            issues.append({
                "issue": "major_version_jump",
                "from": f"v{prev[0]}.{prev[1]}.{prev[2]}",
                "to": f"v{curr[0]}.{curr[1]}.{curr[2]}",
            })

    return tuples, issues

def find_subdirectory_changelogs():
    logs = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        rel = os.path.relpath(root, VAULT_ROOT)
        if rel == '.' :
            continue
        if 'changelog.md' in files:
            logs.append(rel)
    return logs

def check_unlogged_changes():
    try:
        output = subprocess.check_output(
            ["git", "log", "--since=24.hours", "--name-only", "--pretty=format:"],
            cwd=VAULT_ROOT,
            text=True
        )
        files = set(filter(None, output.split('\n')))
        changelogs_touched = [f for f in files if "changelog.md" in f.lower()]
        # If files were modified but no changelog was updated, flag discrepancy
        if files and not changelogs_touched:
            return list(files)
        return []
    except Exception:
        return []

def run():
    versions, version_issues = parse_root_changelog()
    subdir_logs = find_subdirectory_changelogs()
    unlogged_changes = check_unlogged_changes()

    report = {
        "sensor": "changelog",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "root_versions_found": len(versions),
            "version_issues": len(version_issues),
            "subdirectory_changelogs": len(subdir_logs),
            "unlogged_changes": len(unlogged_changes)
        },
        "version_issues": version_issues,
        "subdirectory_changelogs": subdir_logs,
        "unlogged_changes": unlogged_changes,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'changelog_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ changelog → {out}")
    return report

if __name__ == '__main__':
    run()
