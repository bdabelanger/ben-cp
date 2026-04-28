# Implementation Plan: Restructure dream sensors - merge bloat, links-paths, fix handoff, move intelligence-scan, remove tasks

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

Six sensor cleanup tasks. All in `skills/dream/`.

## Change 1 — Merge access.py + context.py → bloat.py

Combine into one sensor covering all size tiers + git touches:
- Yellow: >250KB (token economy warning)
- Red: >750KB (token economy risk)
- Critical: >10MB (resource bloat)
- Recent touches: files changed in last 24h via git

Report shape:
```python
{"sensor": "bloat", "summary": {"critical_flags": N, "red_flags": N, "yellow_flags": N, "files_touched_24h": N},
 "critical_flags": [...], "red_flags": [...], "yellow_flags": [...], "recent_touches": [...]}
```

Drop `is_acknowledged()` index.md check (index files retired). Output: `bloat_report.json`. Delete `access.py` and `context.py`.

## Change 2 — Merge paths.py into links.py

Add `check_stale_paths()` (ported from `paths.py`) to `links.py` as a second check. Combined report:
```python
{"sensor": "links", "summary": {"files_scanned": N, "ghost_links": N, "stale_paths": N},
 "ghost_links": [...], "stale_paths": [...]}
```
Delete `paths.py`.

## Change 3 — Move intelligence-scan to sensor

Create `skills/dream/scripts/intelligence.py`:
- Run `skills/intelligence/run.py --scan` as subprocess
- Parse stdout for findings
- Output: `intelligence_report.json`

Remove `intelligence-scan` from PIPELINES in `run.py`. Add `'intelligence'` to SENSORS list (after `scripts`).

## Change 4 — Remove tasks sensor

Delete `tasks.py`. Remove `'tasks'` from SENSORS list.

## Change 5 — Fix handoff sensor load path

Move `skills/handoff/run.py` → `skills/dream/scripts/handoffs.py`. Fix content:
- `HANDOFF_DIR = os.path.join(REPO_ROOT, 'reports', 'handoff')` (already correct path, was pointing there)
- Remove `TASKS_DIR` reference
- Rename sensor to `"handoffs"` (plural)
- Use frontmatter for required field checks instead of prose section checks
- Stale threshold: 14 days (not 72h)

Remove special-case in `load_sensor()` that loaded from `skills/handoff/run.py`. All sensors now load from `skills/dream/scripts/`.

## Change 6 — Update run.py SENSORS list

```python
SENSORS = [
    'reindex', 'pulse', 'links', 'frontmatter', 'drift',
    'handoffs', 'index', 'agents',
    'bloat', 'changelog', 'intelligence',
    'scripts',
]
```

Update `build_highlights()`: replace `context`/`access` refs with `bloat`. Update `skills/dream/SKILL.md` sensor table.

## Verification
- [ ] `bloat.py` runs; `access.py` and `context.py` deleted
- [ ] `links.py` includes stale path check; `paths.py` deleted
- [ ] `tasks.py` deleted, removed from SENSORS
- [ ] `handoffs.py` in `skills/dream/scripts/`, reads from `reports/handoff/`
- [ ] `load_sensor()` no longer special-cases handoff
- [ ] `intelligence.py` sensor runs `--scan`
- [ ] `intelligence-scan` removed from PIPELINES
- [ ] `python3 skills/dream/run.py` completes without failures
