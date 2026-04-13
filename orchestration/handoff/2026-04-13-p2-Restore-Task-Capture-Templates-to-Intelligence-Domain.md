# Implementation Plan: Restore Task Capture Templates to Intelligence Domain

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P2
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

# Handoff: restore-task-capture-templates

> **Prepared by:** Antigravity (2026-04-13)
> **Assigned to:** Claude (Cowork) / User
> **Priority:** P2 — Completion of Skill Migration

## Context
During the structural consolidation of the `projects` skill, it was discovered that the `references/` subdirectory (which was supposed to contain Task Capture templates) was empty. These files are required for the full execution of the **Task Capture** procedure but currently reside only in the runtime Cowork plugin at `.claude/skills/task-capture/references/`.

## Objective
Restore the following template files to the vault's unified intelligence domain at `intelligence/product/projects/source/`:

- `asana-custom-fields.md`
- `user-story-template.md`
- `task-template.md`
- `bug-template.md`
- `cx-bug-template.md`
- `research-template.md`

## Next Steps
1. **Locate Source**: Extract the content of these files from the active Cowork plugin `.claude/skills/task-capture/references/`.
2. **Deploy to Vault**: Create these files in `intelligence/product/projects/source/`.
3. **Update Index**: Mark "Pending Restoration" as complete in `skills/product/projects/index.md`.
4. **Consistency Check**: Verify that `skills/product/projects/procedure.md` correctly references these new paths.

## Notes
The Cowork plugin version must remain functional for runtime use, but the vault copy is the canonical reference for logic and structure.
