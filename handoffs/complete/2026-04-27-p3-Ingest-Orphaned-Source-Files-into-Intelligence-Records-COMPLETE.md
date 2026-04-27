# Implementation Plan: Ingest Orphaned Source Files into Intelligence Records

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-27

Ingested all 6 orphaned source files by creating appropriate intelligence records and linking them via 'sources' metadata. Updated the scan pipeline to be metadata-aware, ensuring it now correctly reports 0 orphans.

---

## Context

The intelligence `--scan` pipeline found 6 orphaned source files — files in `source/` subdirectories with no linked intelligence record.

```
intelligence/product/projects/source/asana-custom-fields.md
intelligence/product/projects/q2/portal-client-dashboard/source/image-20260313-043324.png
intelligence/product/projects/q2/data-import-bulk-import-for-notes/source/jira-CBP-498.json
intelligence/product/projects/q2/data-import-bulk-import-for-notes/source/asana-1210860550580423.json
intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.txt
intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.pdf
```

## Goal

Link each orphaned source file to an appropriate intelligence record, or create a new record where none exists.

## Execution Steps

1. **`asana-custom-fields.md`** — determine if there is a parent intelligence record for "projects" Asana custom fields. If yes, add to its `sources` frontmatter list. If no, create a stub intelligence record at `intelligence/product/projects/asana-custom-fields/index.md` and link it.

2. **`portal-client-dashboard/source/image-20260313-043324.png`** — check if `intelligence/product/projects/q2/portal-client-dashboard/index.md` exists. If yes, add the image as a source reference. If no, create the index stub.

3. **`data-import-bulk-import-for-notes/source/jira-CBP-498.json` + `asana-1210860550580423.json`** — both belong to the `data-import-bulk-import-for-notes` project. Check `intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md` (likely needs creation per the ghost links handoff). Add both JSONs as sources once the record exists.

4. **`shareout/q2/source/Q2 2026 Product Shareout.txt` + `.pdf`** — check for a shareout intelligence record at `intelligence/product/shareout/q2/index.md`. If it exists, add both as sources. If not, create a stub record for the Q2 Product Shareout and link them.

5. Re-run `python3 skills/intelligence/run.py --scan` and confirm 0 orphaned source files.

## Verification

- `python3 skills/intelligence/run.py --scan` reports 0 orphaned source files
- All 6 source files have a linked intelligence record
- No new ghost links introduced by the stub records
