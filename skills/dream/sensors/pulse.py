#!/usr/bin/env python3
"""pulse.py — Monitor physical sync health and boundary rules."""
import os, sys, json, re
from datetime import datetime, timezone

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

def check_changelog_staleness():
    path = os.path.join(VAULT_ROOT, 'changelog.md')
    if not os.path.exists(path):
        return {"status": "ERROR", "detail": "changelog.md not found"}
    mtime = os.path.getmtime(path)
    age_h = (datetime.now().timestamp() - mtime) / 3600
    # Also try to parse the last date entry from content
    with open(path, errors='replace') as f:
        content = f.read()
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
    last_date = dates[-1] if dates else None
    stale = age_h > 24
    return {
        "status": "SYNC_STALE" if stale else "OK",
        "last_modified_hours_ago": round(age_h, 1),
        "last_date_in_content": last_date,
    }

def scan_boundary_violations():
    violations = []
    intel_dir = os.path.join(VAULT_ROOT, 'intelligence')
    for root, dirs, files in os.walk(intel_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith(('.py', '.ts')):
                rel = os.path.relpath(os.path.join(root, f), VAULT_ROOT)
                violations.append({"path": rel, "rule": "code_in_intelligence"})

    # Non-functional data files in skills/ or orchestration/
    data_exts = {'.json', '.csv', '.xml', '.html', '.txt'}
    for check_dir in ['skills', 'orchestration']:
        dir_path = os.path.join(VAULT_ROOT, check_dir)
        if not os.path.isdir(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in data_exts:
                    # Allow schemas and templates
                    rel_dir = os.path.relpath(root, VAULT_ROOT)
                    if 'schemas' in rel_dir or 'templates' in rel_dir:
                        continue
                    rel = os.path.join(rel_dir, f)
                    violations.append({"path": rel, "rule": "data_file_in_skills_or_orchestration"})
    return violations

def check_index_coverage():
    missing = []
    ignore_dirs = {'.', 'node_modules', 'reports', 'dist', 'src', '.git', '.gemini'}
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_dirs and d != '__pycache__']
        rel_root = os.path.relpath(root, VAULT_ROOT)
        md_files = [f for f in files if f.endswith('.md')]
        if md_files and 'index.md' not in files:
            missing.append(rel_root)
    return missing

def run():
    staleness = check_changelog_staleness()
    violations = scan_boundary_violations()
    missing_index = check_index_coverage()

    report = {
        "sensor": "pulse",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "changelog_status": staleness["status"],
            "boundary_violations": len(violations),
            "dirs_missing_index": len(missing_index),
        },
        "changelog": staleness,
        "boundary_violations": violations,
        "dirs_missing_index": missing_index,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'pulse_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ pulse → {out}")
    return report

if __name__ == '__main__':
    run()
