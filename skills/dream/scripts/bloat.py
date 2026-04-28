#!/usr/bin/env python3
"""bloat.py — Monitor file volume and recent activity for resource hygiene.
Merges logic from retired access.py and context.py sensors.
"""
import os, json, subprocess
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

YELLOW_KB = 250
RED_KB    = 750
CRITICAL_MB = 10
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'complete', 'archive', 'archived'}

def check_recent_touches():
    try:
        output = subprocess.check_output(
            ["git", "log", "--since=24.hours", "--name-only", "--pretty=format:"],
            cwd=REPO_ROOT,
            text=True
        )
        files = set(filter(None, output.split('\n')))
        return list(files)
    except Exception:
        return []

def run():
    yellow_flags = []
    red_flags    = []
    critical_flags = []
    total_files  = 0
    total_bytes  = 0

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            total_files += 1
            total_bytes += size
            rel = os.path.relpath(path, REPO_ROOT)
            size_kb = size / 1024
            size_mb = size / (1024 * 1024)

            if size_mb > CRITICAL_MB:
                critical_flags.append({"file": rel, "size_mb": round(size_mb, 2)})
            elif size_kb > RED_KB:
                red_flags.append({"file": rel, "size_kb": round(size_kb, 1)})
            elif size_kb > YELLOW_KB:
                yellow_flags.append({"file": rel, "size_kb": round(size_kb, 1)})

    critical_flags.sort(key=lambda x: -x["size_mb"])
    red_flags.sort(key=lambda x: -x["size_kb"])
    yellow_flags.sort(key=lambda x: -x["size_kb"])
    touches = check_recent_touches()

    report = {
        "sensor": "bloat",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_files": total_files,
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "critical_flags": len(critical_flags),
            "red_flags": len(red_flags),
            "yellow_flags": len(yellow_flags),
            "files_touched_24h": len(touches)
        },
        "critical_flags": critical_flags,
        "red_flags": red_flags,
        "yellow_flags": yellow_flags,
        "recent_touches": touches
    }
    
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'bloat_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ bloat → {out}")
    return report

if __name__ == '__main__':
    run()
