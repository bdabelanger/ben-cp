---
title: Project Reporting Changelog
type: changelog
domain: skills/status
---

# Project Reporting Changelog

> Detail log for `skills/status/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-17 — Execute End-to-End Smoke Test for Local Agent Readiness

**Files changed:**
- `intelligence/product/projects/asana_field_definitions.md` — Created new intelligence record cataloging Asana GIDs from source data. COMPLETE

**Handoff:** `handoff/2026-04-17-p2-Gemma-Local-End-to-End-Smoke-Test.md`

**Next:** Review handoff completion by Cowork.


## 2026-04-16 — Jira Data Integrity & Reporting Pipeline Hardening

Resolved the data discrepancy issue where stale local caches were preventing accurate Jira issue counts.
- **Forced Fetch**: Modified `step_2_atlassian_fetch.py` to unconditionally fetch fresh data.
- **Pipeline Gating**: Updated `full_run.py` to always execute fetch and harvest phases.
- **Dream Report Fix**: Corrected data path in `tools/product/projects/report.py` to use fresh harvested data.
- **UI Enhancements**: Standardized external links to open in new tabs and restored the Asana icon.

## 2026-04-12 — Initial vault migration

Migrated project reporting skill components into vault.
