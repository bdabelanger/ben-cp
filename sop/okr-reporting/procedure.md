# Procedure: OKR Baseline & Target Establishment

> [!NOTE]
> ⚙️ **STATUS:** Active — v1.1 (2026-04-08)
> Evergreen runbook — no quarterly content lives here.
> For current KR baseline status and next steps, see the quarterly reference file below.

---

## 🎯 Goal

Populate the `Baseline` and `Target` columns in the Work Planning Register for
any Platform KR currently showing `X%`, `Needs baseline`, `In progress`, or a
blank value, so that the status mapping logic in
`sop/skill-builder/mappings/status_mapping.md` can be applied consistently going forward.

---

## 📅 Quarterly KR Reference

The per-KR baseline status, confirmed values, targets, and next steps live in
a separate quarterly file — not here. This keeps the runbook evergreen.

| Quarter | File |
| :--- | :--- |
| Q2 2026 | `okr-reporting/2026-q2-kr-reference.md` |

> When a new quarter begins, create `[year]-[quarter]-kr-reference.md` and
> add it to the table above. Archive the previous quarter's file in place.

---

## 📋 Pre-Flight Checklist

Before starting any KR, confirm:
- [ ] The KR is marked `In? = Yes` or `Stretch` in the register
- [ ] The KR has a defined `Data Source` column value (if blank → see Step 0)
- [ ] You know the acquisition path (see Step 1)
- [ ] The feature the KR measures has shipped, or a proxy baseline approach has been agreed (see quarterly reference)

---

## 🗺️ Execution Steps

### Step 0: Triage the KR

**When:** KR has no `Data Source` listed, status is `Pending release`, or
feature is not yet shipped.

**Action:** Skip this KR for now. Log in the register Notes column:
> `Baseline deferred — [reason]. Revisit: [target date or milestone]`

**Decision point:** If `Pending release` but the feature has since shipped,
proceed to Step 1. If a proxy baseline approach has been agreed (see quarterly
reference), proceed to Step 2A or 2B using the proxy method noted there.

---

### Step 1: Identify the Acquisition Path

Check the `Data Source` column and route accordingly:

| Data Source | Path |
| :--- | :--- |
| Casebook Admin Reporting / Reveal BI | **Path A** → Self-serve (Step 2A) |
| ChurnZero | **Path A** → Self-serve (Step 2A) |
| HubSpot | **Path A** → Self-serve (Step 2A) |
| Google Analytics | **Path A** → Self-serve (Step 2A) |
| SQL query | **Path B** → Delegated to Data team (Step 2B) |
| Multiple sources listed | Run each source independently; combine values |
| No source listed | Stop — define source before proceeding |

> **Note on DB access:** Direct SQL access is not available. Any KR requiring
> a raw DB query must go through Path B (Data team) or wait for a pipeline
> to be scoped via API. See `okr-reporting/data_sources.md`.

---

### Step 2A: Self-Serve Pull (Casebook Admin / Reveal BI / ChurnZero / HubSpot / GA)

1. Navigate to the relevant saved report or dashboard for this KR
2. Apply required filters:
   - **Tenant scope:** Active/engaged tenants only unless KR specifies otherwise
     (apply disengaged tenant filter via `cbp_active_users` join on `tenant_id`
     where used in Reveal BI)
   - **Date range:** Use the KR's `Period` column:
     - `Full Year` → Jan 1 2026 – present (or full year 2025 for historical baseline)
     - `Q1 / Q2 / Q3 / Q4` → Start of that quarter to present
3. Locate the specific metric matching the KR definition
4. Record the raw value in the register under the appropriate period column
   (e.g., `April 2026` column if pulling today)
5. Enter the value in the `Baseline` column if no baseline exists yet
6. Add a note in the `Notes` column:
   > `Baseline pulled [date] from [source / report name]. Shortcuts live at time of pull: [list if applicable]`

**Decision point:** If the saved report doesn't exist or is broken → switch to
Path B and note: `Report unavailable as of [date] — Data team notified`.

---

### Step 2B: Delegated Pull (SQL / No DB Access)

1. Copy the exact KR text from the register
2. Note all filter criteria from the `Notes` column (tenant scope, date range,
   cohort definitions, exclusions, disengaged tenant filter)
3. Send a request to the Data team with:
   - KR text (verbatim)
   - Desired output: single % or count value
   - Date range / cohort definition
   - Deadline needed by
4. When the value is returned, follow steps 3–6 from Path A above
5. Log the Data team member who ran the query in `Notes` for traceability

**Decision point:** If Data team turnaround is > 2 business days and KR is
blocking a reporting deadline → flag in Asana and note:
> `Baseline pending — Data team [name], requested [date]`

---

### Step 3: Set the Target

Once the baseline is confirmed:

1. Review the KR text — most targets are implied in the wording
   (e.g., "from X% to Y%", "at least N tenants", "≤ threshold")
2. If Target is still `X%` or `Needs launch plan`:
   - Use baseline + reasonable growth assumption (10–20% improvement, or match
     a stated business goal or comparable feature's adoption curve)
   - For beta-window KRs, set target as a specific count of beta tenants rather
     than a % (cleaner signal at small N)
   - Flag for stakeholder alignment before locking:
     > `Target proposed: [value]. Needs sign-off — [person / date]`
3. Enter the confirmed Target in the `Target` column
4. Update `Notes` with rationale:
   > `Target = [value] based on [reasoning / source / comp]`

---

### Step 4: Apply Status Mapping

With Baseline and Target both populated, apply health logic from
`sop/skill-builder/mappings/status_mapping.md`:

- Pull the most recent actual value from the current period column
- Calculate progress: `Current ÷ Target`
- Apply the mapping:
  - ≥ 100% → ✅ Achieved
  - 80–99% → ⚠️ At Risk
  - < 80% → ❌ Missed
  - Current value null → 👀 Needs Attention (Data)
  - Target null → 🎯 On Track / Unknown

---

## ⚠️ Failure Handling

| Situation | Action |
| :--- | :--- |
| Report / dashboard broken or inaccessible | Switch to Path B; note date |
| Data team doesn't have access to the metric | Escalate to Engineering for pipeline scoping |
| KR definition is ambiguous (can't tell what to measure) | Stop; align with Objective owner before pulling any data |
| Baseline pull returns unexpected outlier | Note in register; do not enter until confirmed with Data team |
| Feature not yet shipped | Use agreed proxy baseline (see quarterly reference) or defer with dated note |
| Metric stacks as new shortcuts/entry points ship | Note which shortcuts were live at time of baseline pull; revisit at each launch |

---

## 🔗 References

- Quarterly KR reference: `okr-reporting/2026-q2-kr-reference.md`
- Data source inventory: `okr-reporting/data_sources.md`
- KR-specific measurement SOPs: `okr-reporting/notes_datagrid_shortcuts.md`, `okr-reporting/notes_quick_entry.md`
- Status logic: `sop/skill-builder/mappings/status_mapping.md`
- Visual standards: `sop/skill-builder/styles/emoji_key.md`
