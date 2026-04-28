# Implementation Plan: Upgrade frontmatter sensor with taxonomy check and optimize dream sensor suite

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

Several dream sensor optimizations identified. All changes in `skills/dream/scripts/`.

## 1 — Create `utils.py` (shared helpers)

```python
# skills/dream/scripts/utils.py
import os, json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports', 'art', 'complete', 'archive', 'archived'}

def collect_md_files(root=None, skip_dirs=None):
    root = root or REPO_ROOT
    skip = skip_dirs or SKIP_DIRS
    files = []
    for dirpath, dirs, fs in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip and not d.startswith('.')]
        for f in fs:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return files

def get_manifest():
    path = os.path.join(REPO_ROOT, 'reports', 'dream', 'data', 'raw', 'reindex_report.json')
    try:
        with open(path) as f:
            return json.load(f).get('manifest', {})
    except: return {}

def get_manifest_files():
    manifest = get_manifest()
    if manifest:
        return [os.path.join(REPO_ROOT, f) for f in manifest.get('files', {}).keys()]
    return collect_md_files()
```

## 2 — frontmatter.py: add taxonomy validation

Add `load_taxonomy_terms()` function (reads from `intelligence/casebook/taxonomy.md`, extracts product/feature names). In the main `run()` loop, for files under `intelligence/`:

```python
taxonomy_val = fm_data.get('taxonomy') if isinstance(fm_data, dict) else None
if taxonomy_val is None:
    issues.append({"file": rel, "issue": "missing_taxonomy"})
elif str(taxonomy_val).strip().lower() != 'none':
    terms = [t.strip() for t in str(taxonomy_val).split(',')]
    unknown = [t for t in terms if t.lower() not in taxonomy_terms]
    if unknown:
        issues.append({"file": rel, "issue": "unknown_taxonomy_term", "terms": unknown})
```

Skip `index.md`, `changelog.md`, `taxonomy.md`.

## 3 — Fix SKIP_DIRS inconsistency

`links.py` currently scans `src/` and `reports/` — add both to its SKIP_DIRS:
```python
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports', 'archived', 'archive', 'complete'}
```

## 4 — Move top-level imports

In `frontmatter.py`: move `import yaml` to module top-level (currently inside `parse_frontmatter()`).
In `context.py`: `import urllib.parse` already at top — confirm `links.py` and `index.py` match.

## 5 — drift.py: add fallback guard

In `load_sanctioned_dirs()`, if result is empty set, print warning and return early from `scan_root_dirs()`:
```python
sanctioned = load_sanctioned_dirs()
if not sanctioned:
    print("⚠️  drift: could not load sanctioned dirs from AGENTS.md — skipping root scan")
    return []
```

## 6 — frontmatter.py: expand VALID_TYPES

Add: `'run_log', 'shareout', 'source', 'reference', 'overview'`

## Verification
- [ ] `python3 skills/dream/scripts/frontmatter.py` runs without error
- [ ] Intelligence file with `taxonomy: Notes` — no issue
- [ ] Intelligence file with `taxonomy: BadTerm` — `unknown_taxonomy_term` issue
- [ ] Intelligence file with `taxonomy: none` — no issue
- [ ] Intelligence file missing `taxonomy` — `missing_taxonomy` issue
- [ ] `links.py` no longer scans `reports/` or `src/`
