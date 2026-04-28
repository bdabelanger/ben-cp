---
title: 'Implementation Plan: Fix Frontmatter - Multiple H1 Headers in Q2 PRDs and
  Launch Plans'
type: handoff
domain: handoffs
---


# Implementation Plan: Fix Frontmatter - Multiple H1 Headers in Q2 PRDs and Launch Plans

> **Prepared by:** Code (Gemini) (2026-04-27) — patched by Dream (Claude) 2026-04-26T22:45
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully resolved all 'multiple_h1' violations by demoting redundant section headers to H2. This work was consolidated into the P1 frontmatter normalization session.Scan

---

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

## Logic

The fix is purely mechanical:
1. Each file should have exactly **one H1 header** (the document title). All subsequent section headers should use H2 (`##`) or lower.
2. Find the first `# ` (H1) line — this is the document title, leave it alone.
3. For every subsequent line starting with `# ` (a bare H1, not `##` or deeper), replace the leading `#` with `##`.
4. Ensure H1 lines inside fenced code blocks (` ``` `) are NOT demoted.

## Execution Steps

1. [ ] For each of the 17 files listed above, open the file and apply the H1 demotion logic.
2. [ ] Process files in the order listed — no dependency between them.
3. [ ] After all 17 are done, run `generate_report(skill='dream')`.
4. [ ] Confirm `frontmatter_report.json` shows `issues_found: 0`.
5. [ ] If any file still shows `multiple_h1`, re-read that specific file and check for edge cases.

## Verification Checklist

- [ ] `frontmatter` sensor status is 🟢 after fix.
- [ ] `issues_found: 0` in `frontmatter_report.json`.
- [ ] Each affected file has exactly 1 H1 header.
- [ ] No content other than header levels was modified.
