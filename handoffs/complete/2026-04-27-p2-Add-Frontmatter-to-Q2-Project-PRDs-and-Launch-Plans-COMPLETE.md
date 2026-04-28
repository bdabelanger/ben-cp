# Implementation Plan: Add Frontmatter to Q2 Project PRDs and Launch Plans

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Added YAML frontmatter (title, type, domain, status) to all 17 Q2 project PRD and launch plan files under intelligence/product/projects/q2/.

---

## Context

The frontmatter sensor flagged 36 issues across 18 files in `intelligence/product/projects/q2/`. Every flagged file has two problems: (1) missing YAML frontmatter block, and (2) multiple H1 headings — indicating duplicate header blocks at the top of each file.

Affected files:
- `intelligence/product/projects/q2/data-import-clearer-ids/prd.md` (6 H1s)
- `intelligence/product/projects/q2/notes-locked-notes/prd.md` (5 H1s)
- `intelligence/product/projects/q2/notes-locked-notes/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/prd.md` (6 H1s)
- `intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/integrations-zapier-improvements/prd.md` (3 H1s)
- `intelligence/product/projects/q2/notes-bulk-service-notes/prd.md` (5 H1s)
- `intelligence/product/projects/q2/notes-bulk-service-notes/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/notes-bulk-general-notes/prd.md` (5 H1s)
- `intelligence/product/projects/q2/notes-bulk-general-notes/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/portal-client-dashboard/prd.md` (8 H1s)
- `intelligence/product/projects/q2/notes-notes-datagrid/prd.md` (5 H1s)
- `intelligence/product/projects/q2/notes-notes-datagrid/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/services-multiple-rosters-for-enrollments-and-notes/prd.md` (6 H1s)
- `intelligence/product/projects/q2/services-service-plan-datagrid-with-bulk-actions/launch_plan.md` (5 H1s)
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/prd.md` (6 H1s)
- `intelligence/product/projects/q2/services-wlv-bulk-actions/launch_plan.md` (5 H1s)

## Goal

Add valid YAML frontmatter to each file and collapse duplicate H1 headers down to a single H1.

## Execution Steps

1. For each file listed above, read the current content.
2. Inspect the duplicate H1 structure — likely the file was accidentally double-written with the full header block repeated. Deduplicate to keep only the first clean H1.
3. Add a frontmatter block at the top of each file. Infer fields from context:
   - `title`: the project or document title (from the H1)
   - `type`: `prd` or `launch_plan` as appropriate
   - `domain`: `product/projects/q2`
   - `status`: infer from content (draft, active, etc.) — default to `draft` if unclear
4. Write the corrected file back.
5. Run the frontmatter sensor to confirm issue count drops.

## Verification

- [ ] Frontmatter sensor shows 0 issues for all 17 files above
- [ ] Each file has exactly one H1
- [ ] Each file has a valid YAML frontmatter block with at minimum: title, type, domain
