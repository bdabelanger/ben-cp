# Implementation Plan: Wire reindex sensor into dream cycle and share manifest with other sensors

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

Merged into 2026-04-28-p2-Make-list-and-search-tools-frontmatter-native-and-retire-index.md-dependency.md — Part 3 covers all reindex wiring tasks.

---

## Context

`reindex.py` has been written and placed at `skills/dream/scripts/reindex.py`. It walks the entire repo, parses frontmatter from every `.md` file, validates taxonomy terms, and:

1. Writes a full manifest JSON to `reports/dream/data/raw/reindex_report.json`
2. Updates the auto-generated stats block at the bottom of root `index.md`

The manifest is the ground truth other sensors should reference instead of walking the filesystem independently.

**Root `index.md`** has been authored at `index.md` — it's the single human-readable map of the repo. The reindex sensor keeps its stats footer current. The hand-authored tree sections above the `---` divider are never touched by the script.

---

## Task 1 — Wire reindex into run.py as the first sensor

In `skills/dream/run.py`, add `'reindex'` as the **first entry** in the `SENSORS` list:

```python
SENSORS = [
    'reindex',   # ← add here, must run first
    'pulse', 'links', 'frontmatter', 'drift',
    'handoffs', 'index', 'agents',
    'tasks', 'changelog', 'context', 'access',
    'paths', 'scripts',
]
```

Add it to the sensor table in `skills/dream/SKILL.md`:

```
| reindex | `dream/reindex_report.json` | Walks repo, validates frontmatter + taxonomy, regenerates root index.md |
```

---

## Task 2 — Update `frontmatter.py` to read from reindex manifest

`frontmatter.py` currently walks the filesystem itself and parses frontmatter per file. Now that reindex runs first and writes a full manifest, frontmatter should consume that instead of re-walking.

```python
def run():
    manifest_path = os.path.join(OUTPUTS_DIR, 'reindex_report.json')
    try:
        with open(manifest_path) as f:
            reindex = json.load(f)
        files = reindex['manifest']['files']
    except (OSError, KeyError):
        # Fallback: run own walk if reindex hasn't run yet
        files = walk_and_parse_own()

    issues = []
    for rel, meta in files.items():
        if not meta['has_frontmatter']:
            issues.append({"file": rel, "issue": "missing_frontmatter"})
        # ... rest of existing checks using meta['type'], meta['taxonomy']
```

This eliminates the duplicate filesystem walk and makes frontmatter.py ~10x faster on large repos.

The taxonomy validation already done by reindex (`unknown_taxonomy_terms`) can be consumed directly — no need to re-validate in frontmatter.py.

---

## Task 3 — Update `links.py` to use reindex file list

`links.py` walks the filesystem to collect `.md` files before checking links. Replace with:

```python
manifest_path = os.path.join(OUTPUTS_DIR, 'reindex_report.json')
try:
    with open(manifest_path) as f:
        reindex = json.load(f)
    md_files = [os.path.join(REPO_ROOT, p) for p in reindex['manifest']['files'].keys()]
except (OSError, KeyError):
    md_files = collect_md_files()  # fallback
```

---

## Task 4 — Add reindex to dream report summary

In `run.py`'s `build_highlights()`, add a highlight for reindex findings:

```python
if name == 'reindex' and data['status'] != 'FAILED':
    r = data['report']
    missing = r.get('summary', {}).get('frontmatter_missing', 0)
    unknown = r.get('summary', {}).get('unknown_taxonomy_terms', 0)
    if missing > 0:
        lines.append(f'- **{missing} files** missing frontmatter')
    if unknown > 0:
        lines.append(f'- **{unknown} files** with unknown taxonomy terms')
```

Also add a row to the sensor status table logic in `sensor_status_line()` — `reindex` uses `issues_found` in summary for the finding count (same pattern as frontmatter).

---

## Task 5 — Update root index.md `updated` frontmatter date

`reindex.py` regenerates the stats block but doesn't update the `updated:` field in the frontmatter header. Add this to `regenerate_index()`:

```python
# Update the updated: field in frontmatter
today = datetime.now().strftime('%Y-%m-%d')
updated = re.sub(r'^updated:.*$', f'updated: {today}', updated, flags=re.MULTILINE)
```

---

## Verification Checklist

- [ ] `python3 skills/dream/scripts/reindex.py` runs without error
- [ ] `reports/dream/data/raw/reindex_report.json` is written with `manifest.files`, `manifest.directories`
- [ ] `index.md` footer stats block is updated after run
- [ ] `python3 skills/dream/run.py` runs reindex first and completes without error
- [ ] `frontmatter.py` reads from reindex manifest (no duplicate walk)
- [ ] `links.py` uses reindex file list
- [ ] Dream report highlights section includes reindex findings
- [ ] `index.md` `updated:` frontmatter field reflects today's date after run
