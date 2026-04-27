#!/usr/bin/env python3
"""paths.py — Detect stale hardcoded vault paths in Python scripts.

Scans all .py files for string literals that look like vault-relative paths
(e.g. reports/projects/data, reports/dream/report.md) and checks whether the
referenced top-level directory actually exists. Flags any that do not.

This catches the class of bug where a directory is renamed or restructured
but script path constants are not updated to match.
"""
import os, json, re, ast
from datetime import datetime

VAULT_ROOT  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUTPUTS_DIR = os.path.join(VAULT_ROOT, 'reports', 'dream', 'data', 'raw')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist'}

# Vault-relative path pattern: starts with a known top-level dir name,
# followed by / and more path components. We extract the first segment
# and check it exists under VAULT_ROOT.
# Only flag paths with at least 2 segments (avoids single-word false positives).
PATH_PATTERN = re.compile(r'["\']([a-zA-Z][\w\-]+/[\w\-\./]+)["\']')

# Known vault top-level directories — only flag paths whose root is one of these.
# This prevents MIME types like "application/json" from triggering false positives.
VAULT_ROOTS = {
    'reports', 'skills', 'intelligence', 'handoffs', 'tasks',
    'agents', 'src', 'dist', 'orchestration', 'tools',
}

# Top-level dirs that are allowed to not exist (generated, ephemeral, etc.)
IGNORE_ROOTS = {'dist', 'node_modules', '__pycache__'}


def collect_py_files():
    files = []
    for root, dirs, fs in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for f in fs:
            if f.endswith('.py'):
                files.append(os.path.join(root, f))
    return files


def extract_path_strings(filepath):
    """Extract string literals from a Python file that look like vault paths."""
    try:
        with open(filepath, errors='replace') as f:
            source = f.read()
    except OSError:
        return []

    candidates = []
    for m in PATH_PATTERN.finditer(source):
        path_str = m.group(1)
        # Get line number
        line_num = source[:m.start()].count('\n') + 1
        candidates.append((path_str, line_num))
    return candidates


def check_path(path_str):
    """
    Check if the vault-relative path's top-level directory exists.
    Returns (root_segment, exists, skip) where skip=True means ignore this path.
    """
    root_segment = path_str.split('/')[0]
    # Only check paths whose root is a known vault directory
    if root_segment not in VAULT_ROOTS:
        return root_segment, True, True  # skip — not a vault path
    if root_segment in IGNORE_ROOTS:
        return root_segment, True, False
    full = os.path.join(VAULT_ROOT, root_segment)
    return root_segment, os.path.exists(full), False


def run():
    findings = []
    scanned = 0
    py_files = collect_py_files()

    for filepath in py_files:
        scanned += 1
        rel = os.path.relpath(filepath, VAULT_ROOT)
        candidates = extract_path_strings(filepath)

        for path_str, line_num in candidates:
            root_segment, exists, skip = check_path(path_str)
            if skip or exists:
                continue
            findings.append({
                "file": rel,
                "line": line_num,
                "path": path_str,
                "missing_root": root_segment,
                "severity": "WARN",
            })

    # Deduplicate — same stale root in same file is one finding
    seen = set()
    deduped = []
    for f in findings:
        key = (f["file"], f["missing_root"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    report = {
        "sensor": "paths",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "files_scanned": scanned,
            "stale_paths": len(deduped),
        },
        "findings": deduped,
    }

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, 'paths_report.json')
    with open(out, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ paths → {out}")
    return report


if __name__ == '__main__':
    report = run()
    findings = report["findings"]
    if findings:
        print(f"\n⚠️  {len(findings)} stale path(s) found:")
        for f in findings:
            print(f"  {f['file']}:{f['line']} — \"{f['path']}\" (missing root: {f['missing_root']})")
    else:
        print("✅ No stale paths found.")
