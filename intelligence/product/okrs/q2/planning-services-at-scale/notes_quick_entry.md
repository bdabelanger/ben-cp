---
title: KR Measurement SOP Notes Quick Entry (Outside UOW)
type: intelligence
domain: intelligence/product/okrs/q2/planning-services-at-scale
---

# KR Measurement SOP: Notes Quick Entry (Outside UOW)

> [!NOTE]
> ⚙️ **STATUS:** Baseline Set — v1.2 (2026-04-10)
> KR Owner: Platform Team
> Period: Q2 2026
> Last updated: 2026-04-10

---

## 🎯 KR Definition

> *X% of Users with at least one Note created within the collection period have
> created a Note from a global entry point (outside UOW)*

---

## 📐 Measurement Definition

### Denominator
**Users with at least one Note created in the collection period**

| Field | Value |
| :--- | :--- |
| GA Event | `noteSubmit` |
| Scope | All tenants, filtered to engaged/active only |
| Granularity | User-level (not tenant-level — this KR measures % of users, not % of tenants) |
| Window | Q2 2026 (April 1 – June 30) |

---

### Numerator
**Users who created a Note from a global entry point (outside UOW)**

The non-UOW distinction is determined by **which entry point fired the Note creation**, not by the `noteSubmit` event itself (which is generic). Each confirmed non-UOW entry point has its own GA event.

| GA Event | Entry Point | Status |
| :--- | :--- | :--- |
| `EngageWLVAddNote` | Engage WLV | ✅ Instrumented (Baseline established) |
| 

> **Exclusions:** `dashboardAddNoteOpen` is excluded from the current baseline calculation as it was disabled during testing. Future pulls will decide on its inclusion.

---

## 🔍 How to Discover New Entry Point Events

As new Note entry points ship, confirm their GA event names before adding to
the numerator. The reliable method:

1. Open the Casebook app in Chrome with **DevTools open** (F12 → Network tab
   or Application → GA debug)
2. Navigate to the entry point you want to confirm (e.g., Notes WLV, a specific
   WLV add button)
3. Trigger the action (click "Add Note" or equivalent)
4. Observe the GA event that fires — note the exact event name
5. Add it to the table above with ship date and status
6. Update this file with the new event and re-pull baseline if the change is
   material

> **This is the standard method for event discovery.** Always verify event
> names this way rather than assuming naming conventions carry over.

---

## 📊 Baseline Approach

This KR has an established baseline based on beta cohort usage:

| Pull date | Entry points included | Baseline value |
| :--- | :--- | :--- |
| March 2026 (Beta) | `EngageWLVAddNote`, `TrackServiceNoteNew` | **49%** (174/357) |

---

## 🗺️ How to Pull the Metric (Path A — Self-Serve via GA)

1. Open Google Analytics → Casebook property
2. Navigate to your Notes quick entry dashboard (or Explore → Events report)
3. Set date range: **April 1, 2026 to present** for trend analysis; full Q2 for end-of-quarter measurement.
4. Pull **denominator**: count of unique users with at least one `noteSubmit` event
5. Pull **numerator**: count of unique users with at least one of the confirmed live non-UOW entry point events (see table above).
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in current period column (e.g., `April 2026`)
   - If first pull, enter in `Baseline` column
   - Add note:
     > `Trend analysis pulled [date] from GA. Baseline established March 2026 at 49%. Events live at pull: [list events]. Excluded (not yet shipped): [list].`

---

## 🎯 Target Setting

- **Q2 target:** Maintain or slightly exceed the initial beta baseline of 49% as we monitor for overlap with new Notes WLV features.
- **Future Growth:** The Q3/Q4 targets will be set *after* Notes WLV events ship, anticipating a material increase in adoption.
- **Target format:** Use a specific **%** once denominator population is large enough; revisit at each major event launch.

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| `EngageWLVAddNote` context unconfirmed | May be UOW, not non-UOW | Confirm with dev tools before including in numerator |
| Remaining WLV entry points not yet live | Numerator understates true adoption | Document which entry points are live at each pull; add events as they ship |
| Metric is additive as shortcuts ship | Baseline shifts at each new launch | Date every baseline snapshot; note shortcuts live at time of pull |
| No single "non-UOW note created" event | Must union multiple entry point events | Maintain this event table as entry points ship |

---

## 🔗 Constituent Projects

The following initiatives contribute to this KR:
- [**Notes - Notes WLV / Datagrid**](../../../projects/q2/notes-notes-datagrid/index.md)
- [**Notes - Global Notes WLV**](../../../projects/q2/notes-global-notes-wlv-(1210368097846960).md)

---

## 🔗 References

- Parent procedure: `../../procedure.md`
- Notes datagrid SOP: `./notes_datagrid_shortcuts.md`
- Status logic: `../../../../skills/status/schemas/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
