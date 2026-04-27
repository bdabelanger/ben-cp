---
title: SkillsPipelines Changelog
type: changelog
domain: skills/pipelines
---

# Skills/Pipelines Changelog

## [Unreleased]

## 2026-04-26 — Fix Confluence ingestion pipeline, build unified task harvester, build 11-sensor dream suite, standardize pipeline naming convention

**Files changed:**
- `orchestration/pipelines/product/projects/pipeline/harvest_confluence_docs.py` — Fixed REPO_ROOT path bug (4→5 levels) — was silently failing every run; also fixed stale module import and added sys.exit(1) on fetch failure fixed
- `orchestration/pipelines/product/projects/pipeline/confluence_v2.py` — Fixed REPO_ROOT path bug (4→5 levels) causing missing .env credentials; added sys.exit(1) on failure for proper error surfacing fixed
- `orchestration/pipelines/tasks/pipeline/run.py` — New daily task harvester — fetches personal Asana tasks + Jira issues, writes asana.md and jira.md as daily wipe-and-rebuild snapshots new
- `orchestration/tasks/asana.md` — Daily snapshot of Asana tasks grouped by project new
- `orchestration/tasks/jira.md` — Daily snapshot of Jira issues grouped by project with priority/status inline new
- `orchestration/utilities/sensors/pulse.py` — New sensor — changelog staleness, boundary violations, index.md coverage new
- `orchestration/utilities/sensors/links.py` — New sensor — ghost link detection across all .md files new
- `orchestration/utilities/sensors/frontmatter.py` — New sensor — YAML frontmatter schema enforcement and readability checks new
- `orchestration/utilities/sensors/drift.py` — New sensor — unplanned directory growth vs sanctioned AGENTS.md structure new
- `orchestration/utilities/sensors/handoffs.py` — New sensor — handoff standards audit (sections, checkboxes, staleness) new
- `orchestration/utilities/sensors/index.py` — New sensor — shadow files and ghost refs vs index.md new
- `orchestration/utilities/sensors/agents.py` — New sensor — role compliance and AI assistant phrase detection new
- `orchestration/utilities/sensors/tasks.py` — New sensor — high-priority task staleness and broken project links new
- `orchestration/utilities/sensors/notes.py` — New sensor — notes.md entry format and staleness new
- `orchestration/utilities/sensors/changelog.py` — New sensor — version sequence integrity and subdirectory log coverage new
- `orchestration/utilities/sensors/context.py` — New sensor — file size audit for token economy (yellow >250KB, red >750KB) new
- `orchestration/utilities/dream.py` — New dream cycle orchestrator — runs all 11 sensors, logs timing and failures to dream_run.json new
- `orchestration/pipelines/product/projects/pipeline/` — Renamed all step_N scripts to verb_noun convention: fetch_asana_projects, harvest_asana_projects, fetch_jira_work_items, harvest_jira_work_items, harvest_confluence_docs, normalize_vault, generate_platform_status; full_run.py → run.py renamed
- `orchestration/pipelines/tasks/pipeline/` — Renamed harvest_tasks.py → run.py; established tasks pipeline as independent domain renamed

**Next:** Build triage.py — Anthropic API call condensing 11 sensor JSONs into TRIAGE_REPORT.md for Quartermaster

