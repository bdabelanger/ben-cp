# Procedure: OKR Baseline & Target Establishment

> [!NOTE]
> ⚙️ **STATUS:** Active — v1.0 (2026-04-08)
> This runbook documents the manual steps for establishing Baselines and Targets
> for net-new Platform KRs in the Work Planning Register. Focused on first-pull /
> initialization, not ongoing monthly status updates.

---

## 🎯 Goal

Populate the `Baseline` and `Target` columns in the Work Planning Register for
any Platform KR currently showing `X%`, `Needs baseline`, `In progress`, or a
blank value, so that the status mapping logic in
`skill-builder/mappings/status_mapping.md` can be applied consistently going forward.

---

## 📋 Pre-Flight Checklist

Before starting any KR, confirm:
- [ ] The KR is marked `In? = Yes` or `Stretch` in the register
- [ ] The KR has a defined `Data Source` column value (if blank → see Step 0)
- [ ] You know the acquisition path (see Step 1)
- [ ] The feature the KR measures has shipped, or a proxy baseline approach has been agreed (see Blocker Reference below)

---

## 🗺️ Execution Steps

### Step 0: Triage the KR

**When:** KR has no `Data Source` listed, status is `Pending release`, or
feature is not yet shipped.

**Action:** Skip this KR for now. Log in the register Notes column:
> `Baseline deferred — [reason]. Revisit: [target date or milestone]`

**Decision point:** If `Pending release` but the feature has since shipped,
proceed to Step 1. If a proxy baseline approach has been agreed (see Appendix),
proceed to Step 2A or 2B using the proxy method noted there.

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
`skill-builder/mappings/status_mapping.md`:

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
| Feature not yet shipped | Use agreed proxy baseline (see Appendix) or defer with dated note |
| Metric stacks as new shortcuts/entry points ship | Note which shortcuts were live at time of baseline pull; revisit at each launch |

---

## 🔗 References

- Data source inventory: `okr-reporting/data_sources.md`
- Status logic: `skill-builder/mappings/status_mapping.md`
- Visual standards: `skill-builder/styles/emoji_key.md`

---

---

# Appendix: Q2 2026 Platform KR Baseline Reference

> [!NOTE]
> 📅 **SOURCE:** Migrated from *Q2 2026 - OKR Reference* (Google Doc, last updated 2026-04-02)
> This appendix documents the current baseline/target status and next steps for
> each active Q2 Platform KR. Update in place as work progresses — this replaces
> the Google Doc as the single source of truth.

---

## Elevate Notes to first-class experience

---

### KR: Notes WLV Adoption
> *X% of Tenants with at least one Note created within collection period have at
> least one user with usage in the Notes WLV*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Notes WLV not yet live. No usage data. |
| **Target** | 🟡 Proxy — Services WLV quarterly usage applied to # of beta tenants targeted |
| **Sources** | GA, ChurnZero (click / filter / sort / search events at tenant level post-launch) |

**Next steps:**
- [ ] Confirm analytics requirements — verify click/filter/sort/search actions in Notes WLV fire trackable events with tenant ID on launch
- [ ] Pull Services WLV baseline — use as directional target comp while Notes WLV data matures
- [ ] Set proxy baseline using Services WLV quarterly usage × beta tenant count
- [ ] Wait for launch before recording any real baseline (Beta 6/25, GA 7/27)

**Notes:** Services WLV is the closest internal comp. Beta/GA window is late Q2/Q3 — this KR is effectively a Q3 measurement.

---

### KR: Notes Quick Entry (Outside UOW)
> *X% of Users with at least one Note created within collection period have
> created a Note from a global entry point (outside UOW)*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Partial — GA tracks Note creation with UOW context today for shipped shortcuts |
| **Target** | 🟡 Estimated — directional target from current GA data; grows as more shortcuts ship |
| **Sources** | Google Analytics |

**Next steps:**
- [ ] **Pull current baseline from GA** — Note creation events filtered to non-UOW context, by tenant; establish current state with shipped shortcuts only
- [ ] Set a Q2 target focused on already-live entry points only
- [ ] Set a Q3 additive target once WLV-based shortcuts ship (Beta 7/13, GA 8/10)
- [ ] Track as additive metric — note baseline date and which shortcuts were live at time of pull
- [ ] Confirm event coverage for upcoming shortcuts — verify new entry points fire the same Note creation event with UOW context on launch

**Notes:** # of users is cleaner than % given rolling baseline as entry points expand. Worth dating each baseline snapshot with shortcut list.

---

### KR: Locked / Signed Notes (High-Confidentiality Tenants)
> *X% of high-confidentiality Tenants with at least one Note have created a
> locked or signed a note with Services data*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — Locked Notes adoption among high-confidentiality tenants (Signed Notes not yet live) |
| **Target** | TBD — # of high-confidentiality tenants in beta with at least one locked/signed Note |
| **Sources** | ChurnZero, SQL (via Data team) |

**Next steps:**
- [ ] Pull proxy baseline — compare non-service note locked note data with Note Type % to project potential usage
- [ ] Validate high-confidentiality tenant population — confirm this is a clean filterable segment in Reveal BI (denominator source: Margaux's sheet)
- [ ] Confirm instrumentation at build time — locked Service Note creation should be tied to tenant + confidentiality flag in DB
- [ ] Wait for Signed Notes launch before recording real baseline (Beta 7/27, GA 8/24)
- [ ] Beta target: # of high-confidentiality beta tenants with at least one locked/signed Note

**Notes:** Denominator requires joining with Margaux's high-confidentiality tenant list. All three fields (locked, signed, Services data) must be present — confirm this is trackable as a combined event.

---

### KR: Bulk Import for Notes (New Tenants)
> *X% of new Tenants (rolling 90 days) have imported Notes using bulk import*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Partially blocked — needs CX ops input on current migration volume as comp |
| **Target** | 🛑 Blocked — to be estimated once CX ops comp is available |
| **Sources** | CX ops data (Cierra), GA / ChurnZero for signals post-launch |

**Next steps:**
- [ ] Check with Cierra — confirm how many new tenants currently require paid onboarding migrations for Notes (this is the baseline comp)
- [ ] Check GA / ChurnZero for any existing signals
- [ ] Add instrumentation at build time — bulk import for Notes needs a job record tied to tenant + timestamp on completion (no current DB traceability)
- [ ] Move measurement window to Q3 — no Q2 GA exposure (GA 7/13)

**Notes:** Bulk import is live for other entities but not Notes. Target will be directionally set from CX ops migration data once Cierra confirms.

---

## Planning/delivering services at scale

---

### KR: Service Notes — Roster Association (Q1 carryover)
> *Increase % of Service Notes created that are associated with a Rostered Service Offering*

| | |
| :--- | :--- |
| **Baseline** | ✅ Unblocked — queryable in Reveal BI today |
| **Target** | ✅ Unblocked — pull baseline first to set meaningful target |
| **Sources** | Casebook Admin Reporting / Reveal BI |

**Next steps:**
- [ ] **Pull baseline in Reveal BI** — join `cbp_service_notes` + `cbp_services` on `service_id`, filter where `rostering = true` for numerator; all Service Notes for denominator. Filter disengaged tenants via `cbp_active_users` join on `tenant_id`
- [ ] Define window — monthly cadence, plus Q1 quarterly snapshot
- [ ] Set target once baseline is in hand

**Notes:** Disengaged tenant filter (`disengaged = false`) applied consistently via `cbp_active_users` joined on `tenant_id` — standard across all Reveal queries.

---

### KR: Notes Datagrid — Navigation Shortcuts
> *X% of Tenants who have ever used the Notes datagrid have at least one user
> who has used at least one new navigation shortcut in the Notes datagrid*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — beta usage exists today in GA/ChurnZero; directional |
| **Target** | 🟡 Estimated — beta cohort data available as early signal; GA 4/9 already live |
| **Sources** | GA, ChurnZero |

**Next steps:**
- [ ] **Pull beta baseline from GA / ChurnZero** — tenant-level sort / filter / search events on Notes datagrid; note beta cohort is not representative of full population
- [ ] Confirm event coverage — verify sort, filter, and search each fire distinct trackable events with tenant ID
- [ ] Confirm denominator is trackable — tenants who have opened the Notes datagrid at least once should be a separate event
- [ ] Reassess baseline at GA launch (GA 4/9) — replace beta baseline with full population baseline

**Notes:** Most actionable of the Notes analytics KRs — beta data available now. GA already live as of 4/9.

---

### KR: Service Plan Datagrid — Navigation Shortcuts
> *X% of Tenants who have ever used the Service Plan datagrid have at least one
> user who has used at least one new navigation shortcut in the Service Plan datagrid*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Service Plan datagrid still in development |
| **Target** | 🛑 Blocked — Notes datagrid beta data available as comp once Notes launches |
| **Sources** | TBD — GA / ChurnZero at launch |

**Next steps:**
- [ ] Wait for launch — feature must ship before any baseline is measurable (GA 5/28)
- [ ] Confirm analytics requirements at launch — sort / filter / search must fire distinct trackable events with tenant ID
- [ ] Use Notes datagrid beta cohort as comp — same interaction pattern, closest parallel
- [ ] Beta target: focus on beta cohort adoption; modest # given narrow window

**Notes:** Nearly identical instrumentation story to Notes datagrid but no beta data yet.

---

### KR: Service Notes — All Data Entry Shortcuts
> *X% of Tenants with at least one Service Note created within the measurement
> period have at least one user who has used at least one data entry shortcut
> for creating new Service Notes*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Service Notes shortcuts not yet fully live; some shipped |
| **Target** | 🟡 Estimated — comparable shortcuts may provide loose comp once identified |
| **Sources** | GA, ChurnZero (verify at launch) |

**Next steps:**
- [ ] Pull prod baseline — some shortcuts are already live; use current usage as starting baseline
- [ ] Confirm analytics requirements — verify shortcut interaction events fire with tenant ID in GA / ChurnZero at launch
- [ ] Identify comp — find closest existing shortcuts feature for directional target
- [ ] Q2 target: focus on adoption growth among tenants with at least one Service Note; all features live in GA except Service Groups (landing with Notes beta)

**Notes:** Broad KR covering multiple UX behaviors — define which specific shortcut interactions count at instrumentation time.

---

### KR: Enrollments — All Data Entry Shortcuts
> *X% of Tenants with at least one Enrollment created within the measurement
> period have at least one user who has used at least one data entry shortcut
> for creating new Enrollments*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — Enrollments shortcuts not yet fully live |
| **Target** | 🟡 Estimated — Service Notes shortcuts comp once identified; same feature pattern |
| **Sources** | Casebook Admin Reporting, GA / ChurnZero (verify at launch) |

**Next steps:**
- [ ] Pull prod baseline — some shortcuts already live; use current Casebook Admin Reporting data as starting point
- [ ] Confirm analytics requirements — verify shortcut interaction events fire with tenant ID at launch
- [ ] Use Service Notes shortcuts as comp — nearly identical feature pattern
- [ ] Q2 target: all features live in GA; focus on adoption growth among tenants with at least one Enrollment

**Notes:** Consider measuring Enrollments and Service Notes shortcuts together once both are launched — nearly identical instrumentation story.

---

## Reduce admin burden — Third-party data entry channels

---

### KR: Zapier — Custom Fields
> *# of entitled Tenants with at least one Incoming Integration have created/
> updated a record including at least one new field or line item via Zapier*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — explore Zapier Insights for comps |
| **Target** | 🛑 Blocked — no meaningful baseline / comps yet |
| **Sources** | Zapier Insights, Super Admin (API Access flag), SQL / machine clients |

**Next steps:**
- [ ] Explore with Engineering — may have a data source idea
- [ ] Check Zapier Insights dashboard — may provide richness data; note: won't provide tenant-identifying info so will be a blind ratio
- [ ] Entitled tenants from Super Admin — "API Access" flag in Super Admin tenants table (needs verification)
- [ ] Incoming Integrations — explore machine clients as proxy (needs verification)
- [ ] GA target: minimal Q2 exposure (GA 6/11); focus on achievable # of tenants

**Notes:** Metric instrumentation needs to measure data richness of Zapier interactions by tenant, filtered to entitled tenants only. Blind ratio from Zapier Insights is a weak signal — Engineering input needed for a stronger source.

---

### KR: Portal — Invitations Sent
> *# of entitled BETA Tenants have sent at least one portal invitation to a
> (non-Provider) Person*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — data model for new Portal work may change |
| **Target** | 🛑 Blocked |
| **Sources** | DB (`external_user_invitations` table, pending data model confirmation) |

**Next steps:**
- [ ] Resolve Portal data model first — determine if `external_user_invitations` table will be reused before building instrumentation
- [ ] No clear baseline comp — Access Provider Portal is not a valid comp
- [ ] Beta target: GA is Q3; beta-centric only in Q2 (Beta 6/11 + 6/25). Invitations likely landing in 6/11 beta release
- [ ] Metric instrumentation — measure invitations sent with user type attached, in DB or as GA custom event

**Notes:** Current `external_user_invitations` table has: `application_id`, `status`, `expiration`, `person_id`, `email`, `first/last name` — looks general, may be reusable. Unblocks with Portal data model decision.

---

### KR: Portal — Invitation Acceptance
> *# of entitled BETA Tenants that have sent at least one portal invitation also
> had a (non-Provider) Person log in to the Portal*

| | |
| :--- | :--- |
| **Baseline** | 🛑 Blocked — data model unstable; Access Provider Portal not a valid comp |
| **Target** | 🛑 Blocked |
| **Sources** | GA (`/portal` page view as proxy), DB session data (no primary source currently) |

**Next steps:**
- [ ] Resolve Portal data model (same blocker as Invitations)
- [ ] Proxy available: GA `/portal` page view — not a strict login event, not distinct (may show multiple per session), but directional. Consider for HEART metrics
- [ ] Beta target: same window as Invitations (Beta 6/11 + 6/25)
- [ ] Metric instrumentation — login events with user type + tenant ID, either in DB or GA custom event

**Notes:** All three Portal KRs share the same architectural blocker — they unblock together once data model is confirmed.

---

### KR: Portal — Person Profile Updates
> *# of entitled BETA Tenants have had at least one (non-Provider) Person
> update their profile via the Portal*

| | |
| :--- | :--- |
| **Baseline** | 🟡 Proxy — external Task completion in current data model is a directional comp |
| **Target** | 🛑 Blocked — non-Provider distinction unresolved |
| **Sources** | DB / GA (profile update event with user type + tenant ID) |

**Next steps:**
- [ ] Resolve Portal data model (same blocker as Invitations and Acceptance)
- [ ] Pull Task completion proxy — use external Task success rate as directional baseline while instrumentation is pending
- [ ] Beta target: new task type likely landing in 6/25 beta release
- [ ] Metric instrumentation — profile update action tracked as distinct event with user type and tenant ID

**Notes:** Shares exact same architectural blocker as Portal Invitations and Acceptance — all three unblock together.
