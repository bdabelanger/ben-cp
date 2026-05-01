# Reports/Dream Changelog

## [Unreleased]

## 2026-04-26 — Restructure dream cycle — retire utilities/, establish orchestration/dream/ as first-class audit domain, wire sensors into daily-report.md

**Files changed:**
- `orchestration/dream/run.py` — New dream cycle master — runs all 11 sensors, consolidates output into daily-report.md + daily-report.html, writes dream_run.json run log new
- `orchestration/dream/sensors/` — Moved from orchestration/utilities/sensors/ — REPO_ROOT depth unchanged, no path fixes required moved
- `orchestration/utilities/` — Retired entirely — all report.py scripts were superseded by new sensor suite; dream.py absorbed into dream/run.py deleted
- `reports/dream/daily-report.md` — Now written by dream/run.py with sensor summary table, highlights, large files, and ghost links sample updated
- `reports/dream/daily-report.html` — HTML render of daily-report.md, co-written each run updated

**Next:** Build triage.py (or fold into dream/run.py) — Anthropic API call condensing sensor JSON into actionable summary

