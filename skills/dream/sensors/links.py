#!/usr/bin/env python3
"""links.py — Validate internal reference integrity across all .md files."""
import os, json, re
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'archived', 'complete'}
SKIP_SCHEMES = ('http://', 'https://', 'mailto:', 'ftp://', '#')

def collect_md_files():
    files = []
    for root, dirs, fs in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md'):
                files.append(os.path.join(root, f))
    return files

def extract_links(path):
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return []
    links = []
    # [[wiki-links]]
    for m in re.finditer(r'\[\[([^\]]+)\]\]', content):
        links.append(('wiki', m.group(1).strip()))
    for m in re.finditer(r'\[([^\]]*)\]\(([^ \n]+)\)', content):
        target = m.group(2).strip().split('#')[0].rstrip(')')
        if not target or any(target.startswith(s) for s in SKIP_SCHEMES):
            continue
        links.append(('md', target))
    return links

def resolve(link_target, source_path):
    if os.path.isabs(link_target):
        return os.path.normpath(link_target)
    base = os.path.dirname(source_path)
    return os.path.normpath(os.path.join(base, link_target))

def run():
    ghost_links = []
    scanned = 0
    md_files = collect_md_files()
    for path in md_files:
        scanned += 1
        for kind, target in extract_links(path):
            if kind == 'wiki':
                # Wiki links: search for any file matching the name anywhere under vault
                name = target.split('|')[0].strip()
                candidates = [p for p in md_files if os.path.splitext(os.path.basename(p))[0] == name]
                if not candidates:
                    ghost_links.append({
                        "source": os.path.relpath(path, VAULT_ROOT),
                        "link": f"[[{target}]]",
                        "type": "wiki",
                    })
            else:
                resolved = resolve(target, path)
                if not os.path.exists(resolved):
                    ghost_links.append({
                        "source": os.path.relpath(path, VAULT_ROOT),
                        "link": target,
                        "type": "md",
                    })

    report = {
        "sensor": "links",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanned,
            "ghost_links": len(ghost_links),
        },
        "ghost_links": ghost_links,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'links_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ links → {out}")
    return report

if __name__ == '__main__':
    run()
