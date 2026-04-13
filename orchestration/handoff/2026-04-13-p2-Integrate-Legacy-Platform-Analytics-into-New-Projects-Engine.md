# Implementation Plan: Integrate Legacy Platform Analytics into New Projects Engine

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P2
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

The standardization of the `ben-cp` intelligence architecture successfully established a repo-local, autonomous reporting pipeline (The Daily Gazette). However, the new `product/projects` audit script (tools/product/projects/report.py) currently generates a bare-bones detailed report.

There is a "hidden" legacy engine at `tools/product/projects/scripts/platform_report.py` that contains 700+ lines of high-fidelity analytics, Jira synchronization logic, and project scorecard metrics.

**Task:**
1. Refactor the `product/projects` detailed report generation to utilize the logic from the legacy `platform_report.py`.
2. Ensure the Gazette summary remains concise (11 active projects audit).
3. Ensure the "Full Report" link in the Gazette lands on the data-rich output produced by the legacy logic.
