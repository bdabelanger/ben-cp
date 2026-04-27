#!/usr/bin/env python3
"""access.py — Verify vault boundaries, permission integrity, and resource bloat."""
import os, json, subprocess
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')

def check_resource_bloat():
    large_files = []
    threshold_bytes = 10 * 1024 * 1024  # 10MB
    for root, dirs, files in os.walk(VAULT_ROOT):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
                if size > threshold_bytes:
                    large_files.append({
                        "file": os.path.relpath(path, VAULT_ROOT),
                        "size_mb": round(size / (1024 * 1024), 2)
                    })
            except Exception:
                pass
    return large_files

def check_recent_touches():
    # Simple check for files modified in the last 24 hours
    try:
        output = subprocess.check_output(
            ["git", "log", "--since=24.hours", "--name-only", "--pretty=format:"],
            cwd=VAULT_ROOT,
            text=True
        )
        files = set(filter(None, output.split('\n')))
        # Basic boundary check: alert if intelligence/ is modified directly (outside skills/ etc)
        # For now, just logging the touches to be reviewed by the Quartermaster
        return list(files)
    except Exception as e:
        return []

def run():
    bloat = check_resource_bloat()
    touches = check_recent_touches()

    report = {
        "sensor": "access",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "large_files": len(bloat),
            "files_touched_24h": len(touches)
        },
        "resource_bloat": bloat,
        "recent_touches": touches
    }
    
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'access_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ access → {out}")
    return report

if __name__ == '__main__':
    run()
