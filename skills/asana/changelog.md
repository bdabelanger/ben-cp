---
title: Skills/Pipelines/Asana Changelog
type: changelog
domain: skills/asana
---


# Skills/Pipelines/Asana Changelog

## [Unreleased]

## 2026-04-27 — Build Task Capture MCP Tools from Skill

**Files changed:**
- `src/ben-cp.ts` — Added loadEnv() + httpsRequest() helpers; added 5 new MCP tools: capture_task, create_asana_project, create_asana_task, create_jira_issue, link_asana_jira ✅
- `dist/` — Rebuilt TypeScript compilation — clean build confirmed ✅

**Next:** Restart MCP server to pick up new tools


## 2026-04-26 — Update documentation and registry for new Asana pipeline

**Files changed:**
- `orchestration/pipelines/intelligence/index.md` — Updated pipeline stages table to include harvest step complete
- `orchestration/pipelines/asana/index.md` — Created new index for asana pipeline complete
- `ben-cp` — Rebuilt ben-cp complete

**Handoff:** `handoff/complete/2026-04-26-p2-Update:-Intelligence-Pipeline-index.md-and-ben-cp-Registry-COMPLETE.md`

**Next:** Verify Asana pipeline outputs


## 2026-04-26 — Refactor Shared Asana Pipeline + Intelligence Harvest

**Files changed:**
- `orchestration/pipelines/asana/` — Created shared asana pipeline with run.py, 01_fetch_projects.py, 02_fetch_tasks.py, 03_normalize.py complete
- `orchestration/pipelines/projects/scripts/03_harvest_asana_projects.py` — Updated to use shared asana cache complete
- `orchestration/pipelines/intelligence/scripts/` — Added 01_harvest.py and updated run.py complete

**Handoff:** `handoff/complete/2026-04-26-p1-Refactor:-Shared-Asana-Pipeline-+-Intelligence-Harvest-COMPLETE.md`

**Next:** Test the intelligence harvest script and ensure it fetches documents correctly

