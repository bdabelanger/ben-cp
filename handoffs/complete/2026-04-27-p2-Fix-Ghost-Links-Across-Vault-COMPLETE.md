# Implementation Plan: Fix Ghost Links Across Vault

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully resolved all 10 ghost links flagged in the vault. Most were stale relative paths or drag-and-drop absolute path artifacts. Verified with a fresh dream cycle showing 0 ghost links across 210 scanned files.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/Scan

---

## Context

The `links` sensor in the 2026-04-27 Dream cycle found 10 ghost links across the vault — broken internal references in markdown files. These range from truncated absolute paths (likely Markdown editor artifacts) to missing target files and stale relative paths.

## Goal

Resolve all 10 ghost links. For each, either fix the path to point to the correct existing file, or remove/replace the link with plain text if the target no longer exists.

## Ghost Links to Fix

| Source File | Broken Link | Notes |
|---|---|---|
| `intelligence/product/projects/index.md` | `../../../skills/pipelines/asana/schemas/asana-custom-fields.md` | Target doesn't exist — `skills/pipelines/` is not a valid path. Check if file moved or remove the reference. |
| `intelligence/governance/policy.md` | `source/Q2 2026 Product Shareout.pdf` | Check if file exists at `intelligence/governance/source/`. If not, remove the link. |
| `intelligence/casebook/reporting/schema_joins.md` | `/Users/benbelanger/My` (×2) | Truncated absolute path — likely a dragged file that got cut off. Remove both occurrences or find the intended target. |
| `skills/index.md` | `intelligence/index.md` | `skills/intelligence/` directory exists but `skills/intelligence/index.md` does not. Create a stub index or fix the link to an existing file. |
| `skills/index.md` | `utilities/index.md` | `skills/utilities/` does not exist. Remove or update the reference. |
| `skills/status/scripts/index.md` | `07_build_report.py` | Check if this script exists in `skills/status/scripts/`. If not, remove the link. |
| `skills/styles/report.md` | `file:///Users/benbelanger/My` | Truncated local file:// URI — drag-and-drop artifact. Remove entirely. |
| `reports/status/data/raw/index.md` | `asana.json` | Check if `asana.json` exists in `reports/status/data/raw/`. If not, remove the link or update to correct filename. |
| `reports/status/data/raw/index.md` | `asana_all_projects.json` | Same as above — check and fix or remove. |

## Execution Steps

1. For each row, read the source file first before editing.
2. Determine if the target exists at any corrected path. Use `list_intelligence` or filesystem tools to verify.
3. Fix or remove the link.
4. After all fixes, note which links were repaired vs. removed in a brief comment.

## Verification

- Re-run `generate_report(skill='dream')` after fixes.
- Confirm `links` sensor drops from 10 ghost links to 0 (or near 0 if any are ambiguous).
