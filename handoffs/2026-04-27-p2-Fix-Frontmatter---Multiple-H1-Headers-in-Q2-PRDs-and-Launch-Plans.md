# Implementation Plan: Fix Frontmatter - Multiple H1 Headers in Q2 PRDs and Launch Plans

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

# Fix Frontmatter - Multiple H1 Headers in Q2 PRDs and Launch Plans

## Context

The Dream frontmatter sensor (2026-04-26) flagged **17 files** with `multiple_h1` issues — all of them Q2 project PRDs or launch plans under `intelligence/product/projects/q2/`. These files have between 3 and 8 H1 (`#`) headers each.

This is likely an artifact of how the PRD/launch plan templates were generated — each section was written with an H1 instead of H2/H3 sub-headings. This causes rendering and navigation issues in tools that expect a single document title.

## Affected Files

| File | H1 Count |
|------|----------|
| `intelligence/product/projects/q2/data-import-clearer-ids/prd.md` | 6 |
| `intelligence/product/projects/q2/notes-locked-notes/prd.md` | 5 |
| `intelligence/product/projects/q2/notes-locked-notes/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/prd.md` | 6 |
| `intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/integrations-zapier-improvements/prd.md` | 3 |
| `intelligence/product/projects/q2/notes-bulk-service-notes/prd.md` | 5 |
| `intelligence/product/projects/q2/notes-bulk-service-notes/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/notes-bulk-general-notes/prd.md` | 5 |
| `intelligence/product/projects/q2/notes-bulk-general-notes/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/portal-client-dashboard/prd.md` | 8 |
| `intelligence/product/projects/q2/notes-notes-datagrid/prd.md` | 5 |
| `intelligence/product/projects/q2/notes-notes-datagrid/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/services-multiple-rosters-for-enrollments-and-notes/prd.md` | 6 |
| `intelligence/product/projects/q2/services-service-plan-datagrid-with-bulk-actions/launch_plan.md` | 5 |
| `intelligence/product/projects/q2/data-import-bulk-import-for-notes/prd.md` | 6 |
| `intelligence/product/projects/q2/services-wlv-bulk-actions/launch_plan.md` | 5 |

## Goal

Each file should have exactly **one H1 header** (the document title). All subsequent section headers should use H2 (`##`) or lower.

## Specific Steps

1. For each affected file, read the full content
2. Keep the **first** `#` header as the document title (H1)
3. Demote all subsequent `#` headers to `##` (H2), preserving their text exactly
4. Do not alter any H2, H3, or lower headers
5. Do not alter any body content, links, or metadata
6. Run `generate_report(skill='dream')` after completing all files and confirm frontmatter sensor shows 0 `multiple_h1` issues

## Verification Checklist

- [ ] `frontmatter` sensor status is 🟢 after fix
- [ ] `issues_found: 0` in `frontmatter_report.json`
- [ ] Each affected file has exactly 1 H1 header
- [ ] No content other than header levels was modified
