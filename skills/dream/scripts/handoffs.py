#!/usr/bin/env python3
"""handoffs.py — Audit implementation plan standards."""
import os, json, re
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')
HANDOFF_DIR = os.path.join(REPO_ROOT, 'handoffs')
TASKS_DIR   = os.path.join(REPO_ROOT, 'tasks')

REQUIRED_SECTIONS = {'## Context', '## Execution Steps'}
# ## Logic is highly encouraged but optional for simple tasks
STALE_HOURS = 72

def scan_dir(path):
    results = []
    if not os.path.isdir(path):
        return results
    for f in os.listdir(path):
        if not f.endswith('.md') or f == 'index.md':
            continue
        if f in {'asana.md', 'jira.md'} or 'Dream-Report' in f:
            continue
        results.append(os.path.join(path, f))
    return results

def audit_file(path):
    rel = os.path.relpath(path, REPO_ROOT)
    issues = []
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return [{"file": rel, "issue": "unreadable"}]

    is_ready = bool(re.search(r'READY', content, re.IGNORECASE))

    # Required sections
    for section in REQUIRED_SECTIONS:
        if section not in content:
            issues.append({"file": rel, "issue": "missing_section", "section": section})

    if is_ready:
        # Execution Steps has checkboxes
        steps_match = re.search(r'^## Execution Steps(.*?)(?=\n## |\Z)', content, re.DOTALL | re.MULTILINE)
        if steps_match:
            checkboxes = re.findall(r'[*-]\s*\[[ x]\]|\d+\.\s*\[[ x]\]', steps_match.group(1))
            if not checkboxes:
                issues.append({"file": rel, "issue": "ready_no_checkboxes"})

        # Staleness check
        age_h = (datetime.now().timestamp() - os.path.getmtime(path)) / 3600
        if age_h > STALE_HOURS:
            issues.append({"file": rel, "issue": "ready_stale", "hours_since_edit": round(age_h, 1)})

    return issues

def run():
    all_issues = []
    files = scan_dir(HANDOFF_DIR) + scan_dir(TASKS_DIR)
    for path in files:
        all_issues.extend(audit_file(path))

    report = {
        "sensor": "handoffs",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_audited": len(files),
            "issues_found": len(all_issues),
        },
        "issues": all_issues,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'handoffs_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ handoffs → {out}")
    return report

if __name__ == '__main__':
    run()
