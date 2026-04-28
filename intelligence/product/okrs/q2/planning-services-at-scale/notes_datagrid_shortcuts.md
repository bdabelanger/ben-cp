---
title: 'KR Measurement SOP: Notes Datagrid Navigation Shortcuts'
type: intelligence
domain: intelligence/product/okrs/q2/planning-services-at-scale
taxonomy: none
---
# KR Measurement SOP: Notes Datagrid Navigation Shortcuts

> [!NOTE]
> ⚙️ **STATUS:** Active — v1.0 (2026-04-08)
> KR Owner: Platform Team
> Period: Q2 2026
> Last updated: 2026-04-08

---

## 🎯 KR Definition

> *X% of Tenants who have ever used the Notes datagrid have at least one user
> who has used at least one new navigation shortcut in the Notes datagrid*

---

## 📐 Measurement Definition

### Denominator
**Tenants with at least one user who has created a Note**

| Field | Value |
| :--- | :--- |
| GA Event | `noteSubmit` |
| Scope | All tenants, filtered to engaged/active only |
| Window | Q2 2026 (April 1 – June 30) |

> **Rationale:** "Tenants who have ever used the Notes datagrid" is not
> directly measurable as a standalone event. `noteSubmit` (a Note was saved)
> is used as the qualifying signal — if a tenant is creating Notes, they have
> access to the datagrid context. This is the agreed proxy denominator.

---

### Numerator
**Tenants with at least one user who fired a navigation shortcut in the Notes datagrid**

| GA Event | Shortcut Type | Status |
| :--- | :--- | :--- |
| `NotesWLVFilterAdded` | Filter applied | ✅ Instrumented |
| `NotesQuickFilterApplied` | Quick filter applied | ✅ Instrumented |
| `NotesWLVColumnToggleHidden` | Column visibility changed | ✅ Instrumented |
| `NotesWLVColumnToggleVisible` | Column visibility changed | ✅ Instrumented |
| `NotesWLVDensityChange` | Density / display changed | ✅ Instrumented |
| `NotesWLVSort` | Sort column | ⚠️ **NOT INSTRUMENTED** |

> **Sort gap:** Sort is named in the KR definition ("sort, filter, or search")
> but `NotesWLVSort` does not exist in GA as of 2026-04-08. This is an open
> instrumentation gap. Baseline and targets are calculated **excluding sort**
> until this event is added. Flag for Engineering to add at next opportunity.
> Revisit baseline once instrumented — sort adoption will likely increase the %.

---

## 🗺️ How to Pull the Baseline (Path A — Self-Serve via GA)

1. Open Google Analytics → Casebook property
2. Navigate to your Notes datagrid dashboard (or Explore → Events report)
3. Set date range: **Q2 start (April 1, 2026) to present** for baseline pull;
   full Q2 (April 1 – June 30) for end-of-quarter measurement
4. Pull **denominator**: count of unique tenants with at least one `noteSubmit` event
5. Pull **numerator**: count of unique tenants with at least one of the
   instrumented shortcut events above (`NotesWLVFilterAdded`, `NotesQuickFilterApplied`,
   `NotesWLVColumnToggleHidden`, `NotesWLVColumnToggleVisible`, `NotesWLVDensityChange`)
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in the current period column (e.g., `April 2026`)
   - If first pull, enter in `Baseline` column
   - Add note: `Baseline pulled [date] from GA. Sort not yet instrumented — excluded from numerator.`

---

## 🎯 Target Setting

- **Beta baseline** (pre-GA): directional only — beta cohort not representative
- **Official Baseline:** March 2026 established at 39% based on beta cohort usage. Future pulls will confirm this trend.
- **Q2 target**: set after first full-month GA baseline is in hand; aim for
  modest adoption growth given early-stage feature
- **Target format**: use a specific **%** once denominator population is large
  enough; consider a raw **# of tenants** if denominator is small in early weeks

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| `NotesWLVSort` not instrumented | Sort interactions excluded from numerator | Flag to Engineering; add event at next opportunity |
| No dedicated "datagrid opened" event | Can't measure denominator as "tenants who opened datagrid" | Using `noteSubmit` as proxy — documented above |
| Tenant ID granularity | GA export may require custom dimension or BigQuery for tenant-level aggregation | Confirmed: tenant_id available in GA dashboard |

---

## 📊 Data Sources

See master inventory: `../../data_sources.md`

| Source | Usage | Link |
| :--- | :--- | :--- |
| Google Analytics | Primary — all shortcut events + denominator | [GA4 Analysis](https://analytics.google.com/analytics/web/#/analysis/a122185697p384028779/edit/aK7_-dWoRZSgOlSAKdeIRQ) |

---

## 🔗 Constituent Projects

The following initiatives contribute to this KR:
- [**Notes - Notes WLV / Datagrid**](../../../projects/q2/notes-notes-datagrid/overview.md)

---

## 🔗 References

- Parent procedure: `../../procedure.md`
- Status logic: `../../../../skills/status/schemas/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
