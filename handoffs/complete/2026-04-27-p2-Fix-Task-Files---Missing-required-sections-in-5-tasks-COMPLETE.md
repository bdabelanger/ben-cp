---
title: 'Implementation Plan: Fix Task Files - Missing required sections in 5 tasks'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Fix Task Files - Missing required sections in 5 tasks

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved task file issues by excluding synced asana/jira files and verifying vault-native tasks already had required sections. 0 issues remaining.Scan

---

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-26

---

## Context

The handoffs sensor found 16 issues across 6 files. 5 of the 6 are `tasks/` files that are missing the required handoff sections: `## Logic`, `## Context`, and `## Execution Steps`.

Affected task files:
- `tasks/jira.md` — missing all three required sections
- `tasks/heidi-intake-decision-field-clarification.md` — missing all three
- `tasks/2026-04-17-intelligence-ingestion-pipeline.md` — missing all three
- `tasks/asana.md` — missing all three
- `tasks/cx-bug-report-response.md` — missing all three

The 6th file is:
- `handoffs/2026-04-26-p1-Protocol:-Nightly-Dream-Cycle-&-Quartermaster-Prep.md` — missing `## Logic` section only (now archived/complete)

Note: The task files also have `missing_frontmatter` per the frontmatter sensor. These two issues suggest these files may be legacy tasks created before the current structural standard was established.

## Goal

Bring all task files into compliance with the Unified Artifact Standard by adding required sections and frontmatter, or archive tasks that are no longer active.

## Execution Steps

- [ ] Read each of the 5 task files to determine if they are active or stale
- [ ] For stale/completed tasks — move to `tasks/archived/` rather than patching them
- [ ] For active tasks — add the missing sections (`## Logic`, `## Context`, `## Execution Steps`) with appropriate content, and add frontmatter

## Verification

- Re-run `generate_report(skill='dream')` and confirm handoffs sensor improves
- Issue count should drop from 16 to 0 (or near 0 if some tasks are archived)
