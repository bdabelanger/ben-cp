# Data Sources Inventory: OKR Reporting Skill

> [!NOTE]
> ⚠️ **PROCESS TYPE:** Manual Workflow (Not API Driven)
> This document inventories the tools, systems, and vault references used to
> acquire metric values for Platform KR measurement.
> Last updated: 2026-04-08

---

## 📊 Metric Sources by System

### Google Analytics (GA4)
Self-serve. Used for user behavior tracking across Notes and WLV features.

| Event | Used For | KR |
| :--- | :--- | :--- |
| `noteSubmit` | Denominator — users who created a note | Notes Quick Entry, Notes Datagrid |
| `dashboardAddNoteOpen` | Numerator — global entry point | Notes Quick Entry |
| `EngageWLVAddNote` | Numerator — WLV entry point (UOW context TBC) | Notes Quick Entry |
| `TrackServiceNoteNew` | Numerator — service note entry point | Notes Quick Entry |
| `NotesWLVFilterAdded` | Numerator — datagrid shortcut usage | Notes Datagrid |
| `NotesQuickFilterApplied` | Numerator — datagrid shortcut usage | Notes Datagrid |
| `NotesWLVColumnToggleHidden` | Numerator — datagrid shortcut usage | Notes Datagrid |
| `NotesWLVColumnToggleVisible` | Numerator — datagrid shortcut usage | Notes Datagrid |
| `NotesWLVDensityChange` | Numerator — datagrid shortcut usage | Notes Datagrid |
| `NotesWLVSort` | ⚠️ NOT INSTRUMENTED — flagged for Engineering | Notes Datagrid |

**GA property:** All one property. Tenant ID available as a dimension.
**Pull instructions:** See individual KR SOPs in `skills/okr-reporting/`.

---

### Casebook Admin Reporting / Reveal BI
Self-serve SQL-style queries via Reveal BI. Used for service/enrollment adoption metrics.

**Reference docs:** `skills/casebook/reporting/` — consult these before writing any query:

| File | Covers |
| :--- | :--- |
| `casebook-cases.md` | Case entity schema and key fields |
| `casebook-intake.md` | Intake entity schema |
| `casebook-people.md` | Person entity schema |
| `casebook-tenants.md` | Tenant entity schema — use for tenant segmentation |
| `casebook-users.md` | User entity schema — use for user-level metrics |
| `reveal_bi_syntax.md` | Query syntax reference for Reveal BI |
| `reveal_bi_visualizations.md` | Visualization and output formatting |

**KRs that use this source:**
- Service Notes — Roster Association (`cbp_service_notes` + `cbp_services`, join on `service_id`)
- Locked/Signed Notes — high-confidentiality tenant segment (validate with Margaux's sheet)
- Service Notes / Enrollments — Data Entry Shortcuts (baseline pullable from prod)

---

### ChurnZero
Used for tenant-level adoption and NPS metrics. Acquisition: self-serve dashboard.

**KRs that use this source:**
- Notes WLV Adoption (post-launch)
- Locked/Signed Notes (post-launch, alongside SQL)

---

### CX Ops (Cierra)
Manual — request from Cierra. Used for migration/import volume data.

**KRs that use this source:**
- Bulk Import for Notes — paid migration volume comp

---

### SQL via Data team (Path B)
Delegated query. Used when self-serve sources don't cover the needed dimension.

**KRs that use this source:**
- Portal KRs (×3) — blocked pending data model confirmation
- Any metric requiring `external_user_invitations` or session-level data

---

## ⚠️ Gaps and TODOs

- [ ] `EngageWLVAddNote` — confirm UOW vs. non-UOW context via dev tools; update Notes Quick Entry numerator
- [ ] Additional Notes Quick Entry entry point events — Ben to discover via dev tools
- [ ] Zapier Insights — explore with Engineering for Zapier Custom Fields KR
- [ ] Super Admin `API Access` flag — verify in tenants table for Zapier entitlement
- [ ] Portal data model — all three Portal KRs unblock together once confirmed
