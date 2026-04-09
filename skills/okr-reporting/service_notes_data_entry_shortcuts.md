# KR Measurement SOP: Service Notes — Data Entry Shortcuts

> [!NOTE]
> ⚙️ **STATUS:** Refining — v0.2 (2026-04-10)
> KR Owner: Platform Team
> Period: Q3 2026 (Targeting initial pull)
> Last updated: [Date of creation]

---

## 🎯 KR Definition

> *X% of Tenants who have at least one Service Note created have a user associated with that note who utilized a specific Data Entry Shortcut.* 

---

## 📐 Measurement Definition

### Denominator
**Tenants with at least one Service Note created.**

| Field | Value |
| :--- | :--- |
| Data Source | Casebook Admin Reporting / Reveal BI (via `cbp_service_notes` table) |
| Scope | All tenants, filtered to engaged/active only |
| Window | Q3 2026 (July 1 – Sept 30) |

> **Rationale:** This is the qualifying signal for a tenant having used the Service Notes feature.

---

### Numerator
**Tenants where at least one user associated with a Service Note fired a Data Entry Shortcut event.**

| GA Event | Shortcut Type | Status |
| :--- | :--- | :--- |
| [EVENT_NAME_1] | [Shortcut Description 1] | [Status] |
> *Note: Specific GA events must be discovered via DevTools, following the process in notes_quick_entry.md.*
| [EVENT_NAME_2] | [Shortcut Description 2] | [Status] |
| ... | ... | ... |

> **Note:** The specific GA events for Data Entry Shortcuts must be discovered via DevTools, similar to the process documented in `notes_quick_entry.md`. These placeholders will be populated after data acquisition.

---

## 🗺️ How to Pull the Baseline (Path A — Self-Serve via Reveal BI/GA)

1. **Determine Source:** Check `data_sources.md` for the primary source of shortcut events (likely GA4, but may require a join through Reveal BI).
2. **If GA4:** Follow the process in `notes_quick_entry.md`, substituting Service Note-specific events.
3. **If Reveal BI:** Execute a query joining `cbp_service_notes` to the relevant user/shortcut event logs, counting unique tenants where the shortcut event fired.
4. Pull **denominator**: count of unique tenants with at least one Service Note event.
5. Pull **numerator**: count of unique tenants associated with a Data Entry Shortcut event.
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in current period column (e.g., `July 2026`)
   - If first pull, enter in `Baseline` column
   - Add note: `Baseline pulled [date] from [source]. Shortcut events confirmed live at time of pull: [list events].`

---

## 🎯 Target Setting

- **Q3 target:** Set after initial baseline is confirmed; aim for modest adoption growth.
- **Target format**: Use a specific **%** once denominator population is large enough.

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| Shortcut events not yet instrumented | Numerator understates true adoption | Flag to Engineering; add event at next opportunity. |
| Denominator/Numerator mismatch | Inconsistent reporting if one source is delayed | Ensure both metrics are pulled in the same measurement window and note discrepancies. |

---

## 📊 Data Sources

See master inventory: `okr-reporting/data_sources.md`

| Source | Usage | Link |
| :--- | :--- | :--- |
| Google Analytics / Reveal BI | Primary — shortcut event tracking and Service Note denominator | [GA4 Analysis](https://analytics.google.com/analytics/web/#/analysis/a122185697p384028779/edit/aK7_-dWoRZSgOlSAKdeIRQ) |

---

## 🔗 References

- Parent procedure: `okr-reporting/procedure.md`
- Status logic: `skills/skill-builder/mappings/status_mapping.md`
- Visual standards: `skills/skill-builder/styles/emoji_key.md`
