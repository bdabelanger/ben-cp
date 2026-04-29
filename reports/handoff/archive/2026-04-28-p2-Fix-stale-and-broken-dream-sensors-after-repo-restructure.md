# Implementation Plan: Fix stale and broken dream sensors after repo restructure

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

Audit of all `skills/dream/scripts/` sensors found several issues needing fixes. All changes in `skills/dream/`.

## Issue 1 — handoffs.py missing

`run.py` lists `handoffs` in SENSORS but `skills/dream/scripts/handoffs.py` doesn't exist — dream cycle fails.

Create `skills/dream/scripts/handoffs.py`:
- Walk `reports/handoff/`, skip `index.md`, `.keep`, `complete/`
- Parse YAML frontmatter from each file
- Flag: missing required keys (`title`, `priority`, `assigned_to`, `status`, `date`), malformed frontmatter, READY handoffs older than 14 days
- Output: `reports/dream/data/raw/handoffs_report.json`
- Sensor name: `"handoffs"`

## Issue 2 — index.py dead code

Has `audit_directory()` function with full subdirectory cross-reference logic despite comment saying "Only audit root index.md now."

Remove `audit_directory()`. Inline root-only logic in `run()`:
- Ghost refs: links in root `index.md` that don't resolve on disk
- Shadow files: `.md` files in repo root not mentioned in `index.md` (skip: `changelog.md`, `AGENTS.md`, `README.md`)

Update `skills/dream/SKILL.md` sensor table:
```
| index | dream/index_report.json | Ghost refs and shadow files in root index.md |
```

## Issue 3 — tasks.py is a no-op

References non-existent `tasks/` directory. Repurpose to audit `reports/tasks/report.md`:
- Flag if report missing
- Flag if older than 48 hours
- Count overdue tasks (lines with past due dates)

```python
TASKS_REPORT = os.path.join(REPO_ROOT, 'reports', 'tasks', 'report.md')
```

## Issue 4 — agents.py over-broad index.md skip

```python
# Before
if rel == 'AGENTS.md' or rel.endswith('index.md'):
# After
if rel in ('AGENTS.md', 'index.md'):
```

## Issue 5 — reindex.py taxonomy path

Update in same commit as taxonomy move handoff (Move taxonomy.md to intelligence root):
```python
path = os.path.join(REPO_ROOT, 'intelligence', 'taxonomy.md')
```

## Verification
- [ ] `python3 skills/dream/scripts/handoffs.py` runs, writes handoffs_report.json
- [ ] `index.py` simplified, audit_directory() removed
- [ ] `tasks.py` reads reports/tasks/report.md
- [ ] `agents.py` skip updated
- [ ] `python3 skills/dream/run.py` completes without sensor failures
