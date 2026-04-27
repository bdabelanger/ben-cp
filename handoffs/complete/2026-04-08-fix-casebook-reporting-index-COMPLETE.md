---
title: Claude Code Implementation Plan Fix casebookreportingindex.md
type: handoff
domain: handoffs/complete
---

# Claude Code Implementation Plan: Fix casebook/reporting/index.md

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Source:** Vault Auditor report `reports/knowledge-report-2026-04-08.md` flag 1.4
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **v1.0**
> **STATUS**: ✅ COMPLETE

`skills/casebook/reporting/schema_joins.md` created with the existing index.md content, paths fixed from `casebook-reporting/` to `casebook/reporting/`, and "File Management Best Practice" section removed. `index.md` replaced with a proper directory TOC listing all 9 files including the new `schema_joins.md` and existing `changelog.md`.

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

`skills/casebook/reporting/index.md` is currently a "Schema Relationships & Data
Joins" reference document — not a directory index. This means 8 files in the
directory are invisible to any agent that relies on the index for navigation.

The schema joins content is valuable and should be preserved as its own file
(`schema_joins.md`). The index.md needs to become a proper TOC.

Also: the existing index.md contains broken path references pointing to the old
`casebook-reporting/` location (pre-consolidation). These need to be fixed in
the new `schema_joins.md`.

---

## Execution Order

1. **Task 1** — Read current index.md and all files in the directory
2. **Task 2** — Create `schema_joins.md` with the existing index.md content (fixed paths)
3. **Task 3** — Rewrite `index.md` as a proper directory TOC
4. **Task 4** — Final audit and completion report

---

## Task 1: Audit the Directory

Read and list:
1. `list_directory` on `skills/casebook/reporting/` — note all files
2. `read_text_file` on `skills/casebook/reporting/index.md` — note current content

---

## Task 2: Create schema_joins.md

**Check first:** confirm `skills/casebook/reporting/schema_joins.md` does not exist.

Create `skills/casebook/reporting/schema_joins.md` with the content currently
in `index.md`, but fix the broken path references:

Replace:
```
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook-reporting/reveal_bi_syntax.md
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook-reporting/reveal_bi_visualizations.md
```
With:
```
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook/reporting/reveal_bi_syntax.md
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook/reporting/reveal_bi_visualizations.md
```

Also remove the "File Management Best Practice" section at the bottom — that
belongs in AGENTS.md, not a reference doc.

---

## Task 3: Rewrite index.md as Directory TOC

**Read first:** current `skills/casebook/reporting/index.md`

Replace entire contents with:

```markdown
# Skill: Casebook Reporting

> Reveal BI reference docs and Casebook entity schemas.
> Last updated: [YYYY-MM-DD]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `schema_joins.md` | Core join map and BI modeling strategy |
| `reveal_bi_syntax.md` | Query syntax reference for Reveal BI |
| `reveal_bi_visualizations.md` | Visualization and output formatting |
| `casebook-cases.md` | Case entity schema and key fields |
| `casebook-intake.md` | Intake entity schema |
| `casebook-people.md` | Person entity schema |
| `casebook-tenants.md` | Tenant entity schema — use for tenant segmentation |
| `casebook-users.md` | User entity schema — use for user-level metrics |
| `changelog.md` | Detail log for this subdirectory |
```

Use `edit_file` — do not `write_file` on the existing index.md.

---

## Task 4: Final Audit and Completion Report

1. Read `skills/casebook/reporting/index.md` — confirm it is now a TOC
2. Read `skills/casebook/reporting/schema_joins.md` — confirm content present and paths fixed
3. Write changelog entry using `write_changelog_entry`

```
## Completion Report

**Files created:**
- skills/casebook/reporting/schema_joins.md — schema joins reference doc (moved from index.md)

**Files modified:**
- skills/casebook/reporting/index.md — replaced with proper directory TOC

**Flags for Ben:** [anything unexpected]
```
