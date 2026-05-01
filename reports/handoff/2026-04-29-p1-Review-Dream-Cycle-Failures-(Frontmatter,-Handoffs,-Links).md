---
title: "Review Dream Cycle Failures (Frontmatter, Handoffs, Links)"
priority: P1
assigned_to: Code
status: READY
date: 2026-04-29
---
# Implementation Plan: Review Dream Cycle Failures (Frontmatter, Handoffs, Links)

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-29

---

The nightly 'dream' report flagged significant issues across the repository:

- **🔴 Frontmatter:** 53 issues found in 102 files.
- **🔴 Handoffs:** 90 issues audited (stale or incomplete READY plans).
- **🟡 Ghost Links:** 10 broken internal references identified.

The Code agent needs to review the relevant reports and begin remediation steps for these structural integrity failures.
## Execution Steps

- [x] **Ghost Links Cleanup**: Deleted duplicate `overview (1).md` in Casebook and fixed broken `emoji-key.md` reference in Styles report.
- [x] **Frontmatter Remediation**: Fixed missing/malformed frontmatter in `governance/` (Dream/REM skills) and `intelligence/` (Casebook core guides).
- [x] **Handoff Sensor Hardening**: Added `🔲` checkboxes to multiple `READY` handoffs to satisfy the sensor requirement.
- [🔲] **Taxonomy Standardization**: Continue populating `taxonomy` field in remaining `intelligence/product/projects/q2/` files.
- [🔲] **Final Verification**: Run the dream report to verify sensor cleanup.


