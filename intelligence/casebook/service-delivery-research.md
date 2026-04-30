# Service Delivery Research — Domain Patterns & Terminology

- **taxonomy:** Service Plan, Services
- **type:** intelligence

# Service Delivery Research — Domain Patterns & Terminology

> **Source:** Confluence — [Service Delivery Research](https://casecommons.atlassian.net/wiki/spaces/PROD/pages/652574739/Service+Delivery+Research)
> **Last updated in Confluence:** 2021-10-19
> **Status:** ✅ Domain patterns are stable and still applicable. State agency specifics may have evolved. Non-profit context noted as partially different from state agencies.

---

## Key Domain Patterns

### Services
Services are typically delivered by third-party providers on behalf of a state agency, which reimburses the provider. Broken down into types by activity (therapy, drug testing, counseling, transportation, in-home care, etc.).

Two atomic service delivery models:
1. Care recipient receives service type for an interval of time from a provider
2. Provider offers capacity of a service type utilized by care recipient for an interval of time

> **Child welfare exception:** "Services" in child welfare also includes agency-delivered services (investigation, foster placement, caseworker supervision, visitation management, adoptions) — distinct from the common third-party model.

### Placements
Generally refers to residential placement — someone placed somewhere to live. Stricter rules around provider capacity (licensed beds, space requirements).

> **Child welfare:** Placement has a very specific meaning — removing children from legal guardians and placing them in foster care, group homes, or residential facilities. A substantial sub-domain with dedicated workers, business rules, and outcome measures (number of placements in a removal, disruptions, reasons for change, final outcome: reunification, adoption, age-out, etc.).

### Service Plans
Documented plans for multiple services to improve a person's or family's circumstances. Generally loose and unstructured. Cover:
- Outcomes to achieve (to close the involvement)
- Goals to target
- Risks and needs to overcome
- Progress narratives
- Potential next steps / step up or step down

> **Child welfare:** Versioning of service/case plans is commonly requested — each formal revision becomes a new version, still associated with prior ones.

### Outcomes
Two broad categories:
- **Positive outcomes to achieve:** Measurable improvement in life circumstances (independence, grades, meeting obligations)
- **Negative outcomes to avoid:** Recidivism, failed drug tests, placement disruptions, missed appointments, reported abuse

Two measurement types:
- **Explicit:** Measured directly via a dedicated data point (school scores, decision fields, assessment data) — easier to measure, easier to misuse
- **Implicit/derived:** Derived from other data (case durations, event dates, reasons for closure) — more insight, more complex reporting

> **Field insight:** Front-line practitioners often unclear on performance measures. Supervisors/administrators want better measures but struggle with existing systems. Most outcome measures tied to regulatory compliance or avoiding negatives — inflexible to evolving needs.

### Group Services
Less standardized than individual services. Invoicing typically still done per person. Some states require providers to enter service delivery detail individually (like an HR hours tracking system), which can distinguish group vs. individual delivery.

### Rosters & Capacity
Provider capacity defined by:
- **License** — most common for foster families (max children based on home assessment) and residential facilities
- **Contract** — most common for professional providers (max billable hours due to budget limits, staff ratios, or class size limits)
- **Arbitrary / no limit**

Capacity must be measured by a service's unit of delivery — a provider may offer services with different units that can't be easily combined into one total capacity measure.

### Invoicing / Units of Service
Services reimbursed by government funds in standardized units:
1. **Time interval** — one day/night/week/month (residential services)
2. **Individual sessions/events** — single instance on a specific date

Basic billing formula: `# of people × (time interval / unit of delivery) × rate = $$$`

> **Common pain point (quoted directly):** *"I can't even tell what I'm being billed for and what I'm getting for that money, let alone whether the quality of the service is worth the cost."*

---

## Common Terminology

| Term | Definition |
|---|---|
| Care recipient / client / patient | The person receiving services. "Client" most common in human services state agencies and CBOs. "Patient" common in clinical contexts. |
| Provider / service provider / resource | Non-government entity delivering services to clients on behalf of government. Can be for-profit, non-profit, CBO. |
| Community-based organization (CBO) | Non-profit working at a local level to deliver services. May be pre-existing organizations (clubs, churches, schools) that have branched out, or purpose-built. |
| Service / activity | Type of service provided. "Activity" sometimes used for a sub-class of service (specific activity in a session). |
| Program | A set of services/practices administered by government to provide social services. Can comprise bundled services eligible for funding reimbursement. May be tied to dedicated funding streams with eligibility criteria. |
| Case plan / service plan / support plan / care plan | Documented result of case manager + care recipient working together on goals, steps, and services needed. May require formal signature. Multiple template types depending on human service domain. |
| Evidence-based practice (EBP) | Activity whose efficacy is verified empirically by independent clearinghouses. Some funding streams reserved only for EBPs. |
| "No wrong door" | ACA policy that channels people to any needed health/human service regardless of first point of contact. Envisions a single application for all services. |

---

## Relevance to Roadmap Themes

- **Theme 2 (Flexible Service Models & Tracking Outcomes):** The entire domain pattern section directly maps to Casebook's services model — enrollments, rosters, cohorts, outcomes, service plans, invoicing/units of service
- **Theme 5 (Amazing Analytics):** The outcomes section explains why reporting is hard — explicit vs. implicit measures, regulatory compliance vs. true outcome measurement, lack of standardization
- **Theme 6 (Automating & Optimizing Work):** The invoicing pain point and referral tracking complexity point directly to manual burden areas where automation adds value
- **Theme 3 (Workflows):** Referral sub-processes (provider acceptance/rejection tracking), plan versioning approvals, and warm hand-offs are all workflow problems

---

## Open Questions (From Original Research — Still Relevant)

- How much of outcome measurement can reside in Reporting vs. needing to be calculated in APIs?
- How to model capacity for mixed-unit providers (beds + classroom) in a single dashboard view?
- Who actually enters service delivery data, and when in their process?
- How much can be automated or derived rather than requiring manual entry?

