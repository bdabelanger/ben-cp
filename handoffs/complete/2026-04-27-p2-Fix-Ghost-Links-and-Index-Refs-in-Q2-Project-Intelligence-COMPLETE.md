# Implementation Plan: Fix Ghost Links and Index Refs in Q2 Project Intelligence

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved 13 actionable ghost links and 6 index ghost refs by updating project indices, release notes, and shareout slides with correct subdirectory paths and relative OKR links. Verified clean dream run.

---

## Context

The links sensor found 15 ghost links; the index sensor found 6 ghost refs. The majority share a single root cause: files in `intelligence/product/projects/q2/` were reorganized from flat `.md` files into subdirectories, but references in several files were never updated to point at the new paths.

Three project entries are affected:
- `data-import-bulk-import-for-notes-(1210860550580423)` → now at `data-import-bulk-import-for-notes/`
- `integrations-zapier-improvements-(1213496879668016)` → now at `integrations-zapier-improvements/`
- `notes-signing-service-note-locking-(1213685097670626)` → now at `notes-signing-service-note-locking/`

Additionally, three project `index.md` files link to OKR files that don't exist:
- `intelligence/product/projects/q2/integrations-zapier-improvements/index.md` → `../../okrs/q2/reduce-admin-burden/index.md`
- `intelligence/product/projects/q2/notes-signing-service-note-locking/index.md` → `../../okrs/q2/elevate-notes/locked_and_signed_notes.md`
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md` → `../../okrs/q2/elevate-notes/index.md`

Two ghost links in `reports/dream/report.md` are report-generation artifacts — not actionable.

## Goal

Resolve all 13 actionable ghost links and 6 index ghost refs so both sensors return clean.

## Execution Steps

1. **Update `intelligence/product/projects/q2/index.md`** — replace all 6 flat/relative refs to the three project files with correct subdirectory paths:
   - `./data-import-bulk-import-for-notes-(1210860550580423).md` → `./data-import-bulk-import-for-notes/index.md`
   - `./integrations-zapier-improvements-(1213496879668016).md` → `./integrations-zapier-improvements/index.md`
   - `./notes-signing-service-note-locking-(1213685097670626).md` → `./notes-signing-service-note-locking/index.md`
   - Remove bare (no `./` prefix) duplicates if present

2. **Update release files** — fix `../projects/q2/data-import-bulk-import-for-notes-(1210860550580423).md` in:
   - `intelligence/product/releases/2026-07-13-release.md`
   - `intelligence/product/releases/2026-07-09-release.md`
   - `intelligence/product/releases/7-9-2026-release.md`
   → new path: `../projects/q2/data-import-bulk-import-for-notes/index.md`

3. **Update shareout file** — fix link in `intelligence/product/shareout/q2/slide-26-bulk-import-notes.md`:
   → `../../projects/q2/data-import-bulk-import-for-notes/index.md`

4. **Resolve OKR links** — for the three project index files linking to missing OKR paths, either:
   - Create stub OKR files at the expected paths if the OKR structure exists but files are missing, OR
   - Remove/comment the broken OKR links if Q2 OKRs are not tracked in the repo

5. **Re-run dream sensors** after fixes and confirm links + index sensors return clean.

## Verification

- `generate_report(skill='dream')` → links sensor: 0 ghost links (excluding report artifacts) · index sensor: 0 ghost refs
- All source files updated, no regressions in other sensors
