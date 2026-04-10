# Initiative: Planning Services at Scale — Index

> This directory contains KR SOPs and measurement documentation specific to the
> "Planning Services at Scale" initiative for Q2 2026.
>
> **All agents:** read `AGENTS.md` at the vault root before modifying any file here.

---

## 📋 KR Status Dashboard

| KR | Status | Baseline | Target | SOP |
| :--- | :--- | :--- | :--- | :--- |
| **Service Notes — Roster Assoc.** | ✅ Unblocked | Queryable (Reveal) | ⏳ TBD | [SOP](./service_notes_roster_association.md) |
| **Notes Datagrid Shortcuts** | ⏳ Pending | Pending April pull | ⏳ TBD | [SOP](./notes_datagrid_shortcuts.md) |
| **Service Plan Shortcuts** | 🛑 Blocked | Pending launch | 🛑 Blocked | *(pending)* |
| **Service Notes Shortcuts** | 🟡 Partial | Pullable | 🟡 Estimated | [SOP](./service_notes_data_entry_shortcuts.md) |
| **Enrollments Shortcuts** | 🟡 Partial | Pullable | 🟡 Estimated | [SOP](./enrollments_data_entry_shortcuts.md) |

---

## 🛠️ Detailed Metadata & Next Steps

### 1. Service Notes — Roster Association
- **Sources:** Casebook Admin Reporting / Reveal BI
- **Next steps:**
  - Pull baseline in Reveal BI — join `cbp_service_notes` + `cbp_services` on `service_id`, filter `rostering = true`.
  - Set target once baseline is in hand.

### 2. Notes Datagrid Navigation Shortcuts
- **Sources:** Google Analytics (tenant_id confirmed available)
- **Next steps:**
  - Pull April baseline from GA — see SOP for full instructions.
  - Flag `NotesWLVSort` gap to Engineering.

### 3. Service Plan Datagrid Navigation Shortcuts
- **Sources:** TBD — GA / ChurnZero at launch (GA 5/28)
- **Next steps:**
  - Create KR measurement SOP at launch.

### 4. Data Entry Shortcuts (Service Notes & Enrollments)
- **Sources:** GA, ChurnZero, Casebook Admin Reporting.
- **Next steps:**
  - Pull prod baseline for currently-live shortcuts.
  - Identify comp feature for targets.

---

## 🔗 References

- Parent Q2 Index: `../index.md`
- Master OKR Index: `../../index.md`
- Status logic: `../../../skill-builder/mappings/status_mapping.md`
- Visual standards: `../../../skill-builder/styles/emoji_key.md`
