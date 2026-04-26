#!/usr/bin/env python3
"""index.py — Ensure documentation-to-disk parity via index.md cross-reference."""
import os, json, re
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', 'archived', 'complete', 'source'}
SKIP_FILES = {'index.md', 'changelog.md', 'AGENTS.md', 'README.md'}

def extract_index_refs(index_path):
    """Pull all .md filenames referenced in an index.md."""
    try:
        with open(index_path, errors='replace') as f:
            content = f.read()
    except OSError:
        return set()
    refs = set()
    # [text](filename.md) or [text](filename)
    for m in re.finditer(r'\[.*?\]\(([^)]+)\)', content):
        target = m.group(1).strip().split('#')[0]
        if target.endswith('.md') or ('.' not in os.path.basename(target)):
            name = os.path.basename(target)
            if not name.endswith('.md'):
                name += '.md'
            refs.add(name)
    return refs

def audit_directory(dir_path):
    shadow = []  # on disk, not in index
    ghosts = []  # in index, not on disk
    index_path = os.path.join(dir_path, 'index.md')
    if not os.path.exists(index_path):
        return shadow, ghosts

    disk_files = {
        f for f in os.listdir(dir_path)
        if f.endswith('.md') and f not in SKIP_FILES and os.path.isfile(os.path.join(dir_path, f))
    }
    index_refs = extract_index_refs(index_path)

    rel_dir = os.path.relpath(dir_path, VAULT_ROOT)
    for f in disk_files - index_refs:
        shadow.append({"dir": rel_dir, "file": f, "type": "shadow"})
    for f in index_refs - disk_files:
        ghosts.append({"dir": rel_dir, "file": f, "type": "ghost_ref"})

    return shadow, ghosts

def run():
    all_shadow = []
    all_ghosts = []

    for root, dirs, _ in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        s, g = audit_directory(root)
        all_shadow.extend(s)
        all_ghosts.extend(g)

    report = {
        "sensor": "index",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "shadow_files": len(all_shadow),
            "ghost_refs": len(all_ghosts),
        },
        "shadow_files": all_shadow,
        "ghost_refs": all_ghosts,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'index_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ index → {out}")
    return report

if __name__ == '__main__':
    run()
