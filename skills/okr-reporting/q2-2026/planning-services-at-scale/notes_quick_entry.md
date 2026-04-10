# KR Measurement SOP: Notes Quick Entry (Outside UOW)

> [!NOTE]
> ⚙️ **STATUS:** Active — v1.0 (2026-04-08)
> KR Owner: Platform Team
> Period: Q2 2026
> Last updated: 2026-04-08

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

| GA Event | Entry Point | Ships | Status |
| :--- | :--- | :--- | :--- |
| `dashboardAddNoteOpen` | Dashboard | ✅ Live | ✅ Instrumented |
| `EngageWLVAddNote` | Engage WLV | ✅ Live | ⚠️ Confirm UOW vs non-UOW context (see note below) |
| `TrackServiceNoteNew` | Services Track view | ✅ Live | ✅ Instrumented — confirm scope |
| `NotesWLV*` entry point | Notes WLV | Beta 6/25 / GA 7/27 | ⏳ Not yet live — Q3 |
| Intake WLV entry point | Intake WLV | TBD | ⏳ Pending — confirm event name |
| Providers WLV entry point | Providers WLV | TBD | ⏳ Pending — confirm event name |
| Services WLV entry point | Services WLV | TBD | ⏳ Pending — confirm event name |
| *(additional entry points)* | *(to be added)* | TBD | 🔍 Discover via dev tools — see below |

> **`EngageWLVAddNote` context note:** Name suggests Engage WLV (global list,
> non-UOW) but could fire from within an Engage record (UOW). Confirm which
> context this fires in before including in numerator.

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

This KR is an **additive metric** — the baseline grows as more entry points
ship. Each pull should note which entry points were live at time of measurement.

| Pull date | Entry points included | Baseline value |
| :--- | :--- | :--- |
| *(first pull — TBD)* | `dashboardAddNoteOpen`, `EngageWLVAddNote`, `TrackServiceNoteNew` | TBD |
| *(Q3 pull — post Notes WLV)* | + Notes WLV entry point | TBD |

---

## 🗺️ How to Pull the Metric (Path A — Self-Serve via GA)

1. Open Google Analytics → Casebook property
2. Navigate to your Notes quick entry dashboard (or Explore → Events report)
3. Set date range: **April 1, 2026 to present** for baseline; full Q2 for
   end-of-quarter measurement
4. Pull **denominator**: count of unique users with at least one `noteSubmit` event
5. Pull **numerator**: count of unique users with at least one of the confirmed
   live non-UOW entry point events (see table above — live entries only)
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in current period column (e.g., `April 2026`)
   - If first pull, enter in `Baseline` column
   - Add note:
     > `Baseline pulled [date] from GA. Entry points live at pull: [list events]. Excluded (not yet shipped): [list].`

---

## 🎯 Target Setting

- **Q2 target:** Focus on already-live entry points only (`dashboardAddNoteOpen`,
  `EngageWLVAddNote`, `TrackServiceNoteNew`). Set directional target from first
  full-month GA pull.
- **Q3 additive target:** Set separately once Notes WLV and remaining WLV entry
  points ship — baseline will expand materially.
- **Target format:** # of users is cleaner than % given rolling baseline; revisit
  at each new entry point launch.

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| `EngageWLVAddNote` context unconfirmed | May be UOW, not non-UOW | Confirm with dev tools before including in numerator |
| Remaining WLV entry points not yet live | Numerator understates true adoption | Document which entry points are live at each pull; add events as they ship |
| Metric is additive as shortcuts ship | Baseline shifts at each new launch | Date every baseline snapshot; note shortcuts live at time of pull |
| No single "non-UOW note created" event | Must union multiple entry point events | Maintain this event table as entry points ship |

---

## 🔗 References

- Parent procedure: `../../procedure.md`
- Notes datagrid SOP: `./notes_datagrid_shortcuts.md`
- Status logic: `../../../skill-builder/mappings/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
