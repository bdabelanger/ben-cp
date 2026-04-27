# Implementation Plan: Add Missing index.md Files - 14 Directories Without Index

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

# Add Missing index.md Files - 14 Directories Without Index

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

## Specific Steps

1. For each directory, create an `index.md` with:
   - A brief description of the directory's purpose (1–2 sentences)
   - A list of the files/subdirectories it contains with short descriptions
   - Standard vault frontmatter if applicable (follow existing index.md patterns in the vault)
2. For `handoffs/` and `handoffs/complete/` — these are managed directories; check if a standard index template exists (e.g. from the handoff skill) and use it
3. For `skills/dream` — index should list all sensor files and `run.py`
4. For `intelligence/governance` — index should reference `policy.md`
5. For the vault root (`.`) — check if this is expected or if the root index is named differently

## Verification Checklist

- [ ] `pulse` sensor `dirs_missing_index` drops to 0 (or near-zero if some dirs are intentionally exempt)
- [ ] Each new `index.md` follows the existing vault index format
- [ ] No existing index files were overwritten
- [ ] Run `generate_report(skill='dream')` to confirm pulse sensor improvement
