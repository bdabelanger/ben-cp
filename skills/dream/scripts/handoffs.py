#!/usr/bin/env python3
"""handoffs.py — Audit implementation plan standards and staleness."""
import os, json, re
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')
HANDOFF_DIR = os.path.join(REPO_ROOT, 'reports', 'handoff')

STALE_DAYS = 14

def scan_dir(path):
    results = []
    if not os.path.isdir(path):
        return results
    for root, dirs, files in os.walk(path):
        if 'archive' in dirs:
            dirs.remove('archive')
        if 'complete' in dirs:
            dirs.remove('complete')
        for f in files:
            if not f.endswith('.md') or f == 'index.md':
                continue
            if 'Dream-Report' in f:
                continue
            results.append(os.path.join(root, f))
    return results

def audit_file(path):
    rel = os.path.relpath(path, REPO_ROOT)
    issues = []
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return [{"file": rel, "issue": "unreadable"}]

    # Extract frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    fm = {}
    if fm_match:
        fm_block = fm_match.group(1)
        for line in fm_block.splitlines():
            if ':' in line:
                key, _, val = line.partition(':')
                fm[key.strip()] = val.strip()

    required_fm = ['title', 'priority', 'assigned_to', 'status', 'date']
    for field in required_fm:
        if field not in fm:
            issues.append({"file": rel, "issue": "missing_frontmatter", "field": field})

    is_ready = 'READY' in fm.get('status', '').upper() or 'READY' in content.upper()

    if is_ready:
        # Execution Steps check
        if '## Execution Steps' not in content:
            issues.append({"file": rel, "issue": "missing_section", "section": "## Execution Steps"})
        else:
            steps_match = re.search(r'^## Execution Steps(.*?)(?=\n## |\Z)', content, re.DOTALL | re.MULTILINE)
            if steps_match:
                checkboxes = re.findall(r'[*-]\s*\[[ x]\]|\d+\.\s*\[[ x]\]', steps_match.group(1))
                if not checkboxes:
                    issues.append({"file": rel, "issue": "ready_no_checkboxes"})

        # Staleness check (>14 days)
        age_d = (datetime.now().timestamp() - os.path.getmtime(path)) / (3600 * 24)
        if age_d > STALE_DAYS:
            issues.append({"file": rel, "issue": "ready_stale", "days_since_edit": round(age_d, 1)})

    return issues

def run():
    all_issues = []
    files = scan_dir(HANDOFF_DIR)
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
