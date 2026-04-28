---
title: Skills/Dream Changelog
type: changelog
domain: skills/dream
---


# Skills/Dream Changelog

## [Unreleased]

## 2026-04-27 — Restructure dream reports to standard data hierarchy.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/dream/Scan

**Files changed:**
- `reports/dream/` — Restructured report directory to follow standard data hierarchy. COMPLETE
- `skills/dream/sensors/` — Updated output paths for all 13 sensors to reports/dream/data/raw/. COMPLETE
- `skills/dream/run.py` — Updated orchestrator to write run log to data/raw/ and updated internal path logic. COMPLETE

**Next:** Monitor dream run for any path issues in external tools (though MCP server check passed)


## 2026-04-27 — Complete three handoffs (Link Standardization, Large File Convention, JSON Archive Retention) and improve Dream Sensor health.

**Files changed:**
- `intelligence/` — Standardized link headers to `## Links` across 11 `index.md` files in the repo. DONE
- `skills/dream/sensors/context.py` — Introduced the large file flag convention `_(SIZE)_` and an `IGNORE_LIST` in `context.py`. Applied the convention to Q2 Shareout source index. DONE
- `skills/status/scripts/update_manifest.py` — Created `retention_policy.md` enforcing a 7-day TTL on JSON archives. Implemented `cleanup_old_archives` in `update_manifest.py` and purged >50 expired JSON files. DONE
- `skills/dream/sensors/links.py` — Fixed links sensor parsing to handle URL decoding and angle brackets cleanly, eliminating false-positive ghost links. DONE

**Next:** Review remaining ghost links and broken index files if any.

## 2026-04-26 — Restructure dream cycle — retire utilities/, establish orchestration/dream/ as first-class audit domain, wire sensors into daily-report.md

**Files changed:**
- `orchestration/dream/run.py` — New dream cycle master — runs all 11 sensors, consolidates output into daily-report.md + daily-report.html, writes dream_run.json run log new
- `orchestration/dream/sensors/` — Moved from orchestration/utilities/sensors/ — REPO_ROOT depth unchanged, no path fixes required moved
- `orchestration/utilities/` — Retired entirely — all report.py scripts were superseded by new sensor suite; dream.py absorbed into dream/run.py deleted
- `reports/dream/daily-report.md` — Now written by dream/run.py with sensor summary table, highlights, large files, and ghost links sample updated
- `reports/dream/daily-report.html` — HTML render of daily-report.md, co-written each run updated

**Next:** Build triage.py (or fold into dream/run.py) — Anthropic API call condensing sensor JSON into actionable summary

