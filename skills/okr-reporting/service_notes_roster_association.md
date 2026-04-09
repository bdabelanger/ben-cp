# KR Measurement SOP: Service Notes — Roster Association

> [!NOTE]
> ⚙️ **STATUS:** Draft — v0.1 (2026-04-XX)
> KR Owner: Platform Team
> Period: Q3 2026 (Targeting initial pull)
> Last updated: [Date of creation]

---

## 🎯 KR Definition

> *X% of Tenants who have at least one Service Note created have a user associated with that note in the Roster.*

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
**Tenants where at least one user associated with a Service Note exists in the Roster.**

| Data Source | Logic | Status |
| :--- | :--- | :--- |
| Reveal BI (Join)
| Join `cbp_service_notes` to `cbp_services`, then join to `cbp_users` via service/user mapping. Count unique tenants where the joined user record exists. |
| **Status** | ✅ Defined by Schema Reference in `data_sources.md` |

> **Note:** This requires a specific, complex SQL-style query within Reveal BI that joins multiple entity tables.

---

## 🗺️ How to Pull the Baseline (Path A — Self-Serve via Reveal BI)

1. Navigate to your saved report/dashboard in Reveal BI for Service Notes adoption.
2. Apply required filters:
   - **Tenant scope:** Active tenants only.
   - **Date range:** Q3 2026 start to present for baseline pull; full Q3 for EOC measurement.
3. Execute the pre-defined query that joins `cbp_service_notes` and verifies user existence in the Roster tables.
4. Pull **denominator**: count of unique tenants with at least one Service Note event.
5. Pull **numerator**: count of unique tenants where the associated service note record successfully links to an existing rostered user.
6. Calculate: `Numerator ÷ Denominator = %`
7. Record in Work Planning Register:
   - Enter % in current period column (e.g., `July 2026`)
   - If first pull, enter in `Baseline` column
   - Add note: `Baseline pulled [date] from Reveal BI query. Schema reference: casebook/reporting/`

---

## 🎯 Target Setting

- **Q3 target:** Set after initial baseline is confirmed; aim for a high adoption rate given the feature's importance.
- **Target format**: Use a specific **%** once denominator population is large enough.

---

## ⚠️ Known Issues & Gaps

| Issue | Impact | Resolution |
| :--- | :--- | :--- |
| Query complexity in Reveal BI | Requires precise knowledge of entity joins (see `data_sources.md`) | Consult with Casebook Admin team for query validation before running against production data. |
| Roster definition ambiguity | If 