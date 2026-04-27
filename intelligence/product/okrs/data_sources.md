---
Status: active
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Data Source Inventory

This document serves as the authoritative map for all data sources used to calculate Key Results (KRs) within the OKR Reporting skill. It details where each metric's components (Denominator and Numerator) are sourced.

---

## 🌐 Primary Data Sources

1.  **Google Analytics (GA4):** The primary source for user behavior, event tracking, and adoption metrics across various entry points.
2.  **Casebook Admin Reporting / Reveal BI:** Used for querying transactional data from the core Casebook database (e.g., Service Note creation counts, Enrollment records) AND serving as the primary source for Denominators in shortcut metrics.
3.  **ChurnZero/SQL:** Used for high-confidentiality tenant segmentation and external validation.

---

## 📊 KR Metric Mapping

### 1. Notes Quick Entry (Outside UOW)
*   **KR Definition:** % of Users with at least one Note created from a global entry point.
*   **Denominator Source:** GA4 (`noteSubmit` event). Counts unique users in the collection period.
*   **Numerator Source:** GA4. Union of specific, confirmed non-UOW events (e.g., `dashboardAddNoteOpen`, `EngageWLVAddNote`, `TrackServiceNoteNew`).
*   **SOP Reference:** `q2-2026/planning-services-at-scale/notes_quick_entry.md`

### 2. Service Notes — Data Entry Shortcuts
*   **KR Definition:** % of Tenants with a Service Note who used a shortcut.
*   **Denominator Source:** Reveal BI / Casebook DB (`cbp_service_notes`). Counts unique tenants with at least one Service Note.
*   **Numerator Source:** GA4 / Reveal BI. Tracks specific Data Entry Shortcut events fired by users associated with those notes.
*   **SOP Reference:** `q2-2026/planning-services-at-scale/service_notes_data_entry_shortcuts.md`

### 3. Enrollments — Data Entry Shortcuts
*   **KR Definition:** % of Tenants with an Enrollment who used a shortcut.
*   **Denominator Source:** Reveal BI / Casebook DB (`cbp_enrollments`). Counts unique tenants with at least one Enrollment record.
*   **Numerator Source:** GA4 / Reveal BI. Tracks specific Data Entry Shortcut events fired by users associated with those enrollments.
*   **SOP Reference:** `q2-2026/planning-services-at-scale/enrollments_data_entry_shortcuts.md`

### 4. Service Notes — Roster Association
*   **KR Definition:** % of Tenants with a Service Note whose user is in the Roster.
*   **Denominator Source:** Reveal BI / Casebook DB (`cbp_service_notes`). Counts unique tenants with at least one Service Note.
*   **Numerator Source:** Reveal BI (Complex Join). Requires joining `cbp_service_notes` to roster tables via service/user mapping to confirm user existence in the Roster.
*   **SOP Reference:** `q2-2026/planning-services-at-scale/service_notes_roster_association.md`

### 5. Q2 KR Baselines (General)
*   **Source:** `q2-2026/index.md`. This dashboard aggregates status and baseline values, referencing the specific SOPs above for measurement methodology.

### 6. Locked / Signed Notes
*   **KR Definition:** % of high-confidentiality tenants using locked or signed notes.
*   **Denominator Source:** ChurnZero / SQL — high-confidentiality tenant segment (validated via Margaux's sheet).
*   **Numerator Source:** Reveal BI — locked note count for high-conf tenants.
*   **SOP Reference:** `q2-2026/elevate-notes/locked_and_signed_notes.md`

### 16. Notes Datagrid Shortcuts
*   **KR Definition:** % of Users navigating to Notes via the datagrid shortcuts.
*   **Denominator Source:** GA4. Unique users on Notes landing page.
*   **Numerator Source:** GA4. Users with `NotesWLVAddNote` or `NotesWLVViewNote` (once live).
*   **SOP Reference:** `q2-2026/planning-services-at-scale/notes_datagrid_shortcuts.md`

---

## ⚠️ Data Integrity Notes

*   **Event Discovery:** For all shortcut metrics (2 & 3), event names must be confirmed via DevTools before final implementation. 
*   **Portal KRs:** All Portal-related KRs are currently blocked pending data model confirmation.
