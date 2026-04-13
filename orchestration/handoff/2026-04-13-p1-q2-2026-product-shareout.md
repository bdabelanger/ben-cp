# Implementation Plan: Q2 2026 Product Shareout — Full Slide Intelligence

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Gemma
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P1
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

**Source:** Q2 2026 Product Shareout.pdf (43 slides), ingested 2026-04-12
**Status:** Ben is actively working on this deck. Several slides have internal commentary/red annotations indicating slides still need work — flagged below.

---

## Strategy Context

Three changes from the January plan:
1. **Start client portal sooner** — bigger impact on revenue & retention in 2026
2. **Boost foundation for dynamic pages + enhance notes UX**
3. **Make room for surge in service outcome tracking demand**

The deck covers 6 OKR themes + Indiana + Technology/Platform:

---

## OKR Themes & Q2 Slide Breakdown

### OKR 1 — Strengthen Core Case Management
*"Becoming a first-class service delivery planning and note-tracking system"*

**Q1 delivered (slides 7–9):**
- Faster Notes Nav + Authoring UX (bulk note entry, start/end dates on datagrid, narrative preview, sort/filter)
- Cascaded status updates (closure cascades from Case/Intake to all open work; real-time impact preview; "Skip" for standalone tasks)
- Expanded workflow triggers: involvement type, person role, label

**Q2 slides (pp. 15–17):**
- **Slide 16 — Restyled & enhanced notes authoring experience** ⚠️ NEEDS WORK: Internal note says "this is a copy/paste of the old notes slide — remove references to notes table and focus on authoring. Consider a <1 min video showing: adding services/people, tabbed design, shortcuts for loading, Service Groups in notes, people + attended=yes auto-completer, note vs. service date handling"
- **Slide 17 — Bulk tools for service plans (Sort/filter/bulk actions from Service Plan or Services WLV)** ⚠️ NEEDS WORK: Internal note says "play with slide, cover: New Service Plan UX, New Enrollments UX, Bulk Actions on both; most interested in bulk ending enrollments — needs screenshots of each"

**Relevant CBP Q2 roadmap items:** Notes - New authoring UX, Service Plan - New datagrid, Service Plan - New service enrollment datagrid, Services - Bulk end enrollment

---

### OKR 2 — Simplify Reporting
*"Deliver more out-of-the-box reporting experiences and more consistent data behavior"*

**Q1 delivered (slides 12–13):**
- Bringing permissions to reporting (access lists, allow/deny, consistent with Engage/Intake/People)
- Polish: Dynamic Workload View headers, direct linking from reports to UoWs, VPAT/accessibility gaps addressed

**Q2 slides (pp. 18–21):**
- **Slide 19 — Reporting packages: Understand Work and Workflow Performance** ⚠️ NEEDS WORK: Customer quote placeholder still says "A customer said this." — needs a real quote
- **Slide 20 — Reporting packages: Understand Service Delivery and Outcomes** — content looks solid (Lighthouse for the Blind of Fort Worth quote included)
- **Slide 21 — A new dose of Reporting features (Embedded analytics leveled up)** — conditional formatting, high-performance Redis caching, better dashboards/filters/integrations

**Relevant CBP Q2 roadmap items:** Reporting - Tasks/Work package, Services - Outcomes Tracking v1

---

### OKR 3 — Security & Compliance Enablers
*"Enable HIPAA and CJIS-minded customers to operate compliantly"*

**Q1 delivered:** UoW linking in reporting, Bring permissions to reports (also counted under Reporting)

**Q2 slides (pp. 22–24):**
- **Slide 23 — Audit Log: Follow the Work or Follow the User** — filter audit logs by user OR record; cross-platform visibility. Good quote from "The Albertas". Content looks solid.
- **Slide 24 — Sign and lock notes for better compliance mgmt** ⚠️ NEEDS WORK: Internal note asks "Okay to focus on both service note locking and signing, but perhaps we guarantee at least service note locking to beta in June?" — scope decision still open. Capabilities listed: Sign a note to lock it, remove signature to reopen, lock sensitive service notes.

**Relevant CBP Q2 roadmap items:** Audit Log - Follow the person, Notes - Signing/Service Note Lock v1

---

### OKR 4 — Ease Navigation Burdens
*"Reduce navigation complexity and offer more options to reduce redundant data entry"*

**Q2 slides (pp. 25–27):**
- **Slide 26 — Bulk import for notes + import usability updates** ⚠️ NEEDS WORK: Internal note says "update this slide to focus on what we're delivering — bulk import for notes and returning all error messages at once." Import General Notes with historical data; flatten tabs for easier import.
- **Slide 27 — Interact with [all] UoWs (Global Notes WLV)** ⚠️ NEEDS WORK: Internal note says "Focus this slide on the global WLV we're focused on in Q2." View/sort/filter content outside of individual units of work. Quote from Wellmet Project.
- **Slide 28 — Collect more data directly from people via Client Portal** ⚠️ NEEDS WORK: Internal note says "Focus this slide on the v1 scope of client portal." New portal with profiles, forms, eventually tasks; collaborate with people to populate tasks. Quote from Sparta, WI Police Department.

**Relevant CBP Q2 roadmap items:** Client Portal v1, Data import - Bulk import for Notes, Notes - Global Notes WLV v1, SMS - routing improvements

---

### OKR 5 — Enhance Core Configurability
*"Expand the ways Casebook can be personalized to best suit a customer's needs"*

**Q2 slides (pp. 29–31):**
- **Slide 30 — More no-code improvements for Zapier integrations** ⚠️ NEEDS WORK: Internal note says "Focus this slide on what we think we'll deliver in Q2." New triggers (e.g., "Service enrollment created in Casebook"), 4 new write actions (Create a Note, etc.), 5 new lookup actions (Search Cases, etc.), enhance 3 existing write actions with custom fields + line items for Case, Intake Report, Person. Quote from North Cook ISD.
- **Slide 31 — Configurable Relationship Types** — solid. 26 customers, $262k ARR callout. Quote from Western CT Area Agency on Aging.

**Relevant CBP Q2 roadmap items:** People - Config relationship type, Zap - custom fields -> intake/people, Granular Permissions - Services

---

### OKR 6 — Enhance Workflow Engine
*"More triggers, better assignment flexibility and a more refined user experience in workflow"*

**Q2 slides (pp. 32–35):**
- **Slide 33 — Stop jumping between Tasks and Workflows (Collapse Tasks/workflows UX)** — all tasks in one place (workflow + standalone), datagrid for tasks section. Quote from A Child's Place. Content looks solid.
- **Slide 34 — Workflows that reach beyond your team (External people in workflows)** ⚠️ NEEDS WORK: Customer quote placeholder still says "A customer said this." — needs a real quote. Capabilities: assign to case persons (Engage, Intake persons, Provider staff), assign to one/multiple/all relevant people, optional auto-send notifications.
- **Slide 35 — No more missed approvals (Overhauled workflow approvals)** — sequential reviewers, assign by team/role/supervisor of primary assignee, approvals surfaced in Home dashboard + in-app + email. Quote from CAP Canada. Content looks solid.

**Relevant CBP Q2 roadmap items:** Tasks - Workflows + ad-hoc tasks together, Workflows - Approval Improvements, Workflows - Assign WF Tasks to External Users

---

### AI (Q1 Highlight)
**Slides 10–11 — AI-Powered Case Summaries (Alpha)**
- Caseload Summaries for supervisor workload insight
- Case Handoff Briefs for faster transitions
- Enable via Incoming Integrations in Admin; read-only, role-based access
- Launch with small set of engaged customers; alpha learnings shape beta direction
- Linked to Claude Demo 4/3 video

**Relevant CBP Q2 roadmap items:** AI - Facesheet (Q2)

---

### Technology / Platform (Q2+)
**Slide 37 — Consolidating to a Unified API Foundation**
- Replacing Java CRNK layer + Apollo wrapper with Spring Boot GQL
- Reduces platform risk, improves reliability/performance, enables faster scalable development

**CBP TechMod Q2:** CRNK Replacement, Dynamic pages stabilization
**CBP BAU Q2:** Reporting Performance, Reveal Upgrade, Dynamic Pages - stabilize

---

### Indiana (Marquis Customer)
**Slides 38–40 — 2026 Indiana Roadmap**
- **Q2:** Upgrade application server software, upgrade search version/software, Release Rails 3.2, Replace ElasticSearch → OpenSearch 2.3

---

## Slides That Still Need Work — Summary

| Slide | Feature | What's Missing |
|-------|---------|---------------|
| 16 | Notes Authoring UX | Rewrite copy to focus on authoring (not table); consider demo video |
| 17 | Bulk Service Plan Tools | Add screenshots of new Service Plan UX, Enrollments UX, Bulk Actions |
| 19 | Workforce Reporting Package | Real customer quote needed |
| 24 | Sign & Lock Notes | Scope decision: confirm whether to cover both signing + locking or just locking to beta in June |
| 26 | Bulk Import for Notes | Refocus on bulk notes import + returning all errors at once |
| 27 | Global Notes WLV | Refocus on Q2 Global WLV scope specifically |
| 28 | Client Portal | Refocus on v1 scope only |
| 30 | Zapier Improvements | Refocus on confirmed Q2 deliverables (specific new triggers/actions) |
| 34 | External People in Workflows | Real customer quote needed |

---

## Full Q2 CBP Roadmap (Initiatives)

From slide 41:
- AI - Facesheet
- Audit Log - Follow the person
- **Client Portal v1** (highlighted)
- Data import - Bulk import for Notes
- Granular Permissions - Services
- Notes - Global Notes WLV v1
- Notes - New authoring UX
- Notes - Signing/Service Note Lock v1
- People - Config relationship type
- Reporting - Tasks/Work package
- Service Plan - New datagrid
- Service Plan - New service enrollment datagrid
- Services - Bulk end enrollment
- **Services - Outcomes Tracking v1** (highlighted)
- **SMS - routing improvements** (highlighted)
- Tasks - Workflows + ad-hoc tasks, together
- Workflows - Approval Improvements
- Workflows - Assign WF Tasks to External Users
- Zap - custom fields -> intake/people
