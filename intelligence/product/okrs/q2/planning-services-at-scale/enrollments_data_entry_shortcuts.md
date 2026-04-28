---
title: "KR Measurement SOP: Enrollments \u2014 Data Entry Shortcuts"
type: intelligence
domain: intelligence/product/okrs/q2/planning-services-at-scale
taxonomy: none
---
# KR Measurement SOP: Enrollments — Data Entry Shortcuts

> [!NOTE]
> ⚙️ **STATUS:** Drafting — v0.1 (2026-04-10)
> KR Owner: Platform Team
> Period: Q3 2026 (Targeting initial pull)
> Last updated: 2026-04-10

---

## 🎯 KR Definition

> *X% of Tenants who have at least one Enrollment created within the collection period have a user associated with that enrollment who utilized a specific Data Entry Shortcut.* 

---

## 📐 Measurement Definition

### Denominator
**Tenants with at least one Enrollment record in the collection period.**

| Field | Value |
| :--- |
| Data Source | Casebook Admin Reporting / Reveal BI (via `cbp_enrollments` table) |
| Scope | Tenants with at least one Enrollment record in the collection period (The eligible population pool) |
| Granularity | Tenant-level (This KR measures % of tenants, not % of users) |
| Window | Q3 2026 (July 1 – Sept 30) |

> **Rationale:** This is the qualifying signal for a tenant having used the Enrollment feature.

---

### Numerator
**Tenants where at least one user associated with an Enrollment fired a Data Entry Shortcut event.**

The shortcut usage must be tracked via specific GA events tied to enrollment actions, similar to how Notes use global entry points. Each confirmed shortcut event has its own GA event.

| GA Event | Shortcut Type | Status |
| :--- | :--- | :--- |
| [ENROLLMENT_SHORTCUT_EVENT_1] | [Shortcut Description 1] | [Status] |
| [ENROLLMENT_SHORTCUT_EVENT_2] | [Shortcut Description 2] | [Status] |
| ... | ... | ... |

> **Note:** The specific GA events for Enrollment Shortcuts must be discovered via DevTools, following the process documented in notes_quick_entry.md.

---

## 🔍 How to Discover New Entry Point Events

As new Enrollment shortcut entry points ship, confirm their GA event names before adding to the numerator. The reliable method:

1. Open the Casebook app in Chrome with **DevTools open** (F12 → Network tab or Application → GA debug)
2. Navigate to the enrollment action you want to confirm (e.g., Enrollment creation via a specific UI element)
3. Trigger the action (click "Create Enrollment" or equivalent)
4. Observe the GA event that fires — note the exact event name
5. Add it to the table above with ship date and status
6. Update this file with the new event and re-pull baseline if the change is material

> **This is the standard method for event discovery.** Always verify event names this way rather than assuming naming conventions carry over.

---

## 📊 Baseline Approach

This KR is an **additive metric** — the baseline grows as more shortcut types ship. Each pull should note which shortcut events were live at time of measurement.

| Pull date | Shortcut Events Included | Baseline value |
| :--- | :--- | :--- |
| *(first pull — TBD)* | [Initial set of confirmed Enrollment shortcut events] | TBD |
| *(Q3 pull — post new shortcuts)* | + New enrollment shortcut event(s) | TBD |

---

## 🗺️ How to Pull the Metric (Path A — Self-Serve via GA/Reveal BI)

1. **Determine Source:** Check `data_sources.md` for the primary source of enrollment shortcut events.
2. **If GA4:** Follow the process in notes_quick_entry.md, substituting Enrollment-specific events and using Tenant ID as the grouping dimension.
3. **If Reveal BI:** Execute a query joining `cbp_enrollments` to the relevant user/shortcut event logs, counting unique tenants where the shortcut event fired.
4. Pull **denominator**: count of unique tenants with at least one Enrollment record.
5. Pull **numerator**: count of unique tenants associated with a Data Entry Shortcut event (see table above).
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in current period column (e.g., `July 2026`)
   - If first pull, enter in `Baseline` column
   - Add note: `Baseline pulled [date] from [source]. Shortcut events confirmed live at time of pull: [list events].`

---

## 🎯 Target Setting

- **Target Setting Protocol (Per Procedure):** Target must be set *after* the initial baseline pull. If no explicit goal exists, propose a target based on reasonable growth assumptions (e.g., 10-20% improvement over baseline) and flag for stakeholder sign-off.
- **Target format**: Use a specific **%** once denominator population is large enough to support statistical significance.
---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| Enrollment shortcut events not yet instrumented | Numerator understates true adoption | Flag to Engineering; add event at next opportunity. |
| Denominator/Numerator mismatch | Inconsistent reporting if one source is delayed | Ensure both metrics are pulled in the same measurement window and note discrepancies. |

---

## 📊 Data Sources

See master inventory: `../../data_sources.md`

| Source | Usage | Link |
| :--- | :--- | :--- |
| Google Analytics / Reveal BI | Primary — shortcut event tracking and Enrollment denominator | [GA4 Analysis](https://analytics.google.com/analytics/web/#/analysis/a122185697p384028779/edit/aK7_-dWoRZSgOlSAKdeIRQ) |

---

## 🔗 Constituent Projects

The following initiatives contribute to this KR:
- [**Enrollment Dialog - Bulk Services Section**](../../../projects/q2/enrollment-dialog-bulk-services-section/overview.md)
- [**Services WLV - Bulk Actions**](../../../projects/q2/services-wlv-bulk-actions/overview.md)
- [**Service Plan Datagrid - Bulk Actions**](../../../projects/q2/services-service-plan-datagrid-with-bulk-actions/overview.md)

---

## 🔗 References

- Parent procedure: `../../procedure.md`
- Notes quick entry SOP: `./notes_quick_entry.md`
- Status logic: `../../../../skills/status/schemas/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
