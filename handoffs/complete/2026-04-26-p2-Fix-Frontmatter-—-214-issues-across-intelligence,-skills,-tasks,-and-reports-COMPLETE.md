---
title: 'Implementation Plan: Fix Frontmatter — 214 issues across intelligence, skills,
  tasks, and reports'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Fix Frontmatter — 214 issues across intelligence, skills, tasks, and reports

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully resolved 197/214 frontmatter issues. Refined the 'dream' sensor to recognize HTML headers and skip noisy directories (reports, handoffs). Batch-applied standardized metadata to agents, releases, OKRs, and project files. Residual issues are limited to multiple H1s in machine-exported PRDs.

---

## Context

The frontmatter sensor found 214 issues across 167 files. The issues fall into clear buckets by file type — most are systemic missing-frontmatter patterns across file classes that never had frontmatter added, not individual one-off errors.

**Issue Buckets by file class:**

**A. intelligence/product/releases/ — ~45 files, all missing_frontmatter**
Every release file (e.g., `2026-04-23-release.md`, `2025-11-06-release.md`) lacks frontmatter entirely. These should get minimal frontmatter: `type: release`, `date`, `status: published`.

**B. intelligence/product/shareout/q2/ — ~12 files, missing_frontmatter + multiple_h1**
All Q2 shareout slide files have no frontmatter and have 2x H1 headers (likely a title duplication issue in how they were created). Should get frontmatter added and second H1 demoted to H2.

**C. intelligence/product/okrs/q2/ — ~6 files, missing_frontmatter**
OKR sub-files (`notes_quick_entry.md`, `enrollments_data_entry_shortcuts.md`, etc.) lack frontmatter. Add `type: okr-research`, `status`, `date`.

**D. intelligence/product/projects/q2/ — ~15 files, mix of missing_frontmatter, multiple_h1, long_file_no_h2**
Project flat files and prd.md/launch_plan.md files lack frontmatter. The `long_file_no_h2` issues are on PRD and launch plan files — long documents with no section headers, which is likely intentional for these document types. Consider whether to add H2 sections or suppress the check for `prd.md`/`launch_plan.md` files.

**E. skills/ — ~25 files, mostly missing_frontmatter**
SKILL.md files, audit.md, report.md, etc. throughout the skills tree. Skills probably don't need the same frontmatter schema as intelligence records. Evaluate whether to apply a lighter schema or exclude skills from the frontmatter sensor.

**F. tasks/ — 5 files, missing_frontmatter**
Task files in `tasks/` directory lack frontmatter. These may not need standard intelligence frontmatter — confirm expected schema for task files.

**G. agents/ — 3 files (cowork.md, code.md, local.md), missing_frontmatter**
Agent files lack frontmatter. Add minimal `type: agent`, `role` metadata.

**H. reports/ — all report and archive files, missing_frontmatter**
Generated report files have no frontmatter. These are machine-generated; consider excluding from sensor scope or adding a generator-side template.

**I. intelligence/casebook/reporting/ — 7 files, missing_keys**
These files have frontmatter but are missing: `Date`, `Owner`, `Priority`, `Status`. Add the missing keys.

**Specific structural issues:**
- `tasks/2026-04-17-intelligence-ingestion-pipeline.md` — multiple_h1 (count: 2), fix by demoting second H1
- `intelligence/product/projects/asana_field_definitions.md` — multiple_h1, fix by demoting second H1
- `skills/rovo/SKILL.md` — no_h1, add a title header
- Several casebook/reporting files have multiple_h1

## Goal

Systematically add or fix frontmatter across all affected file classes, and make a decision on sensor scope (should skills, reports, and tasks be excluded or use a lighter schema?).

## Execution Steps

1. Decide sensor scope: should `skills/`, `reports/`, and `tasks/` directories be excluded from the frontmatter check or given different required fields? Note this in a sensor config comment if there is one.
2. Fix agents/ — add `type: agent` frontmatter to cowork.md, code.md, local.md
3. Fix casebook/reporting/ — add missing keys (Date, Owner, Priority, Status) to the 7 files that have partial frontmatter
4. Fix intelligence/product/releases/ — batch-add minimal frontmatter to all release files using date from filename
5. Fix multiple_h1 issues — demote second H1 to H2 in: asana_field_definitions.md, notes-signing-service-note-locking.md, notes-global-notes-wlv.md, data-import-bulk-import-for-notes.md, and all shareout/q2/ slide files
6. Fix `skills/rovo/SKILL.md` — add H1 title
7. Fix casebook/reporting multiple_h1 files (casebook-tenants.md, casebook-cases.md)
8. Add frontmatter to OKR sub-files and shareout files
9. Evaluate long_file_no_h2 on prd.md and launch_plan.md — these may be intentional; consider a sensor exclusion for known document types

## Verification

- Re-run `generate_report(skill='dream')` and confirm frontmatter sensor improves from red to yellow or green
- Issue count should drop from 214 to under 30 after structural fixes
