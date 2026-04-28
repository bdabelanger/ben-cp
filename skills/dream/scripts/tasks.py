#!/usr/bin/env python3
"""tasks.py — Audit reports/tasks/report.md for currency and overdue items."""
import os, json, re
from datetime import datetime

REPO_ROOT    = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR  = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')
TASKS_REPORT = os.path.join(REPO_ROOT, 'reports', 'tasks', 'report.md')

STALE_HOURS = 48


def count_overdue(content):
    today = datetime.now().date()
    count = 0
    for line in content.splitlines():
        m = re.search(r'due\s+(\d{4}-\d{2}-\d{2})', line)
        if m:
            try:
                d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
                if d < today:
                    count += 1
            except ValueError:
                pass
    return count


def run():
    issues = []

    if not os.path.exists(TASKS_REPORT):
        issues.append({"file": "reports/tasks/report.md", "issue": "report_missing"})
    else:
        age_h = (datetime.now().timestamp() - os.path.getmtime(TASKS_REPORT)) / 3600
        if age_h > STALE_HOURS:
            issues.append({
                "file": "reports/tasks/report.md",
                "issue": "report_stale",
                "hours_since_update": round(age_h, 1),
            })

        try:
            with open(TASKS_REPORT, errors='replace') as f:
                content = f.read()
            overdue = count_overdue(content)
            if overdue > 0:
                issues.append({
                    "file": "reports/tasks/report.md",
                    "issue": "overdue_tasks",
                    "count": overdue,
                })
        except OSError:
            issues.append({"file": "reports/tasks/report.md", "issue": "unreadable"})

    report = {
        "sensor": "tasks",
        "timestamp": datetime.now().isoformat(),
        "summary": {
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
