#!/usr/bin/env python3
"""pulse.py — Monitor physical sync health and boundary rules."""
import os, re, json
from datetime import datetime
from utils import get_manifest, get_manifest_all_files

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

def check_changelog_staleness():
    path = os.path.join(REPO_ROOT, 'changelog.md')
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
    manifest = get_manifest()
    if not manifest:
        return []

    for rel, meta in manifest.get('files', {}).items():
        # Code in intelligence
        if rel.startswith('intelligence/') and rel.endswith(('.py', '.ts')):
            violations.append({"path": rel, "rule": "code_in_intelligence"})
        
        # Data files in skills or orchestration
        data_exts = {'.json', '.csv', '.xml', '.html', '.txt'}
        if any(rel.startswith(d) for d in ['skills/', 'orchestration/']):
            ext = os.path.splitext(rel)[1].lower()
            if ext in data_exts:
                if 'schemas/' in rel or 'templates/' in rel or 'inputs/' in rel or 'outputs/' in rel:
                    continue
                violations.append({"path": rel, "rule": "data_file_in_skills_or_orchestration"})
    
    return violations

def run():
    staleness = check_changelog_staleness()
    violations = scan_boundary_violations()

    report = {
        "sensor": "pulse",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "changelog_status": staleness["status"],
            "boundary_violations": len(violations),
        },
        "changelog": staleness,
        "boundary_violations": violations,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'pulse_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ pulse → {out}")
    return report

if __name__ == '__main__':
    run()
