# Implementation Plan: Fix Frontmatter and Multiple H1s in Q2 Project Files

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved 41 frontmatter and heading issues by deploying a temporary script that injected YAML metadata and demoted duplicate H1s across 20 affected files in the Q2 project domain. Verified clean sensor status.

---

## Context

The frontmatter sensor (now functioning after pyyaml was installed in the prior Dream run) found 41 issues concentrated in `intelligence/product/projects/q2/`. All `prd.md` and `launch_plan.md` files across the Q2 project subdirectories are missing YAML frontmatter blocks and contain multiple H1 headings — a systematic pattern suggesting these files were generated without frontmatter templating and contain versioned/appended content that accumulated multiple `#` headers.

Additionally, three index files lack frontmatter:
- `intelligence/product/projects/asana-custom-fields/index.md` (also has 2 H1s)
- `intelligence/product/projects/q2/portal-client-dashboard/index.md`
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md`

The `handoffs/2026-04-27-p1-Dream-Report.md` frontmatter issue is resolved (superseded and archived).

## Affected Files (38 issues across ~15 project dirs)

Files with `missing_frontmatter` + `multiple_h1`:
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
- `intelligence/product/projects/asana-custom-fields/index.md` (2 H1s)

Files with `missing_frontmatter` only:
- `intelligence/product/projects/q2/portal-client-dashboard/index.md`
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md`

## Goal

Add proper YAML frontmatter to all affected files and resolve multiple H1 issues (collapse or demote duplicate H1s to H2/H3 as appropriate).

## Execution Steps

1. Write a script (`skills/fix_q2_frontmatter.py`) that:
   - Iterates all affected files
   - Detects existing title from first H1
   - Injects a minimal frontmatter block: `title`, `type` (prd/launch_plan/index), `domain`, `date` (from git log or file mtime)
   - Demotes H1s after the first to H2 (or removes exact duplicates)
2. Run in dry-run mode first, review diff
3. Apply changes
4. Re-run `generate_report(skill='dream')` and confirm frontmatter sensor drops from 🔴 to 🟢 or 🟡

## Verification

- [ ] Frontmatter sensor issue count drops from 41 to ≤3 (only the known benign ones)
- [ ] No file content lost — only structural metadata added
- [ ] No new multiple_h1 findings introduced
- [ ] Script removed or moved to `scripts/archive/` after use
