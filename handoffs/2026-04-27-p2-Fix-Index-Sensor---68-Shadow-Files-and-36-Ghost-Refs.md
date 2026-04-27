# Implementation Plan: Fix Index Sensor - 68 Shadow Files and 36 Ghost Refs

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

# Fix Index Sensor - 68 Shadow Files and 36 Ghost Refs

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

## Specific Steps

1. **Audit each affected directory's `index.md`** — compare listed entries against actual filesystem contents
2. **Remove ghost refs** — delete index entries for the following known missing files:
   - `tasks/index.md`: remove entries for `.md` (malformed) and `index.md` (self-ref)
   - `intelligence/index.md`: remove `policy.md` entry (file doesn't exist at that path — it's at `intelligence/governance/policy.md`)
   - `intelligence/product/okrs/q2/index.md`: remove `changelog.md` ghost ref
   - `intelligence/product/okrs/q2/elevate-notes/index.md`: remove truncated ghost refs (`data-import-bulk-import-for-notes-(1210860550580423.md`, `notes-global-notes-wlv-(1210368097846960.md`)
   - `intelligence/product/projects/q2/index.md`: remove truncated ghost refs (same malformed filenames)
   - Project subdirectory indexes: remove cross-linked OKR refs that don't exist locally
   - `skills/intelligence/memory/index.md`: remove `status_mapping.md` ghost ref
3. **Register shadow files** — add index entries for all unregistered files in each directory
4. **Run `generate_report(skill='dream')` and confirm index sensor shows 0 shadow files and 0 ghost refs**

## Verification Checklist

- [ ] `index` sensor status is 🟢 after fix
- [ ] `shadow_files: 0` in `index_report.json`
- [ ] `ghost_refs: 0` in `index_report.json`
- [ ] No `index.md` has self-referential entries
- [ ] Truncated filenames (missing closing parenthesis) are removed from all indexes
