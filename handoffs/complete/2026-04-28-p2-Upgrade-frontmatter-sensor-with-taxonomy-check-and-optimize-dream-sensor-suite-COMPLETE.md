# Implementation Plan: Upgrade frontmatter sensor with taxonomy check and optimize dream sensor suite

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

Successfully implemented taxonomy validation for intelligence files in frontmatter.py. Optimized the dream sensor suite by deduplicating collect_md_files(), standardizing SKIP_DIRS, and moving imports to the module level. Fixed a sys.path issue in run.py that prevented sensors from importing sibling utilities. Verified with a full dream suite run (13/13 sensors OK).

---

## Context

The dream sensor suite runs nightly across all repo files. Two categories of work here:

1. **New check** — `frontmatter.py` needs a `taxonomy` validation check now that intelligence files carry a `taxonomy:` frontmatter field
2. **Optimizations** — several sensors walk the filesystem independently; shared logic and minor bugs identified

All changes are in `skills/dream/scripts/`. Run `python3 skills/dream/run.py` to verify after.

---

## Part 1 — frontmatter.py: Add Taxonomy Check

### What to add

A new check in `frontmatter.py`'s `run()` loop that validates the `taxonomy` field on intelligence files.

**Rules:**
- Only applies to files under `intelligence/` (skip all other paths)
- If `taxonomy` key is absent: issue `missing_taxonomy`
- If `taxonomy` value is `"none"` (the sentinel for cross-cutting projects like Accessibility, Web Applications): valid, no issue
- If `taxonomy` value is non-empty: validate each comma-separated term against the canonical taxonomy
  - Load valid terms from `intelligence/casebook/taxonomy.md` — extract all Product and Feature names from the Products and Features tables
  - If any term doesn't match a known product or feature (case-insensitive): issue `unknown_taxonomy_term` with the offending term(s)
- Skip `index.md`, `changelog.md`, `taxonomy.md` itself

### Taxonomy loader

```python
def load_taxonomy_terms():
    """Return set of valid taxonomy labels from intelligence/casebook/taxonomy.md."""
    path = os.path.join(REPO_ROOT, 'intelligence', 'casebook', 'taxonomy.md')
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
                if row.startswith('|') and '---' not in row and ('| Product |' not in row) and ('| Feature |' not in row):
                    label = row.split('|')[1].strip()
                    if label:
                        terms.add(label.lower())
    # Also add combined labels like "Cases - Notes", "Admin - Audit Log"
    # These appear in the inference map — extract `backtick` values
    for m in re.finditer(r'`([^`]+)`', content):
        val = m.group(1)
        if ' — ' not in val and val != '*(omit label; do not guess)*':
            terms.add(val.lower())
    return terms
```

### Issue objects to add

```python
# Missing taxonomy on an intelligence file
{"file": rel, "issue": "missing_taxonomy"}

# Unknown term in taxonomy value
{"file": rel, "issue": "unknown_taxonomy_term", "terms": ["Bad Term"]}
```

### Where to call it

In the main `run()` loop, after the existing field presence check, add:

```python
# Taxonomy check — intelligence files only
if rel.startswith('intelligence/') and os.path.basename(path) not in {'index.md', 'changelog.md', 'taxonomy.md'}:
    taxonomy_val = fm_data.get('taxonomy') if isinstance(fm_data, dict) else None
    if taxonomy_val is None:
        issues.append({"file": rel, "issue": "missing_taxonomy"})
    elif str(taxonomy_val).strip().lower() != 'none':
        terms = [t.strip() for t in str(taxonomy_val).split(',')]
        unknown = [t for t in terms if t.lower() not in taxonomy_terms and not any(t.lower() in combo for combo in taxonomy_terms)]
        if unknown:
            issues.append({"file": rel, "issue": "unknown_taxonomy_term", "terms": unknown})
```

Load `taxonomy_terms` once at the top of `run()` before the file loop:
```python
taxonomy_terms = load_taxonomy_terms()
```

---

## Part 2 — Optimizations

### 2a. Deduplicate `collect_md_files()` — frontmatter.py and links.py

Both define identical `collect_md_files()` functions. Extract to a shared utility.

Create `skills/dream/scripts/utils.py`:

```python
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports',
             'art', 'complete', 'archive', 'archived'}

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
```

Then in `frontmatter.py` and `links.py`:
```python
from utils import collect_md_files
```

Note: `links.py` has a slightly different `SKIP_DIRS` (includes `archived` but not `src` or `reports`) — use the links.py set for links, frontmatter.py set for frontmatter. Pass `skip_dirs` explicitly.

### 2b. SKIP_DIRS inconsistency

Each sensor defines its own `SKIP_DIRS`. They drift from each other — `frontmatter.py` skips `src` and `reports`, `links.py` doesn't. This means links.py may scan report outputs and find ghost links to nowhere.

Fix `links.py` SKIP_DIRS to match frontmatter.py and add `reports`:
```python
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'src', 'reports',
             'archived', 'archive', 'complete'}
```

### 2c. frontmatter.py — `parse_frontmatter` imports yaml inside function

```python
def parse_frontmatter(content):
    import yaml  # ← import inside function, called per-file
```

Move `import yaml` to module top-level. Minor but called once per `.md` file.

### 2d. links.py — `import urllib.parse` inside function

Same pattern — `urllib.parse` imported inside `extract_links()` which is called per file. Move to top-level.

### 2e. context.py — `import urllib.parse` inside `is_acknowledged()`

Same — move to top-level.

### 2f. drift.py — sanctioned dir loading is fragile

`load_sanctioned_dirs()` regex-parses the directory tree from `AGENTS.md`. If the tree block format changes, it silently returns an empty set, causing every root dir to flag as unsanctioned.

Add a fallback warning when the set is empty:
```python
sanctioned = load_sanctioned_dirs()
if not sanctioned:
    print("⚠️  drift: could not load sanctioned dirs from AGENTS.md — skipping root scan")
    return []  # don't flag everything
```

### 2g. frontmatter.py — `VALID_TYPES` is missing some types

Current set:
```python
VALID_TYPES = {'index', 'skill', 'intelligence', 'handoff', 'changelog', 'release',
               'prd', 'agent', 'task', 'report', 'log', 'session', 'launch_plan'}
```

Missing types seen in the wild: `launch_plan` is present but `run_log`, `shareout`, `source` are not. Add:
```python
'run_log', 'shareout', 'source', 'reference'
```

---

## Verification Checklist

- [ ] `python3 skills/dream/scripts/frontmatter.py` runs without error
- [ ] A file with `taxonomy: Notes` does not generate an issue
- [ ] A file with `taxonomy: BadTerm` generates `unknown_taxonomy_term`
- [ ] A file with `taxonomy: none` generates no issue
- [ ] An intelligence file with no `taxonomy` key generates `missing_taxonomy`
- [ ] `python3 skills/dream/run.py` completes with frontmatter sensor green or expected issues only
- [ ] No regression on links sensor (SKIP_DIRS change)
