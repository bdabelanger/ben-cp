---
title: 'Implementation Plan: Restore Task Capture Templates to Intelligence Domain'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Restore Task Capture Templates to Intelligence Domain

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2
> **STATUS**: ✅ COMPLETE

Successfully retrieved the missing Task Capture templates from the Claude session cache and deployed them to the canonical intelligence domain. Updated the skill documentation to ensure all procedures point to these new vault-native paths.

---

## Context

During the structural consolidation of the `projects` skill, it was discovered that the `references/` subdirectory (which was supposed to contain Task Capture templates) was empty. These files are required for the full execution of the Task Capture procedure but currently reside only in the runtime Cowork plugin at `.claude/skills/task-capture/references/`.

## Objective

Restore the following template files to the vault's unified intelligence domain at `intelligence/product/projects/source/`:

- `asana-custom-fields.md`
- `user-story-template.md`
- `task-template.md`
- `bug-template.md`
- `cx-bug-template.md`
- `research-template.md`

## Execution Steps

1. **Locate Source**: Read each file from the active Cowork plugin at `.claude/skills/task-capture/references/`.
2. **Deploy to Vault**: Create each file at `intelligence/product/projects/source/`.
3. **Update Index**: Mark "Pending Restoration" as complete in `skills/product/projects/index.md`.
4. **Consistency Check**: Verify that `skills/product/projects/procedure.md` correctly references the new paths.

## Notes

The Cowork plugin version must remain functional for runtime use. The vault copy is the canonical reference for logic and structure — keep them in sync.
