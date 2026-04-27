---
title: 'Implementation Plan: Fix Ghost Links in intelligence-product - OKR and Release
  Cross-References'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Fix Ghost Links in intelligence-product - OKR and Release Cross-References

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved ~39 ghost links in intelligence/product/ by correcting relative paths and stripping stale references. verified via dream report.

---

## Fix Ghost Links in intelligence/product/ - OKR and Release Cross-References

## Context

The links sensor found 79 ghost links vault-wide. Approximately 39 originate in `intelligence/product/` across four clusters:

**Cluster 1: OKR files linking to missing projects/q2/ subdirectories (~20 links)**
Files in `intelligence/product/okrs/q2/planning-services-at-scale/`, `okrs/q2/elevate-notes/`, and `okrs/q2/reduce-admin-burden/` link to `../../projects/q2/` paths that don't exist, e.g.:
- `../../projects/q2/notes-notes-datagrid/index.md`
- `../../projects/q2/notes-global-notes-wlv-(1210368097846960).md`
- `../../projects/q2/notes-bulk-service-notes/index.md`
- `../../projects/q2/enrollment-dialog-bulk-services-section/index.md`
- `../../projects/q2/services-wlv-bulk-actions/index.md`
- `../../projects/q2/services-service-plan-datagrid-with-bulk-actions/index.md`
- `../../projects/q2/notes-locked-notes/index.md`
- `../../projects/q2/notes-signing-service-note-locking/index.md`
- `../../projects/q2/integrations-zapier-improvements/index.md`
- `../../projects/q2/portal-client-dashboard/index.md`
- `../../projects/q2/data-import-bulk-import-for-notes-(1210860550580423).md`

**Cluster 2: Release files linking to archived project files (~4 links)**
Files in `intelligence/product/releases/` link to `../projects/archive/2025/q3/` and `../projects/backlog/` paths that no longer exist:
- `2025-10-09-release.md` → `../projects/archive/2025/q3/notes-navigate-to-note-from-case-history-(1209963394727206).md`
- `2025-03-27-release.md` → `../projects/archive/2025/q1/intake-transfer-more-data-with-create-case-(1209067717586477).md`
- `2026-03-17-release.md` → `../projects/backlog/text-messaging-phone-number-selectiononboarding-(1210615331914089).md`
- `2025-11-06-release.md` → `../projects/archive/2025/q3/funding-budgets-for-allowable-services-(1210452458408257).md`

**Cluster 3: Shareout slides with GID_PENDING links (~2 links)**
- `shareout/q2/slide-19-reporting-packages-workforce.md` → `../../projects/q2/reporting-tasks-work-package-(GID_PENDING).md`
- `shareout/q2/slide-34-external-people-in-workflows.md` → `../../projects/q2/workflows-assign-wf-tasks-to-external-users-(GID_PENDING).md`

**Cluster 4: projects index linking to missing skills path (~1 link)**
- `intelligence/product/projects/index.md` → `../../skills/pipelines/asana/schemas/asana-custom-fields.md`

## Goal

Resolve all ghost links in `intelligence/product/` so the links sensor shows 0 broken references from this subtree.

## Execution Steps

1. **Cluster 1 (OKR → projects/q2/)**: Check whether target project directories exist under `intelligence/product/projects/` (they may have been renamed or moved). If found, update paths. If genuinely absent, either create stub `index.md` files or strip the hyperlink and leave the project name as plain text.

2. **Cluster 2 (releases → archive)**: Check if referenced archive files exist anywhere under `intelligence/product/projects/archive/`. If moved, update paths. If gone, strip the hyperlink and leave the project name as plain text (historical notes are fine without live links).

3. **Cluster 3 (GID_PENDING)**: Either create stub project files at expected paths, or update the shareout slides to reference the projects as plain text until GIDs are assigned.

4. **Cluster 4 (skills path)**: Verify if `skills/pipelines/asana/schemas/asana-custom-fields.md` exists. Correct the path if wrong; remove the link if the file doesn't exist.

5. Re-run `generate_report(skill='dream')` and confirm the links sensor ghost count drops by ~39.

## Verification Checklist

- [ ] `get_report('dream/links.json')` shows 0 ghost links sourced from `intelligence/product/` files
- [ ] No broken links remain in `okrs/q2/` files
- [ ] No broken links remain in `releases/` files
- [ ] No broken links remain in `shareout/q2/` files
- [ ] OKR index files still accurately reflect linked projects
