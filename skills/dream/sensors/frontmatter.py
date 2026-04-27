#!/usr/bin/env python3
"""frontmatter.py — Enforce metadata schema and readability standards."""
import os, json, re
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream')

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', 'archived', 'complete', 'source', 'reports', 'handoffs', 'art'}
SKIP_FILES = {'index.md', 'changelog.md', 'AGENTS.md', 'README.md'}
REQUIRED_KEYS = {'Status', 'Priority', 'Date', 'Owner'}

def collect_md_files():
    files = []
    for root, dirs, fs in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md') and f not in SKIP_FILES:
                files.append(os.path.join(root, f))
    return files

def parse_frontmatter(content):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return None, content
    block = m.group(1)
    keys = set(re.findall(r'^(\w[\w ]*)\s*:', block, re.MULTILINE))
    return keys, content[m.end():]

def word_count(text):
    return len(re.findall(r'\S+', text))

def run():
    issues = []
    scanned = 0

    for path in collect_md_files():
        scanned += 1
        rel = os.path.relpath(path, VAULT_ROOT)
        try:
            with open(path, errors='replace') as f:
                content = f.read()
        except OSError:
            continue

        filename_base = os.path.splitext(os.path.basename(path))[0]
        fm_keys, body = parse_frontmatter(content)

        if fm_keys is None:
            issues.append({"file": rel, "issue": "missing_frontmatter"})
        else:
            missing_keys = REQUIRED_KEYS - fm_keys
            if missing_keys:
                issues.append({"file": rel, "issue": "missing_keys", "keys": sorted(missing_keys)})

        # H1 check (Markdown or HTML)
        h1_md = re.findall(r'^# (.+)$', content, re.MULTILINE)
        h1_html = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        h1_count = len(h1_md) + len(h1_html)
        
        if h1_count == 0:
            issues.append({"file": rel, "issue": "no_h1"})
        elif h1_count > 1:
            issues.append({"file": rel, "issue": "multiple_h1", "count": h1_count})

        # Readability: >500 words without H2 (Markdown or HTML)
        wc = word_count(body if fm_keys is not None else content)
        if wc > 500:
            h2_md = re.findall(r'^## .+$', content, re.MULTILINE)
            h2_html = re.findall(r'<h2[^>]*>', content, re.IGNORECASE)
            if not h2_md and not h2_html:
                issues.append({"file": rel, "issue": "long_file_no_h2", "words": wc})

    report = {
        "sensor": "frontmatter",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanned,
            "issues_found": len(issues),
        },
        "issues": issues,
    }
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'frontmatter_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ frontmatter → {out}")
    return report

if __name__ == '__main__':
    run()
