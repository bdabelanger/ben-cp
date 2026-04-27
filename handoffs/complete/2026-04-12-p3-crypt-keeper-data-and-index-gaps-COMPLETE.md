---
title: 'Any Agent Implementation Plan: Data Sources Gap + Orphaned Index Entries'
type: handoff
domain: handoffs/complete
---


# Any Agent Implementation Plan: Data Sources Gap + Orphaned Index Entries

> **Prepared by:** Claude (Cowork) via knowledge skill run (2026-04-12)
> **Reviewed by:** Claude (Cowork) (2026-04-12) — file state verified against vault
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P3 — data quality gaps
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-12.md`
> **v1.2**
> **STATUS**: ✅ COMPLETE

Added KR #6 (Locked/Signed Notes) to skills/product/okr-reporting/data_sources.md. Tasks 2 and 3 from the original report were invalidated: character content now lives in report.md files (no standalone character.md), and skills/input/ does not exist in the vault. Changelog written at okr-reporting and root level.

**Changelog:** (see root changelog.md)


---

## Context
The knowledge skill run on 2026-04-12 identified a data quality gap: one KR missing from `data_sources.md`. Two other tasks from the original report were invalidated on review — see findings below.

---

## Pre-Execution Findings (Verified 2026-04-12)

- **Task 1 (data_sources.md):** Confirmed gap. KRs 1–5 and 16 are present; entry for Locked/Signed Notes (proposed as #6) is missing. Existing numbering is non-sequential (5 → 16) — intentional, do not renumber.
- **Task 2 (handoff/index.md character.md):** Invalidated. Character content now lives in `report.md` files — no standalone `character.md` files are used. Skip.
- **Task 3 (skills/input/index.md):** Invalidated. `skills/input/` does not exist in the vault. Source report reference was stale. Skip.

---

## Execution Order

1. Add Locked/Signed Notes entry to `data_sources.md`
2. Write changelog and mark complete

---

## Task 1: Update skills/product/okr-reporting/data_sources.md

Read `data_sources.md` first. Add a new KR entry **after the existing ### 5 block and before ### 16**:

```markdown
### 6. Locked / Signed Notes
*   **KR Definition:** % of high-confidentiality tenants using locked or signed notes.
*   **Denominator Source:** ChurnZero / SQL — high-confidentiality tenant segment (validated via Margaux's sheet).
*   **Numerator Source:** Reveal BI — locked note count for high-conf tenants.
*   **SOP Reference:** `q2-2026/elevate-notes/locked_and_signed_notes.md`
```

Do not renumber KR #16.

---

## Task 2: Changelog + Completion

Write changelog entries (subdirectory level at `skills/product/okr-reporting/changelog.md`, then root `changelog.md`). Note in the changelog that Tasks 2 and 3 from the original report were invalidated: character content is now in `report.md` files, and `skills/input/` does not exist.

Then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Read before every write — no exceptions.
- Do not create `character.md` files — character content lives in `report.md` per current convention.
- Do not create `skills/input/` — it was a stale reference in the source report.
