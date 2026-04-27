---
title: Implementation Plan Integrate Legacy Platform Analytics into New Projects Engine
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Integrate Legacy Platform Analytics into New Projects Engine

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE

Refactored tools/product/projects/report.py to use the legacy PlatformStatusReport + render_html pipeline for generating the detailed project report. The script now attempts to import platform_report.py and render_html.py from the scripts/ sibling directory, and when Jira data is available (raw/jira_issues.json), generates the full data-rich HTML output — with project cards, Jira burndowns, milestone tracking, engineer data quality tables, and the sidebar — into the Gazette's reports/product-projects.html. Falls back to the simple Asana-only output if Jira data hasn't been harvested yet. The Gazette summary column remains concise (11 active projects) and the "Full Report" link now always lands on the best available data.

**Changelog:** (see root changelog.md)


---

The standardization of the `ben-cp` intelligence architecture successfully established a repo-local, autonomous reporting pipeline (The Daily Gazette). However, the new `product/projects` audit script (tools/product/projects/report.py) currently generates a bare-bones detailed report.

There is a "hidden" legacy engine at `tools/product/projects/scripts/platform_report.py` that contains 700+ lines of high-fidelity analytics, Jira synchronization logic, and project scorecard metrics.

**Task:**
1. Refactor the `product/projects` detailed report generation to utilize the logic from the legacy `platform_report.py`.
2. Ensure the Gazette summary remains concise (11 active projects audit).
3. Ensure the "Full Report" link in the Gazette lands on the data-rich output produced by the legacy logic.
