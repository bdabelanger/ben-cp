#!/usr/bin/env python3
\"\"\"links.py — Validate internal reference integrity across all .md files and .py scripts.
Merges logic from retired paths.py sensor.
\"\"\"
import os, json, re, urllib.parse
from datetime import datetime
from utils import get_manifest_files

REPO_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports', 'archived', 'archive', 'complete'}
SKIP_SCHEMES = ('http://', 'https://', 'mailto:', 'ftp://', '#')

# Repo-relative path pattern for .py files
PATH_PATTERN = re.compile(r'["\']([a-zA-Z][\w\-]+/[\w\-\./]+)["\']')
REPO_ROOTS = {
    'reports', 'skills', 'intelligence', 'handoffs', 'tasks',
    'agents', 'src', 'dist', 'orchestration', 'tools',
}
IGNORE_ROOTS = {'dist', 'node_modules', '__pycache__'}

def strip_code_blocks(content):
    return re.sub(r'```.*?```', '', content, flags=re.DOTALL)

def extract_links(path):
    try:
        with open(path, errors='replace') as f:
            raw = f.read()
    except OSError:
        return []
    content = strip_code_blocks(raw)
    links = []
    # [[wiki-links]]
    for m in re.finditer(r'\[\[([^\]]+)\]\]', content):
        links.append(('wiki', m.group(1).strip()))
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
            target = urllib.parse.unquote(target)
            if target and not target.startswith(SKIP_SCHEMES):
                links.append(('md', target))
        idx = end + 1
    return links

def resolve(link_target, source_path):
    if os.path.isabs(link_target):
        return os.path.normpath(link_target)
    base = os.path.dirname(source_path)
    return os.path.normpath(os.path.join(base, link_target))

def check_stale_paths():
    findings = []
    py_files = []
    for root, dirs, fs in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))
    
    for filepath in py_files:
        try:
            with open(filepath, errors='replace') as f:
                source = f.read()
        except OSError:
            continue
        
        rel_file = os.path.relpath(filepath, REPO_ROOT)
        for m in PATH_PATTERN.finditer(source):
            path_str = m.group(1)
            root_segment = path_str.split('/')[0]
            if root_segment not in REPO_ROOTS or root_segment in IGNORE_ROOTS:
                continue
            full = os.path.join(REPO_ROOT, root_segment)
            if not os.path.exists(full):
                line_num = source[:m.start()].count('\n') + 1
                findings.append({
                    "file": rel_file,
                    "line": line_num,
                    "path": path_str,
                    "missing_root": root_segment
                })
    
    # Deduplicate
    seen = set()
    deduped = []
    for f in findings:
        key = (f["file"], f["missing_root"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    return deduped

def run():
    ghost_links = []
    scanned = 0
    md_files = get_manifest_files()
    for path in md_files:
        if os.path.basename(path).lower() == 'changelog.md':
            continue
        scanned += 1
        for kind, target in extract_links(path):
            if kind == 'wiki':
                name = target.split('|')[0].strip()
                candidates = [p for p in md_files if os.path.splitext(os.path.basename(p))[0] == name]
                if not candidates:
                    ghost_links.append({
                        "source": os.path.relpath(path, REPO_ROOT),
                        "link": f"[[{target}]]",
                        "type": "wiki",
                    })
            else:
                resolved = resolve(target, path)
                if not os.path.exists(resolved):
                    ghost_links.append({
                        "source": os.path.relpath(path, REPO_ROOT),
                        "link": target,
                        "type": "md",
                    })

    stale_paths = check_stale_paths()

    report = {
        "sensor": "links",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanned,
            "ghost_links": len(ghost_links),
            "stale_paths": len(stale_paths)
        },
        "ghost_links": ghost_links,
        "stale_paths": stale_paths
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'links_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ links → {out}")
    return report

if __name__ == '__main__':
    run()
