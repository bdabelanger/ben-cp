# Implementation Plan: Fix Bad Asana Dates & Null Fields

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Scanned all 22 Q2 intelligence files for null/TBD/stale fields and correlated against the Apr 27 Platform Weekly Status report. Applied 4 confident fixes: Beta Start on notes-notes-datagrid (Apr 1), GA Month on notes-bulk-general-notes (Jun 26), PRD URL on enrollment-dialog-bulk-services-section, PRD URL on integrations-zapier-improvements. Flagged 4 GA-date discrepancies for Ben's review (enrollment-dialog Apr 27 vs May 29; notes-datagrid Apr 23 vs Apr 27; locked-notes May 18 vs May 14 and Beta Apr 27 vs Apr 28; zapier Jun 1 vs Jun 11). All remaining nulls (Discovery Start, CEO Meeting/Next CEO Date, Launch Plan/PRD for non-tracked projects) are unresolvable without a fresh Asana harvest or manual input.

---

# Implementation Plan: Fix Bad Asana Dates & Null Fields

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Local (Gemma 2 27B)
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

A recent audit of the Q2 project intelligence records reveals a high volume of `null`, `TBD`, and `stale` values in critical date fields (e.g., **Discovery Start**, **GA Date**, **CEO Meeting**). These appear to be artifacts of incomplete Asana exports or unpopulated custom fields. Maintaining high-fidelity dates is critical for accurate strategic reporting and the "Pulse" of the repo.

## Logic

As the agent specialized in long-document parsing and intelligence refresh, **Local** should perform a data-quality pass across the Q2 project domain. The goal is to replace placeholders with actual data sourced from active status reports and project documentation.

## Execution Steps

1. **Identify Candidates**: Use `grep` or a scanning script to find all `.md` files in `intelligence/product/projects/q2/` containing `null`, `TBD`, `TBC`, or `stale`.
2. **Correlate with Status Reports**:
   - Read the [Latest Platform Status Report](reports/status/report.md).
   - Extract dates for initiatives mentioned in the report (e.g., *Notes Datagrid GA*, *Locked Notes QA*).
3. **Populate Missing Data**:
   - For each candidate file, determine if a correct date exists in the status report or other intelligence records.
   - Use `edit_intelligence` to update the record, replacing `null` with the correct `YYYY-MM-DD` or `Month YY` string.
4. **Flag Unresolvable Placeholders**: Create a summary list of records that still contain `null` values after the correlation pass, so Ben can provide manual inputs or trigger a fresh harvest.

## Verification

- [ ] `grep -r "null" intelligence/product/projects/q2` returns 0 hits in index files.
- [ ] Q2 Project records reflect the same milestones as the Platform Status report.
- [ ] No `invalid_type` or `malformed_frontmatter` errors are introduced during edits.
