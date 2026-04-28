#!/usr/bin/env python3
"""index.py — Ensure documentation-to-disk parity via index.md cross-reference."""
import os, json, re
from datetime import datetime

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

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
                abs_target = os.path.normpath(os.path.join(index_dir, target))
                rel_target = os.path.relpath(abs_target, REPO_ROOT)
                refs.add(rel_target)
        idx = end + 1
    return refs


def run():
    root_index = os.path.join(REPO_ROOT, 'index.md')
    index_refs = extract_index_refs(root_index)

    # Ghost refs: links in root index.md that don't resolve on disk
    ghosts = []
    for ref in index_refs:
        abs_ref = os.path.join(REPO_ROOT, ref)
        if not os.path.exists(abs_ref):
            ghosts.append({"file": os.path.basename(ref), "ref": ref, "type": "ghost_ref"})

    # Shadow files: .md files in repo root not mentioned in index.md
    shadow = []
    for f in os.listdir(REPO_ROOT):
        if not f.endswith('.md') or f in SKIP_FILES:
            continue
        if not os.path.isfile(os.path.join(REPO_ROOT, f)):
            continue
        if f not in index_refs:
            shadow.append({"file": f, "type": "shadow"})

    report = {
        "sensor": "index",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "shadow_files": len(shadow),
            "ghost_refs": len(ghosts),
        },
        "shadow_files": shadow,
        "ghost_refs": ghosts,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'index_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ index → {out}")
    return report


if __name__ == '__main__':
    run()
