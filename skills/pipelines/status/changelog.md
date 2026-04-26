# Skills/Pipelines/Projects Changelog

## [Unreleased]

## 2026-04-26 — Refactor Shared Asana Pipeline + Intelligence Harvest

**Files changed:**
- `orchestration/pipelines/asana/` — Created shared asana pipeline with run.py, 01_fetch_projects.py, 02_fetch_tasks.py, 03_normalize.py complete
- `orchestration/pipelines/status/scripts/03_harvest_asana_projects.py` — Updated to use shared asana cache complete
- `orchestration/pipelines/intelligence/scripts/` — Added 01_harvest.py and updated run.py complete

**Handoff:** `handoff/complete/2026-04-26-p1-Refactor:-Shared-Asana-Pipeline-+-Intelligence-Harvest-COMPLETE.md`

**Next:** Test the intelligence harvest script and ensure it fetches documents correctly

