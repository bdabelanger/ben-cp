# Procedure: OKR Notes Quick Entry (Outside UOW) Baseline & Target Establishment

> [!NOTE]
> ⚙️ **STATUS:** In Progress - Awaiting full event discovery.
> This runbook documents the manual steps to establish Baselines and Targets for KRs measuring note creation from global entry points, outside of a specific User Workflow (UOW).

---

## 🎯 Goal

To quantify the percentage of tenants who create notes via high-level, non-workflow navigation paths (e.g., Dashboard, Global Lists) compared to the total number of active tenants.

---

## 📋 Pre-Flight Checklist

Before starting, confirm:
- [ ] The KR is marked `In? = Yes` or `Stretch` in the register.
- [ ] You know which acquisition path applies (Self-serve GA pull).

---

## 🗺️ Execution Steps: Measurement Definition

This procedure defines the measurement logic for this specific KR, leveraging Google Analytics event data.

### Step 1: Define the Denominator (Total Active Tenants)

The denominator represents the total population we are measuring against. 

**Metric:** Unique tenants from the defined cohort list below who have at least one note successfully created.
**Cohort Size:** TBD.
**GA Event:** `noteSubmit`
**Rationale:** This event fires upon successful saving for tenants within this specific, defined beta cohort.

### Step 2: Define the Numerator (Global Entry Point Usage)

The numerator counts unique tenants who initiated a note creation from a global/non-UOW context.

**Measurement:** Count of unique `tenant_id` associated with the following events:

*   ✅ **Confirmed Events (High Confidence):**
    *   `dashboardAddNoteOpen`: Note opened directly from the main Dashboard view (Non-UOW).
    *   `EngageWLVAddNote`: Note added via the Engage WLV list view (Non-UOW).
    *   `TrackServiceNoteNew`: Service note creation event (Requires validation for UOW context).

*   🟡 **Candidate Events (Needs Verification):**
    *   `gtm.click` events: Any GTM click that occurs on a global entry point must be manually verified to ensure it corresponds to note creation, as this signal is too broad.

**Decision Point:** If you discover other events during app exploration that clearly indicate a global entry point, add them here.

### Step 3: Calculate Baseline & Target

1.  **Pull Data:** Export GA data for the relevant period and filter by the events listed above (Numerator) and `noteSubmit` (Denominator).
2.  **Calculate Progress:** $	ext{Progress} = rac{	ext{Unique Tenants with Numerator Events}}{	ext{Unique Tenants with } noteSubmit}
3.  **Set Target:** Review KR text for target percentage or growth goal. If undefined, propose a target based on business goals and flag it for stakeholder sign-off.

---

## ⚠️ Instrumentation Gap & Next Steps (CRITICAL)

**The current measurement is incomplete.** The KR definition requires capturing *all* global entry points.

**Action Required:** Continue exploring the application using developer tools to identify any other event names that fire when a note is created from a non-UOW context. If you find new events, please provide them so we can update this SOP and begin baseline pulls.

---

## 🔗 References
- General Procedure: `okr-reporting/procedure.md`
- Status Logic: `skill-builder/mappings/status_mapping.md`