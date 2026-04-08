# OKR Reporting Changelog

> Detail log for `skills/okr-reporting/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

---

## [1.1.0] - Initial OKR Reporting SOPs (2026-04-08)

**Files created/modified:**
- `procedure.md` — evergreen runbook v1.1; quarterly content removed
- `2026-q2-kr-reference.md` — Q2 KR baseline status, migrated from Google Doc
- `notes_datagrid_shortcuts.md` — restored after Gemma overwrite damage; full canonical content
- `notes_quick_entry.md` — full KR measurement SOP (denominator: noteSubmit, numerator: 3 GA events)
- `index.md` — TOC with file type guide
- `data_sources.md` — stub created; not yet populated

**KR State:**
- Notes Quick Entry (Outside UOW): ✅ Baseline ~32%, Target 40% — live entry points only
- Notes Datagrid Navigation Shortcuts: ⏳ Pending — GA live 2026-04-09, first pull in May
- Notes WLV Adoption: 🛑 Blocked — feature not live (Beta 6/25, GA 7/27)
- Locked/Signed Notes: 🟡 Proxy — Locked Notes only; Signed Notes not live
- Bulk Import for Notes: 🟡 Partially blocked — needs CX ops input (Cierra); move to Q3
- Service Notes — Roster Association: ✅ Unblocked — queryable in Reveal BI; pull ready
- Service Plan Datagrid Shortcuts: 🛑 Blocked — not live (GA 5/28)
- Service Notes — Data Entry Shortcuts: 🟡 Partial — some shortcuts live; comp TBD
- Enrollments — Data Entry Shortcuts: 🟡 Partial — some shortcuts live; comp TBD
- Zapier — Custom Fields: 🟡 Proxy — Zapier Insights exploration needed
- Portal KRs (×3): 🛑 Blocked — data model unstable; all three unblock together

**Blockers:**
- `EngageWLVAddNote` — context unconfirmed (inside UOW or outside?); Ben to check via dev tools
- `NotesWLVSort` GA event — NOT INSTRUMENTED; flagged for Engineering
- `data_sources.md` — stub only; needs cross-reference against all KR SOPs

**TODOs:**
1. Confirm `EngageWLVAddNote` UOW vs. non-UOW context — update `notes_quick_entry.md` numerator
2. Discover additional Notes Quick Entry entry point events via dev tools
3. Pull Notes Datagrid April baseline from GA after first full month post-launch
4. Populate `data_sources.md` by cross-referencing all KR SOPs in this directory
5. Create KR SOPs for remaining unblocked KRs (Service Notes Roster Association, Data Entry Shortcuts)
6. Set Notes Datagrid target after April baseline pull
