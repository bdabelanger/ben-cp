# Implementation Plan: Fix Task Files — Missing required sections in 5 tasks

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Superseded by 2026-04-27-p2-Fix-Task-Files---Missing-required-sections-in-5-tasks.md with clean filename.

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
- `handoffs/2026-04-26-p1-Protocol:-Nightly-Dream-Cycle-&-Quartermaster-Prep.md` — missing `## Logic` section only

Note: The task files also have `missing_frontmatter` per the frontmatter sensor. These two issues (no frontmatter + missing required sections) suggest these files may be legacy tasks created before the current structural standard was established.

## Goal

Bring all task files into compliance with the Unified Artifact Standard by adding required sections and frontmatter, or archive tasks that are no longer active.

## Execution Steps

1. Read each of the 5 task files to determine if they are active or stale
2. For stale/completed tasks — move to `tasks/archived/` rather than patching them
3. For active tasks — add the missing sections (`## Logic`, `## Context`, `## Execution Steps`) with appropriate content based on the existing file content, and add frontmatter
4. For `handoffs/2026-04-26-p1-Protocol:-Nightly-Dream-Cycle-&-Quartermaster-Prep.md` — add `## Logic` section describing the trigger/decision logic for the Dream Cycle protocol

## Verification

- Re-run `generate_report(skill='dream')` and confirm handoffs sensor improves
- Issue count should drop from 16 to 0 (or near 0 if some tasks are archived)
