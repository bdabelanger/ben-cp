---
title: Implementation Plan Add Missing index.md Files - 14 Directories Without Index
type: handoff
domain: handoffs
---

# Implementation Plan: Add Missing index.md Files - 14 Directories Without Index

> **Prepared by:** Code (Gemini) (2026-04-27) — patched by Dream (Claude) 2026-04-26T22:45
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Add Missing index.md Files - 14 Directories Without Index

## Context

The Dream pulse sensor (2026-04-26) flagged **14 directories** missing an `index.md` file. Index files are required for agent navigation and vault traversal to work correctly.

## Affected Directories

```
. (vault root)
tasks/archived/q2-shareout
intelligence/product/projects/source
intelligence/product/projects/q2/data-import-clearer-ids
intelligence/product/projects/q2/services-multiple-rosters-for-enrollments-and-notes
intelligence/governance
skills/pipelines
skills/pipelines/intelligence/schemas
skills/pipelines/status/scripts
skills/pipelines/asana/schemas
skills/status/schemas
skills/dream
handoffs
handoffs/complete
```

## Goal

Each directory should have an `index.md` that lists its contents and purpose, enabling agents to navigate the vault correctly.

## Logic

For each directory:
1. List all files and immediate subdirectories in it
2. Determine the directory's purpose from its name and contents
3. Write a minimal `index.md` following the pattern used by existing vault index files (title, 1-2 sentence description, file list with short descriptions)
4. Do not overwrite any existing `index.md` — verify absence before writing
5. For system directories (`skills/`, `handoffs/`): check if the relevant skill's SKILL.md or audit.md defines the expected index format and match it

## Execution Steps

1. **`. (vault root)`** — Check if a root index is expected or if the root is intentionally unindexed (may be intentional if the vault uses a different entry point); if expected, create with top-level directory inventory
2. **`handoffs/`** and **`handoffs/complete/`** — Create minimal index listing subdirectory purpose; check handoff SKILL.md at `skills/handoff/SKILL.md` for expected format
3. **`skills/dream/`** — Index should list: `run.py`, all sensor scripts, `SKILL.md` if present
4. **`intelligence/governance/`** — Index should reference `policy.md` and describe governance scope
5. **`intelligence/product/projects/source/`** — List source files; describe as raw upstream project data
6. **`intelligence/product/projects/q2/data-import-clearer-ids/`** and **`services-multiple-rosters-for-enrollments-and-notes/`** — Create project-level index matching other q2 project dirs (check a neighbor like `notes-locked-notes/` for format)
7. **`tasks/archived/q2-shareout/`** — Create minimal archive index
8. **`skills/pipelines/`**, **`skills/pipelines/intelligence/schemas/`**, **`skills/pipelines/status/scripts/`**, **`skills/pipelines/asana/schemas/`**, **`skills/status/schemas/`** — Create index for each listing pipeline scripts and schemas

## Verification Checklist

- [ ] `pulse` sensor `dirs_missing_index` drops to 0 (or near-zero if root is intentionally exempt)
- [ ] Each new `index.md` follows the existing vault index format
- [ ] No existing index files were overwritten
- [ ] Run `generate_report(skill='dream')` to confirm pulse sensor improvement