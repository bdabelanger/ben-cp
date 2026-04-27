# Implementation Plan: Dream Report

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Ben
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

*The vault dreamed last night. Here is what it saw.*

---

## Sensor Status

| Sensor | Status | Detail |
|---|---|---|
| pulse | 🟢 | clean |
| links | 🔴 | 10 ghost links across 6 files |
| frontmatter | 🔴 FAILED | `No module named 'yaml'` — sensor blind |
| drift | 🟢 | clean |
| handoffs | 🟢 | 2 files, 0 issues |
| index | 🟡 | 5 shadow files, 3 ghost refs |
| agents | 🔴 | 2 false positives (sensor bug) |
| tasks | 🟢 | clean |
| changelog | 🟡 | 15 subdirectory changelogs, 0 issues |
| context | 🟡 | 1 yellow flag — `jira_issues.json` at 536KB |
| access | 🟡 | 600 files touched in 24h |
| paths | 🟢 | clean |
| scripts | 🔴 | 5 warnings — missing script refs in status/asana |

---

## The Dreamscape

*The links sensor moved through the vault like someone reading a library in low light — tracing each reference with a finger, finding ten threads that led nowhere. Some were merely mislabeled doors: a path that once went somewhere real, clipped mid-word into silence. Two entries in `schema_joins.md` terminated at `/Users/benbelanger/My` — a sentence the file forgot to finish. The `skills/index.md` reached for `utilities/` and found only air.*

> **Sensor:** links · **Status:** 🔴 · **Findings:** 10 ghost links across `intelligence/casebook/reporting/schema_joins.md`, `intelligence/product/projects/index.md`, `intelligence/governance/policy.md`, `skills/index.md`, `skills/status/scripts/index.md`, `skills/styles/report.md`, `reports/status/data/raw/index.md`

---

*The frontmatter sensor never woke up. It tried — the run script called for it — but it opened its eyes into darkness and reported only a single word: `yaml`. The module wasn't there. It has been missing since before this run; no one noticed because no findings were being raised either. The sensor has been a closed eye for an unknown number of cycles.*

> **Sensor:** frontmatter · **Status:** 🔴 FAILED · **Findings:** `No module named 'yaml'` — PyYAML not installed in the sensor environment. All frontmatter auditing has been suspended.

---

*The agents sensor found two figures standing in doorways with the wrong names on their badges. It flagged them: `invalid_agent_format`. But looking closer, these were not agents — they were index files holding schema templates, showing what a proper agent record looks like. The sensor had mistaken the illustration for the thing itself. A map marked "this is not a map" read as a real map.*

> **Sensor:** agents · **Status:** 🔴 · **Findings:** 2 false positives — `agents/sessions/index.md` and `agents/logs/index.md` flagged for YAML code block content, not live frontmatter. Sensor logic needs update.

---

*The index sensor counted five shadows — files that exist but cast no reflection in their directory indexes. Three were agent role files (`cowork.md`, `local.md`, `code.md`) standing outside the `agents/index.md` roster. Two were handoffs created yesterday, unregistered. They are real files, doing real work, invisible to the index.*

> **Sensor:** index · **Status:** 🟡 · **Findings:** 5 shadow files (3 in `agents/`, 2 in `handoffs/`), 3 ghost refs

---

*The scripts sensor walked through five skills and found five hallways where doors had been sketched but never built. `run.py` in the status skill called for `full_run.py` — it isn't there. The asana skill's orchestrator called for three numbered scripts — none exist at the paths expected. These are references to a future that was planned but not yet built, or a past that was moved without updating the map.*

> **Sensor:** scripts · **Status:** 🔴 · **Findings:** 5 missing script refs — `skills/status/run.py` → `full_run.py`; `skills/asana/run.py` → `01_fetch_projects.py`, `02_fetch_tasks.py`, `03_normalize.py`. (A handoff for this was already created in a prior run today.)

---

## What Was Fixed (Bucket A)

*Nothing was corrected directly this cycle.* The agents sensor findings are false positives (sensor bug, not file bugs). The ghost link corrections and index gaps require multi-file changes — routed to Code.

---

## Handoffs Created for Code (Bucket B)

- `2026-04-27-p1-Fix-Frontmatter-Sensor-Yaml-Dependency.md` — install PyYAML, restore sensor
- `2026-04-27-p2-Fix-Ghost-Links-Across-Vault.md` — resolve all 10 ghost links
- `2026-04-27-p3-Fix-Agents-Sensor-False-Positives-and-Shadow-File-Index-Gaps.md` — fix sensor logic + register shadow files in indexes

*Pre-existing from today's earlier run:*
- `2026-04-27-p3-Fix-script-ref-issues-flagged-by-scripts-sensor.md`
- `2026-04-27-p3-Restructure-reports-dream-nest-sensor-data.md`

---

## Notable Observations

- **`jira_issues.json` at 536KB** — below the 750KB red flag threshold but worth watching. If the status pipeline runs more frequently, this file will grow. No action needed today.
- **Frontmatter sensor has been blind for an unknown number of cycles** — this is the higher-priority fix. We have no audit coverage of frontmatter quality across 476 files.
- **15 subdirectory changelogs** — this is informational, not a problem. The changelog sensor found no version issues or unlogged changes.
- **600 files touched in 24h** — high activity day. No anomalies flagged by the access sensor.
