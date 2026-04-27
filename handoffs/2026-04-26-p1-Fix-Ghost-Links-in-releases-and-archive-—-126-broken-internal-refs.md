# Implementation Plan: Fix Ghost Links in releases and archive — 126 broken internal refs

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: 🔲 READY — pick up 2026-04-26

---

## Context

The links sensor found 126 ghost links (broken internal references). They cluster into three distinct patterns:

**Pattern 1 — releases/ → flat project files that moved into subdirectories (highest volume)**
Many release files link to flat paths like `../projects/q2/notes-notes-datagrid-(1209963394727039).md` but those files have been reorganized into subdirectories with index files (e.g., `../projects/q2/notes-notes-datagrid/index.md`). Affected releases include: 2026-04-23, 2026-03-17, 2026-05-18, 2026-06-01, 2026-04-27, 2026-05-14, 2026-06-11, 2025-11-06, and more.

Key broken target mapping (flat file → subdirectory index):
- `notes-notes-datagrid-(1209963394727039).md` → `notes-notes-datagrid/index.md`
- `notes-bulk-service-notes-(1211757637943244).md` → `notes-bulk-service-notes/index.md`
- `notes-locked-notes-(1211786365522017).md` → `notes-locked-notes/index.md`
- `notes-bulk-general-notes-(1211838817183809).md` → `notes-bulk-general-notes/index.md`
- `enrollment-dialog-bulk-services-section-(1211631356870657).md` → `enrollment-dialog-bulk-services-section/index.md`
- `services-service-plan-datagrid-with-bulk-actions-(1211631360190563).md` → `services-service-plan-datagrid-with-bulk-actions/index.md`
- `services-wlv-bulk-actions-(1211733450555414).md` → `services-wlv-bulk-actions/index.md`
- `portal-client-dashboard-(1213506659163435).md` → `portal-client-dashboard/index.md`
- `integrations-zapier-improvements-(1213496879668016).md` → `integrations-zapier-improvements/index.md`
- `notes-signing-service-note-locking-(1213685097670626).md` → `notes-signing-service-note-locking/index.md`

**Pattern 2 — archive/daily-report-*.md → stale report paths**
Every archived daily report links to `reports/product-projects.md` and `reports/orchestration-changelog.md` — both ghost paths. These are cosmetically broken legacy files. Leave these alone (low value).

**Pattern 3 — OKR and shareout files → same flat project paths**
Files in `intelligence/product/okrs/q2/` and `intelligence/product/shareout/q2/` have the same flat-path problem as releases/.

**Other notable ghosts:**
- `changelog.md` → `handoffs/2026-04-12-p1-resolve-gemini-root-edit-block.md` (handoff archived or deleted)
- `intelligence/product/index.md` → `reports/latest-platform-status.md` (duplicate occurrence x2, path does not exist)
- `intelligence/product/projects/index.md` → `../../skills/pipelines/asana/schemas/asana-custom-fields.md` (cross-boundary)
- `skills/status/index.md` → `../dod-helper/index.md` and `../weekly-status/index.md` (skill dirs missing or renamed)
- `intelligence/product/shareout/q2/slide-19-reporting-packages-workforce.md` → `reporting-tasks-work-package-(GID_PENDING).md` (placeholder never created)
- `intelligence/product/shareout/q2/slide-34-external-people-in-workflows.md` → `workflows-assign-wf-tasks-to-external-users-(GID_PENDING).md` (same)

## Goal

Reduce ghost link count from 126 to near-zero by updating link paths to match current file structure.

## Execution Steps

1. Audit which flat project files still exist vs. moved into subdirs — run `find intelligence/product/projects/q2 -name "*.md" | sort` to build current map
2. Batch-update `releases/` — replace flat `../projects/q2/<slug>-(GID).md` refs with `../projects/q2/<slug>/index.md` using the mapping above
3. Update OKR index files in `intelligence/product/okrs/q2/` — same flat-to-subdir mapping
4. Update shareout files in `intelligence/product/shareout/q2/` — same pattern
5. Fix `intelligence/product/index.md` — remove or update the duplicate `reports/latest-platform-status.md` links (2 occurrences)
6. Fix `changelog.md` — remove or redirect the ghost handoff link
7. Fix `skills/status/index.md` — verify if `dod-helper/` and `weekly-status/` skill dirs exist; update paths accordingly
8. Leave `archive/daily-report-*.md` — cosmetic broken links, low value to touch archived files
9. Leave GID_PENDING links — flag for Ben to create or remove those project stubs

## Verification

- Re-run `generate_report(skill='dream')` and confirm links sensor improves from red to yellow or green
- Ghost count should drop below 20 after fixing (archive daily reports account for ~30 residual ghosts that we are leaving intentionally)
