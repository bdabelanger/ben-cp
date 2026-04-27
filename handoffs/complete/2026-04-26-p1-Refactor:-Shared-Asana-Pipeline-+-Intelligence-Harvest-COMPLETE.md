---
title: Refactor Shared Asana Pipeline  Intelligence Harvest Step
type: handoff
domain: handoffs/complete
---

# Refactor: Shared Asana Pipeline + Intelligence Harvest Step

## Context

Currently `orchestration/pipelines/projects/scripts/01_fetch_asana_projects.py` fetches Asana data exclusively for the projects pipeline. The intelligence pipeline also needs Asana data (to find PRD links, launch plan links, Jira epic keys) but has no fetch step. Rather than duplicate the fetch, we want a shared Asana pipeline that fetches once and both downstream pipelines read from.

## Goal

1. Extract Asana fetching into `orchestration/pipelines/asana/` — a standalone shared pipeline
2. Both `projects` and `intelligence` pipelines read from its cached output
3. Add `01_harvest.py` to the intelligence pipeline that reads `sources` frontmatter from intelligence records and refreshes stale content by system

---

## Step 1 — Create shared `asana` pipeline

Create `orchestration/pipelines/asana/` with:

```
orchestration/pipelines/asana/
  scripts/
    01_fetch_projects.py    ← move from projects/scripts/01_fetch_asana_projects.py
    02_fetch_tasks.py       ← new: fetch tasks assigned to Ben (for intelligence queue)
    03_normalize.py         ← new: derive filtered views from raw cache
  run.py
  index.md
```

**Output locations** (update `reports/projects/data/` references accordingly):
```
reports/asana/
  raw/
    all_projects.json       ← was reports/projects/data/raw/asana_all_projects.json
    all_tasks.json          ← new
  processed/
    platform_projects.json  ← filtered for projects pipeline (Platform/Reporting/DevOps teams)
    intelligence_queue.json ← filtered for intelligence pipeline (projects with prd_link or confluence_link)
```

**Update `projects` pipeline:**
- `03_harvest_asana_projects.py` — change input path from `reports/projects/data/raw/asana_all_projects.json` → `reports/asana/raw/all_projects.json`
- `run.py` — call `orchestration/pipelines/asana/scripts/run.py` (or ensure cache is fresh) before step 03

**`intelligence_queue.json` filter criteria:**
- Projects where any of the following are non-null/non-empty: `prd_link`, `launch_plan_link`, or a `jira_link` containing `CBP-`

---

## Step 2 — Add `01_harvest.py` to intelligence pipeline

Create `orchestration/pipelines/intelligence/scripts/01_harvest.py`.

**What it does:**
1. Walk all `intelligence/**/*.md` files (excluding `source/`, `index.md`, changelogs)
2. Parse YAML frontmatter from each file
3. For records that have a `sources` block, check `last_fetched` for each entry
4. If stale (> 7 days) or `--force` passed, re-fetch by system:
   - `confluence` entries → use Atlassian API (same client as `10_push_confluence.py`) to fetch page by URL, save to `{record_dir}/source/{type}.html`
   - `asana` entries → read from `reports/asana/raw/all_projects.json` cache (no new API call needed)
   - `jira` entries → fetch epic + children from Jira API, save to `{record_dir}/source/{key}.json`
   - `google_drive` entries → log as "manual refresh required" (no automation yet)
5. Update `last_fetched` in frontmatter after successful fetch
6. Print summary: records checked, refreshed, skipped, failed

**Run signature:**
```bash
python3 orchestration/pipelines/intelligence/scripts/run.py --harvest          # refresh stale only
python3 orchestration/pipelines/intelligence/scripts/run.py --harvest --force  # refresh all
```

Update `run.py` to route `--harvest` flag to `01_harvest.py`.

**Renumber existing scripts:**
- `02_parse.py` stays as-is (parse is still step 2)
- `03_scan_orphans.py` stays as-is

---

## Step 3 — Migrate existing intelligence records to new frontmatter schema

Existing records in `intelligence/product/projects/q2/` have inline markdown fields (no YAML frontmatter). Migrate them to the new schema.

**Schema** (defined in `orchestration/pipelines/intelligence/schemas/source-to-intelligence-prompt.md`):

```yaml
---
title: [Title from # heading]
status: 🟡 Draft
date_ingested: YYYY-MM-DD   ← use file mtime if unknown
sources:
  asana:
    - type: project
      gid: "[GID from **GID:** field]"
      last_fetched: YYYY-MM-DD
  confluence:
    - type: prd
      url: "[url from prd_link if present]"
      last_fetched: YYYY-MM-DD
    - type: launch_plan
      url: "[url from launch_plan_link if present]"
      last_fetched: YYYY-MM-DD
  jira:
    - type: epic
      key: "[CBP-XXXX from **Jira Link:** field if present]"
      last_fetched: YYYY-MM-DD
---
```

**Migration script** (write once, run once): `orchestration/pipelines/intelligence/scripts/migrate_frontmatter.py`
- Parse each file's inline fields
- Build frontmatter from available fields
- Prepend frontmatter, preserve body
- Log any records that couldn't be auto-migrated (missing GID etc.)

---

## Step 4 — Update `index.md` for intelligence pipeline

After steps above are done, update `orchestration/pipelines/intelligence/index.md` to reflect the new pipeline stages:

| # | Script | Mode | What it does |
|---|--------|------|--------------|
| 01 | `01_harvest.py` | Automated | Walk intelligence records, refresh stale sources by system |
| 02 | `02_parse.py` | Agent-assisted | Apply LLM extraction schema to produce/update vault records |
| 03 | `03_scan_orphans.py` | Automated | Verify all source files have matching .md records |

---

## Verification

- [ ] `python3 orchestration/pipelines/asana/scripts/run.py` produces `reports/asana/raw/all_projects.json` and `reports/asana/processed/platform_projects.json`
- [ ] `python3 orchestration/pipelines/projects/scripts/run.py` still works end-to-end using new Asana cache path
- [ ] `python3 orchestration/pipelines/intelligence/scripts/run.py --harvest --force` refreshes at least one Confluence source and updates `last_fetched`
- [ ] `python3 orchestration/pipelines/intelligence/scripts/run.py --scan` still works
- [ ] At least 5 existing intelligence records migrated to new frontmatter schema
