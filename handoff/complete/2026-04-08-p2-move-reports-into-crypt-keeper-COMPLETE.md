# Claude Code Implementation Plan: Move reports/ into skills/crypt-keeper/

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P2 — structural consolidation, Crypt-Keeper owns its reports
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-09**

`skills/crypt-keeper/reports/` and its `archive/` subdirectory were already created in a prior session. The root `reports/` directory was removed via `git rm -r`. `skills/crypt-keeper/procedure.md` updated: output path changed to `skills/crypt-keeper/reports/`, Pre-Flight updated with archive step. `AGENTS.md` vault tree updated: root `reports/` removed, `crypt-keeper/` section expanded with SKILL.md, changelog.md, and `reports/` (with `archive/`). File Placement table updated. `crypt-keeper/index.md` reports/ entry and stale reference updated (done as part of handoff 1). `SKILL.md` was already correct — no change needed.

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

Reports are currently written to `reports/` at vault root. Since Crypt-Keeper
is the only thing that produces reports, they belong inside
`skills/crypt-keeper/reports/` alongside the procedure and templates that
generate them. An `archive/` subdirectory will hold all runs except the most
recent, keeping the reports root clean.

---

## Execution Order

1. **Task 1** — Create new directory structure
2. **Task 2** — Move existing report and .gitkeep
3. **Task 3** — Remove old root `reports/` directory
4. **Task 4** — Update `skills/crypt-keeper/SKILL.md` output path
5. **Task 5** — Update `skills/crypt-keeper/procedure.md` output path
6. **Task 6** — Update `skills/crypt-keeper/report-template.md` output path reference
7. **Task 7** — Update `AGENTS.md` vault structure tree
8. **Task 8** — Update `skills/crypt-keeper/index.md`
9. **Task 9** — Final audit and completion report

---

## Task 1: Create New Directory Structure

```
git mkdir skills/crypt-keeper/reports/
git mkdir skills/crypt-keeper/reports/archive/
```

Or use `create_directory` for each:
- `skills/crypt-keeper/reports/`
- `skills/crypt-keeper/reports/archive/`

---

## Task 2: Move Existing Files

```
git mv reports/cleanup-report-2026-04-08.md skills/crypt-keeper/reports/archive/cleanup-report-2026-04-08.md
git mv reports/.gitkeep skills/crypt-keeper/reports/.gitkeep
```

The existing report goes straight to `archive/` since it is no longer the
active run — it's historical. Future runs write to `skills/crypt-keeper/reports/`
and Crypt-Keeper moves the previous report to `archive/` at the start of each run.

---

## Task 3: Remove Root reports/ Directory

After confirming all files moved:
```
git rm -r reports/
```

---

## Task 4: Update SKILL.md Output Path

**Read first:** `skills/crypt-keeper/SKILL.md`

In the **Report Output** section, replace:
```
`/Users/benbelanger/GitHub/ben-cp/reports/cleanup-report-[YYYY-MM-DD].md`
```
With:
```
`/Users/benbelanger/GitHub/ben-cp/skills/crypt-keeper/reports/cleanup-report-[YYYY-MM-DD].md`
```

Also add an **Archiving** step at the end of the Report Output section:

```markdown
## Archiving

At the start of each run, before writing a new report:
1. Check if a previous `cleanup-report-*.md` exists in `skills/crypt-keeper/reports/`
2. If yes, move it to `skills/crypt-keeper/reports/archive/` using `git mv`
3. Then write the new report to `skills/crypt-keeper/reports/`

This keeps `reports/` showing only the current run, with full history in `archive/`.
```

---

## Task 5: Update procedure.md Output Path

**Read first:** `skills/crypt-keeper/procedure.md`

Replace all occurrences of:
```
/Users/benbelanger/GitHub/ben-cp/reports/
```
With:
```
/Users/benbelanger/GitHub/ben-cp/skills/crypt-keeper/reports/
```

---

## Task 6: Update report-template.md

**Read first:** `skills/crypt-keeper/report-template.md`

If it contains any path reference to `reports/`, update to
`skills/crypt-keeper/reports/`.

---

## Task 7: Update AGENTS.md Vault Structure Tree

**Read first:** `AGENTS.md`

Remove the `reports/` entry from the root level of the vault tree. Add
`reports/` under `skills/crypt-keeper/` instead:

```
skills/crypt-keeper/
    ├── SKILL.md
    ├── index.md
    ├── procedure.md
    ├── report-template.md
    ├── changelog.md
    └── reports/
        ├── cleanup-report-YYYY-MM-DD.md
        └── archive/
```

Also update the File Placement table — replace:
```
| Cleanup reports | `reports/cleanup-report-[YYYY-MM-DD].md` |
```
With:
```
| Cleanup reports | `skills/crypt-keeper/reports/cleanup-report-[YYYY-MM-DD].md` |
```

---

## Task 8: Update skills/crypt-keeper/index.md

**Read first:** `skills/crypt-keeper/index.md`

Add a `reports/` entry to the contents table:

```
| `reports/` | Generated cleanup reports — current run + archive/ |
```

---

## Task 9: Final Audit and Completion Report

1. `list_directory` on `skills/crypt-keeper/reports/` — confirm `.gitkeep` present
2. `list_directory` on `skills/crypt-keeper/reports/archive/` — confirm 2026-04-08 report present
3. Confirm `reports/` no longer exists at vault root
4. Read `SKILL.md` — confirm output path and Archiving section updated
5. Read `procedure.md` — confirm path updated
6. Read `AGENTS.md` — confirm vault tree and file placement table updated
7. Write changelog entry using `write_changelog_entry`

```
## Completion Report

**Directories created:**
- skills/crypt-keeper/reports/
- skills/crypt-keeper/reports/archive/

**Files moved (git mv):**
- reports/cleanup-report-2026-04-08.md → skills/crypt-keeper/reports/archive/
- reports/.gitkeep → skills/crypt-keeper/reports/

**Directories removed:**
- reports/ (vault root)

**Files modified:**
- skills/crypt-keeper/SKILL.md — output path + Archiving section
- skills/crypt-keeper/procedure.md — output path
- skills/crypt-keeper/report-template.md — path reference if present
- AGENTS.md — vault tree + file placement table
- skills/crypt-keeper/index.md — added reports/ entry

**Flags for Ben:** [anything unexpected]
```

---

## Notes for This Agent

- Use `git mv` for all moves — preserves history on the report file
- The 2026-04-08 report goes to `archive/` immediately — it is historical
- Do not modify the content of any report files — move only
- Follow all Read → Write rules from `AGENTS.md`
