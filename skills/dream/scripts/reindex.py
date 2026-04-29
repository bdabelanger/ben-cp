#!/usr/bin/env python3
"""reindex.py — Regenerate root index.md from live filesystem state.

Runs first in the dream cycle. Other sensors read from the generated
index to validate their own findings against ground truth.
"""
import os, json, re
from datetime import datetime

REPO_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw')
INDEX_PATH  = os.path.join(REPO_ROOT, 'index.md')

SKIP_DIRS  = {'.git', '__pycache__', 'node_modules', 'dist', 'reports', 'complete', 'archive', 'archived'}
SKIP_FILES = {'.DS_Store', '.env', '.gitignore'}

def parse_frontmatter(content):
    """Return dict of frontmatter key/value pairs, or empty dict."""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        kv = re.match(r'^([\w_-]+):\s*(.+)$', line)
        if kv:
            result[kv.group(1)] = kv.group(2).strip().strip("'\"")
    return result

def walk_tree(root, prefix='', skip_dirs=None):
    """Yield (rel_path, is_dir, depth) for a directory tree."""
    skip = skip_dirs or SKIP_DIRS
    try:
        entries = sorted(os.scandir(root), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return
    for entry in entries:
        if entry.name.startswith('.') or entry.name in SKIP_FILES:
            continue
        if entry.is_dir() and entry.name in skip:
            continue
        rel = os.path.relpath(entry.path, REPO_ROOT)
        yield rel, entry.is_dir()
        if entry.is_dir():
            yield from walk_tree(entry.path, skip_dirs=skip)

def scan_repo():
    """
    Walk the repo and return a structured manifest:
    {
      "directories": { "rel/path": { "file_count": N, "frontmatter_coverage": 0.0-1.0 } },
      "files": { "rel/path": { "has_frontmatter": bool, "type": str|None, "taxonomy": str|None } },
      "frontmatter_missing": ["rel/path", ...],
      "unknown_taxonomy_terms": [{"file": ..., "terms": [...]}]
    }
    """
    manifest = {
        "directories": {},
        "files": {},
        "frontmatter_missing": [],
        "unknown_taxonomy_terms": [],
    }

    # Initialize root
    manifest["directories"]["."] = {"file_count": 0, "md_count": 0, "fm_count": 0}
    taxonomy_terms = load_taxonomy_terms()

    for rel, is_dir in walk_tree(REPO_ROOT):
        if is_dir:
            manifest["directories"][rel] = {"file_count": 0, "md_count": 0, "fm_count": 0}
        else:
            # Track in parent directory stats
            parent = os.path.dirname(rel) or "."
            if parent in manifest["directories"]:
                manifest["directories"][parent]["file_count"] += 1

            if not rel.endswith('.md'):
                manifest["files"][rel] = {"has_frontmatter": False, "type": "file"}
                continue

            # Skip changelog and index files for frontmatter checks
            basename = os.path.basename(rel)
            if basename in {'changelog.md', 'index.md'}:
                continue

            try:
                with open(os.path.join(REPO_ROOT, rel), errors='replace') as f:
                    content = f.read()
            except OSError:
                continue

            fm = parse_frontmatter(content)
            has_fm = bool(fm)
            fm_type = fm.get('type')
            fm_taxonomy = fm.get('taxonomy')

            manifest["files"][rel] = {
                "has_frontmatter": has_fm,
                "type": fm_type,
                "taxonomy": fm_taxonomy,
            }

            manifest["directories"][parent]["md_count"] = manifest["directories"][parent].get("md_count", 0) + 1
            if has_fm:
                manifest["directories"][parent]["fm_count"] = manifest["directories"][parent].get("fm_count", 0) + 1

            if not has_fm:
                manifest["frontmatter_missing"].append(rel)

            # Taxonomy validation for intelligence files
            if rel.startswith('intelligence/') and fm_taxonomy:
                if fm_taxonomy.strip().lower() != 'none':
                    terms = [t.strip() for t in fm_taxonomy.split(',')]
                    unknown = [t for t in terms if not any(
                        t.lower() in valid.lower() or valid.lower() in t.lower()
                        for valid in taxonomy_terms
                    )]
                    if unknown:
                        manifest["unknown_taxonomy_terms"].append({"file": rel, "terms": unknown})

    # Compute frontmatter coverage per directory
    for d, stats in manifest["directories"].items():
        md = stats.get("md_count", 0)
        fm = stats.get("fm_count", 0)
        stats["frontmatter_coverage"] = round(fm / md, 2) if md > 0 else 1.0

    return manifest

def load_taxonomy_terms():
    """Return set of valid taxonomy labels from governance/taxonomy.md."""
    path = os.path.join(REPO_ROOT, 'governance', 'taxonomy.md')
    try:
        with open(path, errors='replace') as f:
            content = f.read()
    except OSError:
        return set()
    terms = set()
    for section in ('## Products', '## Features'):
        m = re.search(rf'{re.escape(section)}\n\n([\s\S]*?)\n---', content)
        if m:
            for row in m.group(1).splitlines():
                if row.startswith('|') and '---' not in row and '| Product |' not in row and '| Feature |' not in row:
                    label = row.split('|')[1].strip()
                    if label:
                        terms.add(label)
    # Also include combined labels from inference map backtick values
    for m in re.finditer(r'`([^`]+)`', content):
        val = m.group(1)
        if ' — ' not in val and val not in ('*(omit label; do not guess)*',):
            terms.add(val)
    return terms

def regenerate_index(manifest):
    """
    Re-read the existing index.md structural content and update only the
    auto-generated stats block at the bottom. The hand-authored tree
    sections are preserved.
    """
    try:
        with open(INDEX_PATH, errors='replace') as f:
            existing = f.read()
    except OSError:
        existing = ""

    # Strip old auto-generated stats block if present
    existing = re.sub(r'\n---\n## Auto-generated Stats.*$', '', existing, flags=re.DOTALL).rstrip()

    # Build stats block
    total_files   = len(manifest["files"])
    total_dirs    = len(manifest["directories"])
    missing_fm    = len(manifest["frontmatter_missing"])
    unknown_tax   = len(manifest["unknown_taxonomy_terms"])
    fm_coverage   = round((total_files - missing_fm) / total_files * 100, 1) if total_files else 100.0

    lines = [
        "",
        "---",
        "## Auto-generated Stats",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} by dream/reindex",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Directories | {total_dirs} |",
        f"| Markdown files | {total_files} |",
        f"| Frontmatter coverage | {fm_coverage}% |",
        f"| Missing frontmatter | {missing_fm} |",
        f"| Unknown taxonomy terms | {unknown_tax} |",
    ]

    if manifest["frontmatter_missing"][:5]:
        lines += ["", "**Missing frontmatter (first 5):**"]
        for f in manifest["frontmatter_missing"][:5]:
            lines.append(f"- `{f}`")

    if manifest["unknown_taxonomy_terms"][:5]:
        lines += ["", "**Unknown taxonomy terms (first 5):**"]
        for item in manifest["unknown_taxonomy_terms"][:5]:
            lines.append(f"- `{item['file']}` — {', '.join(item['terms'])}")

    updated = existing + "\n".join(lines) + "\n"
    with open(INDEX_PATH, 'w') as f:
        f.write(updated)

def run():
    manifest = scan_repo()

    # Write manifest to raw outputs for other sensors to use
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'reindex_report.json')
    report = {
        "sensor": "reindex",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "directories": len(manifest["directories"]),
            "files_scanned": len(manifest["files"]),
            "frontmatter_missing": len(manifest["frontmatter_missing"]),
            "unknown_taxonomy_terms": len(manifest["unknown_taxonomy_terms"]),
        },
        "manifest": manifest,
    }
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)

    # Regenerate root index.md stats block
    regenerate_index(manifest)

    print(f"✅ reindex → {out} + index.md updated")
    return report

if __name__ == '__main__':
    run()
