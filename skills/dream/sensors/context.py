#!/usr/bin/env python3
"""context.py — Monitor file volume for token economy."""
import os, json
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')

YELLOW_KB = 250
RED_KB    = 750
SKIP_DIRS = {'.git', '__pycache__', 'node_modules'}

IGNORE_LIST = {
    'intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.pdf',
    'intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.txt'
}

def is_acknowledged(path):
    rel = os.path.relpath(path, VAULT_ROOT)
    if rel in IGNORE_LIST:
        return True
    
    dir_path = os.path.dirname(path)
    index_path = os.path.join(dir_path, 'index.md')
    if not os.path.exists(index_path): return False
    filename = os.path.basename(path)
    import urllib.parse
    try:
        with open(index_path, 'r') as f:
            content = f.read()
            # Check for the filename (or its URL-encoded version) and the new convention e.g. _(7.4MB)_
            return (filename in content or urllib.parse.quote(filename) in content) and ("MB)_" in content or "KB)_" in content)
    except: return False

def run():
    yellow_flags = []
    red_flags    = []
    total_files  = 0
    total_bytes  = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in files:
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            total_files += 1
            total_bytes += size
            rel = os.path.relpath(path, VAULT_ROOT)
            size_kb = size / 1024
            if size_kb > RED_KB:
                if not is_acknowledged(path):
                    red_flags.append({"file": rel, "size_kb": round(size_kb, 1)})
            elif size_kb > YELLOW_KB:
                if not is_acknowledged(path):
                    yellow_flags.append({"file": rel, "size_kb": round(size_kb, 1)})

    red_flags.sort(key=lambda x: -x["size_kb"])
    yellow_flags.sort(key=lambda x: -x["size_kb"])

    report = {
        "sensor": "context",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_files": total_files,
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "red_flags": len(red_flags),
            "yellow_flags": len(yellow_flags),
        },
        "red_flags": red_flags,
        "yellow_flags": yellow_flags,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'context_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ context → {out}")
    return report

if __name__ == '__main__':
    run()
