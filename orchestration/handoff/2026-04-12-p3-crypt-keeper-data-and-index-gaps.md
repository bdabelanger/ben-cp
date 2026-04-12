# Any Agent Implementation Plan: Data Sources Gap + Orphaned Index Entries

> **Prepared by:** Claude (Cowork) via knowledge skill run (2026-04-12)
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P3 — data quality gaps
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-12.md`
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-12**

---

## Context
The knowledge skill run on 2026-04-12 identified minor data quality gaps: one KR missing from `data_sources.md`, and two skill files not referenced in their parent index files.

---

## Execution Order

1. Add Locked/Signed Notes entry to `data_sources.md`
2. Add `character.md` reference to `skills/handoff/index.md`
3. Add `captains-log.md` reference to `skills/input/index.md`
4. Write changelog and mark complete

---

## Task 1: Update skills/okr-reporting/data_sources.md

Read `data_sources.md` first. Add a new KR entry after the existing entries:

```markdown
### 6. Locked / Signed Notes
*   **KR Definition:** % of high-confidentiality tenants using locked or signed notes.
*   **Denominator Source:** ChurnZero / SQL — high-confidentiality tenant segment (validated via Margaux's sheet).
*   **Numerator Source:** Reveal BI — locked note count for high-conf tenants.
*   **SOP Reference:** `q2-2026/elevate-notes/locked_and_signed_notes.md`
```

---

## Task 2: Update skills/handoff/index.md

Read `skills/handoff/index.md` first. Add a reference to `character.md`:

```markdown
- [character.md](./character.md) — Voice and persona definition for handoff skill
```

Place it in the files/documentation section, consistent with how other skill index files reference their character files.

---

## Task 3: Update skills/input/index.md

Read `skills/input/index.md` first. Confirm whether `captains-log.md` is referenced. If not, add:

```markdown
- [captains-log.md](./captains-log.md) — Session captain's log artifact
```

---

## Task 4: Changelog + Completion

Write changelog entries (subdirectory first at `skills/knowledge/changelog.md`, then root `changelog.md`), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- These are low-urgency quality fixes — read before every write, no exceptions.
- Character names are not used in skill references outside of `character.md` files.
