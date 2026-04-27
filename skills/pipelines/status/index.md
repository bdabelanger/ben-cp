---
title: projects pipeline
type: index
domain: skills/pipelines/status
---

# projects pipeline

Fetches, processes, and publishes the **Platform Weekly Status Report** — a comprehensive view of all active Platform team projects, their Jira health, milestone progress, and readiness status.

## What it produces

- `reports/projects/report.html` — self-contained HTML report with project cards, readiness bars, milestone tracking, and data quality analytics
- `reports/projects/report.md` — markdown source (consumed by HTML renderer and archived for agent access)
- `intelligence/product/reports/latest-platform-status.md` — agent-accessible copy of the latest report
- `intelligence/product/projects/q2/{slug}/` — per-project Confluence docs (PRD, Launch Plan) harvested for intelligence

## Pipeline stages

| # | Script | What it does |
|---|--------|--------------|
| 01 | `01_fetch_asana_projects.py` | Pulls all active projects from Asana API → `data/raw/asana_all_projects.json` |
| 02 | `02_fetch_jira_work_items.py` | Fetches Jira child issues for each linked CBP-* epic → `data/raw/jira/*.json` |
| 03 | `03_harvest_asana_projects.py` | Filters by team/stage, enriches with milestone data and status HTML → `data/processed/asana_active.json` |
| 04 | `04_harvest_jira_work_items.py` | Deduplicates and normalizes Jira issues, applies status overrides → `data/processed/jira_issues.json` |
| 05 | `05_harvest_confluence_docs.py` | Downloads PRD and Launch Plan docs from Confluence into intelligence vault |
| 06 | `06_generate_platform_status.py` | Legacy report generator (superseded by 07) |
| 07 | `07_build_report.py` | Core report builder — renders project cards, readiness/progress/time bars, milestone flags |
| 08 | `08_render_html.py` | Converts markdown report to self-contained HTML with inline CSS and visualizations |
| 09 | `09_push_asana_corrections.py` | Pushes corrected milestone dates back to Asana (dry-run by default, `--execute` to commit) |
| 10 | `10_push_confluence.py` | Fetches Confluence pages by ID or URL; used by harvest step |
| 99 | `99_normalize_vault.py` | Post-harvest cleanup — merges duplicate project directories, moves files to `index.md` |

**Utilities:**
- `run.py` — orchestrates all stages in sequence; supports `--force` (wipe Jira cache), `--team <name>`, and target GID args
- `update_manifest.py` — tracks step status and file paths in `data/manifest.json`; `reset` archives old outputs
- `generate_rovo_context.py` — stub for future Rovo/Atlassian search integration (currently returns placeholder data)
- `jira_setup.md` — agent guide for manually populating Jira raw data via MCP tools

## Data flow

```
Asana API → 01_fetch → 03_harvest ──────────────────────────────────────┐
                                                                         ↓
Jira API  → 02_fetch → 04_harvest ──────────────────── 07_build_report → 08_render_html
                                                                         ↓
Confluence → 05_harvest → intelligence/product/projects/q2/          report.html
                          99_normalize_vault
```

## How to run

```bash
# From vault root (ben-cp/)
# Full fresh run — wipes stale Jira cache
python3 skills/pipelines/status/scripts/run.py --force

# Re-render with cached Jira data
python3 skills/pipelines/status/scripts/run.py

# Filter to one team
python3 skills/pipelines/status/scripts/run.py --team platform
```

Requires `ASANA_API_TOKEN`, `ATLASSIAN_USER_EMAIL`, and `ATLASSIAN_API_TOKEN` in `.env` at vault root.

## Report structure

Each project card in the report includes:
- **Status** — Asana status update (On Track / At Risk / Off Track)
- **Stage** — current lifecycle stage (Discovery, Build, Beta, GA, etc.)
- **Milestones** — Beta Start, GA Target with date and completion status
- **Readiness bar** — Jira issues bucketed by state (Done / Aligned / Stalled / Lagging / Unmapped)
- **Progress bar** — story points completed vs. estimated
- **Time bar** — calendar progress against milestone window
- **Risk flags** — auto-raised when milestones are missing, overdue, or issues are unmapped

## Accessing via ben-cp

```
list_reports          → shows all available reports including this pipeline's output
get_report(projects)  → returns latest platform status report with pipeline context
```
