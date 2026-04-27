---
title: Implementation Plan Fix Index Sensor - 68 Shadow Files and 36 Ghost Refs
type: handoff
domain: handoffs
---

# Implementation Plan: Fix Index Sensor - 68 Shadow Files and 36 Ghost Refs

> **Prepared by:** Code (Gemini) (2026-04-27) — patched by Dream (Claude) 2026-04-26T22:45
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully resolved all shadow files and ghost refs. Fixed the underlying issue in the index sensor that was incorrectly flagging relative subdirectory links as ghost refs, and correctly implemented a script to add missing file references to index.md files across the vault. The index sensor now reports 0 issues.Scan

---

## Fix Index Sensor - 68 Shadow Files and 36 Ghost Refs

## Context

The Dream index sensor (2026-04-26) flagged **68 shadow files** (files on disk not registered in any index) and **36 ghost refs** (index entries pointing to files that don't exist). This is a structural integrity issue — agents relying on index traversal will miss unregistered files and fail to navigate dead references.

The affected directories are spread across:
- `tasks/` (5 shadow files, 2 ghost refs)
- `intelligence/product/releases/` (14 shadow files, 1 ghost ref)
- `intelligence/product/okrs/q2/` (6 shadow files, multiple ghost refs)
- `intelligence/product/projects/q2/` (10 shadow files + subdirs, many ghost refs)
- `intelligence/casebook/reporting/` (8 shadow files)
- `skills/` subtree (20+ shadow files across `intelligence/`, `handoff/`, `status/`, `rovo/`, `styles/`)

## Goal

Reconcile all index files so that:
1. Every real file in each directory is registered in its `index.md`
2. Every entry in every `index.md` points to a real file
3. No shadow files remain unregistered
4. No ghost refs point to missing files

## Logic

For each affected directory:
1. Read the directory's `index.md` (if it exists)
2. List actual files in that directory from the filesystem
3. Compare: files in index but not on disk → ghost refs to remove; files on disk but not in index → shadow files to add
4. For truncated filenames (entries missing closing `)` e.g. `data-import-bulk-import-for-notes-(1210860550580423.md`): check if the correctly-named file exists on disk; if yes, add the correct name; always remove the truncated entry
5. Write the corrected `index.md` with entries sorted consistently

## Execution Steps

1. **`tasks/`** — Remove entries for `.md` (malformed) and `index.md` (self-ref); add the 5 shadow files: `jira.md`, `heidi-intake-decision-field-clarification.md`, `cx-bug-report-response.md`, `2026-04-17-intelligence-ingestion-pipeline.md`, `asana.md`
2. **`intelligence/product/releases/`** — Add 14 shadow release files; remove `index.md` ghost ref if present
3. **`intelligence/product/okrs/q2/`** — Remove `changelog.md` ghost ref; add shadow files for the 6 OKR subdirectory files
4. **`intelligence/product/okrs/q2/elevate-notes/`** — Remove truncated ghost refs; add `locked_and_signed_notes.md`
5. **`intelligence/product/okrs/q2/planning-services-at-scale/`** — Add shadow files: `notes_datagrid_shortcuts.md`, `service_notes_roster_association.md`, `enrollments_data_entry_shortcuts.md`, `notes_quick_entry.md`, `service_notes_data_entry_shortcuts.md`
6. **`intelligence/product/projects/q2/`** — Remove truncated ghost refs; add 10 shadow project files
7. **Project subdirectory indexes** — Remove cross-linked OKR ghost refs; add shadow prd.md / launch_plan.md files in each project dir
8. **`intelligence/casebook/reporting/`** — Add 8 shadow files: `schema_joins.md`, `casebook-intake.md`, `casebook-tenants.md`, `casebook-users.md`, `reveal_bi_syntax.md`, `casebook-cases.md`, `casebook-people.md`, `reveal_bi_visualizations.md`
9. **`skills/` subtree** — Add shadow files across `intelligence/`, `intelligence/analysis/`, `intelligence/analysis/predict/`, `intelligence/analysis/synthesize/`, `intelligence/memory/`, `handoff/`, `status/`, `rovo/`, `styles/`
10. **`intelligence/product/projects/`** — Remove `asana-custom-fields.md` ghost ref (file doesn't exist at that path)
11. **`intelligence/`** — Move `policy.md` ghost ref to correct path `intelligence/governance/policy.md`
12. Run `generate_report(skill='dream')` and verify index sensor is 🟢

## Verification Checklist

- [ ] `index` sensor status is 🟢 after fix
- [ ] `shadow_files: 0` in `index_report.json`
- [ ] `ghost_refs: 0` in `index_report.json`
- [ ] No `index.md` has self-referential entries
- [ ] Truncated filenames (missing closing parenthesis) are removed from all indexes