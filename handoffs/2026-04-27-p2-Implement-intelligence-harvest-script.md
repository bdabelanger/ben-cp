---
title: "Implement skills/intelligence/01_harvest.py"
type: handoff
priority: P2
status: 🔲 READY
date: 2026-04-27
assigned_to: Code
---

# Implement skills/intelligence/01_harvest.py

## Context

`skills/intelligence/01_harvest.py` is currently a placeholder stub. It needs a real implementation so the dream cycle can refresh stale intelligence source files nightly.

The full spec was written in `handoffs/complete/2026-04-26-p1-Refactor:-Shared-Asana-Pipeline-+-Intelligence-Harvest-COMPLETE.md` (Step 2). That handoff was marked complete prematurely — the shared Asana pipeline was built but `01_harvest.py` was never implemented beyond a stub.

The dream cycle now calls `python3 skills/intelligence/run.py --harvest` as Step 9. It needs to actually do something.

## What it should do

1. Walk all `intelligence/**/*.md` files (exclude `source/`, `index.md`, changelogs)
2. Parse YAML frontmatter from each file
3. For records that have a `sources` block, check `last_fetched` for each entry
4. If stale (> 7 days) or `--force` passed, re-fetch by source type:
   - `confluence` → fetch page by URL via Atlassian API, save to `{record_dir}/source/{slug}.html`
   - `asana` → read from `reports/asana/data/raw/all_projects.json` cache (no new API call)
   - `jira` → fetch epic + children from Jira API, save to `{record_dir}/source/{key}.json`
   - `google_drive` → log as "manual refresh required" (skip, no automation yet)
5. Update `last_fetched` in frontmatter after successful fetch
6. Print summary: records checked, refreshed, skipped, failed

## Path configuration

```python
# skills/intelligence/01_harvest.py -> ../.. -> ben-cp/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTEL_DIR = os.path.join(REPO_ROOT, "intelligence")
ASANA_CACHE = os.path.join(REPO_ROOT, "reports", "asana", "data", "raw", "all_projects.json")
```

## Frontmatter schema to look for

```yaml
sources:
  confluence:
    - type: prd
      url: "https://casecommons.atlassian.net/wiki/..."
      last_fetched: 2026-04-01
  jira:
    - type: epic
      key: "CBP-XXXX"
      last_fetched: 2026-04-01
  asana:
    - type: project
      gid: "12345678"
      last_fetched: 2026-04-01
```

## API clients

Reuse the same Atlassian auth pattern already in `skills/status/scripts/`:
- `ATLASSIAN_USER_EMAIL` + `ATLASSIAN_API_TOKEN` from `.env`
- Confluence REST API v2: `GET /wiki/api/v2/pages/{id}` or fetch by URL
- Jira REST API: `GET /rest/api/3/issue/{key}` with `fields=summary,status,subtasks`

## Run signature

```bash
python3 skills/intelligence/run.py --harvest          # refresh stale only (>7 days)
python3 skills/intelligence/run.py --harvest --force  # refresh all records
```

## Execution Steps

- [ ] 1. Read `skills/intelligence/01_harvest.py` (current stub)
- [ ] 2. Read `skills/status/scripts/02_fetch_jira_work_items.py` — reuse Atlassian auth pattern
- [ ] 3. Implement `01_harvest.py` per spec above
- [ ] 4. Test: `python3 skills/intelligence/run.py --harvest --force` against at least one record with a `confluence` source
- [ ] 5. Verify `last_fetched` is updated in frontmatter after successful fetch
- [ ] 6. Run `python3 skills/dream/sensors/scripts.py` — confirm `intelligence` skill no longer flagged as stub
- [ ] 7. Add changelog entry to `skills/changelog.md`

## Verification

- `python3 skills/intelligence/run.py --harvest` runs without error
- At least one source file written to `intelligence/<domain>/<topic>/source/`
- `last_fetched` updated in corresponding record frontmatter
- `scripts` sensor reports 0 stub findings for intelligence skill
