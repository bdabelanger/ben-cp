# Implementation Plan: 2026-04-13-p3-crypt-keeper-data-quality-gaps

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Gemma
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P3
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

# Any Agent Implementation Plan: P3 Crypt-Keeper — Data Quality Gaps

> **Prepared by:** Claude (Cowork) (Crypt-Keeper scheduled run, 2026-04-13)
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P3 — Data quality gaps (missing KR SOP files, data_sources.md sync, stale migration debt flags)
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-13.md`
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

## Context

The 2026-04-13 Crypt-Keeper run found that `product/projects/data_sources.md` references 6 KR SOP files that do not exist on disk. It also found `shared/separation-policy.md` migration debt items from 2026-04-12 that are still open (one script migration and 7 ephemeral notes.md files — the notes.md items overlap with P2). These are data integrity gaps that leave agents operating on incomplete references.

---

## Execution Order

1. **Task 1** — Investigate and document missing KR SOP files
2. **Task 2** — Check migration debt: `intelligence/report/run.py` script
3. **Task 3** — Update stale Portal KR blocker status in data_sources.md
4. **Task 4** — Write changelog and mark complete

---

## Task 1: Missing KR SOP Files

`product/projects/data_sources.md` references the following SOP files under `q2-2026/`, none of which exist on disk:

| Referenced Path | KR Name |
| :--- | :--- |
| `q2-2026/planning-services-at-scale/notes_quick_entry.md` | Notes Quick Entry (Outside UOW) |
| `q2-2026/planning-services-at-scale/service_notes_data_entry_shortcuts.md` | Service Notes — Data Entry Shortcuts |
| `q2-2026/planning-services-at-scale/enrollments_data_entry_shortcuts.md` | Enrollments — Data Entry Shortcuts |
| `q2-2026/planning-services-at-scale/service_notes_roster_association.md` | Service Notes — Roster Association |
| `q2-2026/planning-services-at-scale/notes_datagrid_shortcuts.md` | Notes Datagrid Shortcuts |
| `q2-2026/elevate-notes/locked_and_signed_notes.md` | Locked / Signed Notes |

Also referenced: `q2-2026/index.md` — does not exist.

**Action:** Determine whether these files were never created (gap to fill) or were removed/moved. Check git history:
```
git log --oneline --all -- skills/product/projects/q2-2026/
```
If they were never created: flag for human user as Q2 OKR documentation debt — do not fabricate content. If they existed and were removed: restore from git. Note that Gemma's 2026-04-13 session note indicates documentation is "In Progress" for the Notes Datagrid Shortcut KR specifically.

---

## Task 2: Migration Debt — intelligence/report/run.py

`shared/separation-policy.md` lists this as open migration debt:
> `skills/intelligence/report/run.py` — execution script (→ `tools/intelligence-report/`)

Verify whether `run.py` still exists at `intelligence/report/run.py` (it is not in the vault listing, suggesting it may be at the tools layer already or was removed). Check:
```
git log --oneline --all -- skills/intelligence/report/run.py
ls tools/intelligence-report/
```
If migration is complete: mark ✅ in `shared/separation-policy.md`. If not: create a sub-handoff or flag for the appropriate agent.

---

## Task 3: Update Portal KR Blocker Status

`product/projects/data_sources.md` states:
> "Portal KRs: All Portal-related KRs are currently blocked pending data model confirmation."

This entry has no date. Verify current status with human user or check recent notes for Portal data model updates. If the blocker is resolved, update the data_sources.md entry with a resolved date and new status. If still blocked, add a date stamp so future audits can track age.

---

## Task 4: Changelog + Completion

Write changelog entries (subdirectory `knowledge` first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Do not fabricate KR SOP content — flag as debt for human user to provide
- Read before every write — no exceptions
- Task 1 is the highest-value action in this handoff; prioritize it
