#!/usr/bin/env python3
"""tasks.py — Track strategic momentum across active tasks."""
import os, json, re
from datetime import datetime

VAULT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR  = os.path.join(VAULT_ROOT, 'reports')
TASKS_DIR    = os.path.join(VAULT_ROOT, 'tasks')
PROJECTS_DIR = os.path.join(VAULT_ROOT, 'intelligence', 'product', 'projects')

STALE_HOURS = 48
SKIP_FILES  = {'index.md', 'asana.md', 'jira.md'}

def collect_task_files():
    files = []
    if not os.path.isdir(TASKS_DIR):
        return files
    for f in os.listdir(TASKS_DIR):
        if f.endswith('.md') and f not in SKIP_FILES:
            files.append(os.path.join(TASKS_DIR, f))
    return files

def extract_priority(content):
    m = re.search(r'\*\*priority\*\*\s*[:\-]\s*(\w+)', content, re.IGNORECASE)
    return m.group(1).upper() if m else None

def extract_project_links(content):
    return re.findall(r'\[.*?\]\(([^)]*intelligence/product/projects[^)]*)\)', content)

def run():
    issues = []
    files = collect_task_files()

    for path in files:
        rel = os.path.relpath(path, VAULT_ROOT)
        try:
            with open(path, errors='replace') as f:
                content = f.read()
        except OSError:
            continue

        priority = extract_priority(content)
        age_h = (datetime.now().timestamp() - os.path.getmtime(path)) / 3600

        if priority in ('P1', 'P2') and age_h > STALE_HOURS:
            issues.append({
                "file": rel,
                "issue": "high_priority_stale",
                "priority": priority,
                "hours_since_update": round(age_h, 1),
            })

        # Verify project links resolve
        for link in extract_project_links(content):
            target = os.path.normpath(os.path.join(VAULT_ROOT, link.lstrip('/')))
            if not os.path.exists(target):
                issues.append({"file": rel, "issue": "broken_project_link", "link": link})

    report = {
        "sensor": "tasks",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_audited": len(files),
            "issues_found": len(issues),
        },
        "issues": issues,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'tasks_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ tasks → {out}")
    return report

if __name__ == '__main__':
    run()
