#!/usr/bin/env python3
"""index.py — Ensure documentation-to-disk parity via index.md cross-reference."""
import os, json, re
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', 'archived', 'complete', 'source'}
SKIP_FILES = {'index.md', 'changelog.md', 'AGENTS.md', 'README.md'}

def extract_index_refs(index_path):
    """Pull all .md file paths (relative to Repo Root) referenced in an index.md."""
    try:
        with open(index_path, errors='replace') as f:
            content = f.read()
    except OSError:
        return set()
    refs = set()
    index_dir = os.path.dirname(index_path)
    
    # Custom parser to handle parens in URLs (e.g. Jira/Asana IDs in filenames)
    idx = 0
    while True:
        idx = content.find('](', idx)
        if idx == -1: break
        start = idx + 2
        parens = 1
        end = start
        while end < len(content):
            if content[end] == '(': parens += 1
            elif content[end] == ')': parens -= 1
            if parens == 0: break
            end += 1
        if parens == 0:
            target = content[start:end].strip()
            if target.startswith('<') and target.endswith('>'):
                target = target[1:-1]
            target = target.split('#')[0].strip()
            target = target.split()[0] if target else ''
            
            if target.endswith('.md') or ('.' not in os.path.basename(target) and target):
                if not target.endswith('.md'):
                    target += '.md'
                # Resolve the target relative to the index_dir
                abs_target = os.path.normpath(os.path.join(index_dir, target))
                # Store the path relative to REPO_ROOT for consistent tracking
                rel_target = os.path.relpath(abs_target, REPO_ROOT)
                refs.add(rel_target)
        idx = end + 1
    return refs

def audit_directory(dir_path):
    shadow = []  # on disk, not in any index
    ghosts = []  # in index, not on disk
    index_path = os.path.join(dir_path, 'index.md')
    if not os.path.exists(index_path):
        return shadow, ghosts

    disk_files = {
        os.path.relpath(os.path.join(dir_path, f), REPO_ROOT) for f in os.listdir(dir_path)
        if f.endswith('.md') and f not in SKIP_FILES and os.path.isfile(os.path.join(dir_path, f))
    }
    index_refs = extract_index_refs(index_path)

    # We only care about shadow files in THIS directory, so we filter index_refs
    # to only those that point to THIS directory.
    local_index_refs = {ref for ref in index_refs if os.path.dirname(os.path.join(REPO_ROOT, ref)) == dir_path}
    
    rel_dir = os.path.relpath(dir_path, REPO_ROOT)
    for f in disk_files - local_index_refs:
        shadow.append({"dir": rel_dir, "file": os.path.basename(f), "type": "shadow"})
        
    # For ghosts, we check if the referenced file exists anywhere it's supposed to
    for ref in index_refs:
        abs_ref = os.path.join(REPO_ROOT, ref)
        if not os.path.exists(abs_ref):
            ghosts.append({"dir": rel_dir, "file": os.path.basename(ref), "type": "ghost_ref"})

    return shadow, ghosts

def run():
    all_shadow = []
    all_ghosts = []

    # Only audit root index.md now
    s, g = audit_directory(REPO_ROOT)
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
