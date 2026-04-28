# Casebook Product-Feature Taxonomy

> **Status:** Authoritative  
> **Confirmed by:** Ben Belanger (2026-04-27)  
> **Used by:** `capture_task` MCP tool (Jira label inference); intelligence domain authors (Casebook domain, Product Roadmap) when mapping content to product/feature concepts; any tool or agent reasoning about Casebook's product surface

---

## Format Convention

- **Hyphenate** product and feature: `Cases - Notes`
- **Comma-separate** multiple areas (no "and"): `Cases - Notes, Attachments`
- **Em-dash** before the summary: `Cases - Notes — Date field not saving`
- **No brackets** around the product area
- **Partial match — feature only known:** drop the product side entirely → `Notes — Summary`
- **Partial match — product only known:** drop the feature side entirely → `Cases — Summary`
- Never write an orphan dash like `- Notes — Summary` or `Cases - — Summary`

---

## Products

| Product | Notes |
|---|---|
| Portal | Branded portal application for external users |
| Admin | |
| API | |
| Authentication | |
| Cases | Also known as Engage |
| Home | |
| Intake | |
| Notifications | |
| People | Top-level product; also exists as a feature within other products |
| Reporting | |
| Search | |
| Track | Covers Parent Organizations and Providers |

---

## Features

Features may appear under one or more products. When labeling, combine as `Product - Feature`.

| Feature | Notes |
|---|---|
| Account Management | |
| Attachments | Covers file uploads, documents, and PDFs |
| Audit Log | Admin-level audit log; distinct from History |
| Communication | Primarily email and SMS syncing via Nylas; users can also create records directly in Casebook |
| Dashboard | |
| Data Import | |
| Dynamic Pages | |
| Forms | |
| History | Activity-oriented record history (e.g. changes, events on a record); not the Admin audit log |
| Integrations | Third-party integrations (e.g. Zapier); excludes Nylas (see Communication, Meetings) |
| Meetings | Primarily calendar syncing via Nylas; users can also create meeting records directly in Casebook |
| Notes | Service notes and interactions tier; common in Cases, also cross-cutting |
| People | Also a top-level product |
| Relationships | |
| Roles | Covers permissions, role assignment, and access control |
| Service Plan | Enrollments tier of Services — managing enrollment of people into service offerings |
| Services | Offerings tier — the service catalog, what services exist and their configuration |
| Settings | |
| Staff | |
| Subscription | Feature gating and plan management; lives under Admin |
| Tasks | |
| Users and Teams | Covers user management and team structure |
| Workflows | |
| Workload View | Cross-product feature; exists in Cases, Intake, People, Track, and more |

### Services tier clarification

The Services area has three distinct feature components:

| Feature | Tier | Covers |
|---|---|---|
| Services | Offerings | The service catalog — what services exist, their configuration |
| Service Plan | Enrollments | Enrolling people into services, bulk enrollment, enrollment dialogs |
| Notes | Interactions | Service notes, case notes, interaction records |

"Enrollments" and "enrollment" as terms map to `Service Plan` in all labeling contexts.

---

## Keyword Inference Map

Used by `capture_task` to infer `Product - Feature` from free-text capture.  
Feature-only rows produce a label without a product prefix (e.g. `Notes — Summary`).  
When context makes the product clear, combine: `Cases - Notes — Summary`.

| Signal keywords | Inferred label |
|---|---|
| portal, external portal, client portal | `Portal` |
| admin, administration, admin panel | `Admin` |
| api, endpoint, webhook, rest | `API` |
| auth, login, sso, saml, password, sign in | `Authentication` |
| cases, case, case record | `Cases` |
| home, homepage, home screen | `Home` |
| intake, referral, referrals | `Intake` |
| notification, notify, alert, email alert | `Notifications` |
| people, person, client, participant | `People` |
| report, reporting, reveal, redshift, dashboard export | `Reporting` |
| search, search bar, search results | `Search` |
| track, provider, parent org, organization | `Track` |
| account, account settings | `Account Management` |
| attachment, file upload, document, pdf | `Attachments` |
| audit, audit log, admin audit | `Admin - Audit Log` |
| communication, email sync, sms sync, text sync, message sync, nylas email | `Communication` |
| dashboard | `Dashboard` |
| import, data import, bulk upload, csv | `Data Import` |
| dynamic page, dynamic pages | `Dynamic Pages` |
| form, forms | `Forms` |
| history, activity, record history, activity log | `History` |
| integration, zapier, third party | `Integrations` |
| meeting, meetings, calendar, calendar sync, appointment, nylas calendar | `Meetings` |
| note, notes, case note, service note, autosave | `Notes` |
| relationship, relationships | `Relationships` |
| role, roles, role assignment, permission, permissions, access, access control, restrict | `Roles` |
| enrollment, enrollments, enroll, service plan, service enrollment | `Service Plan` |
| service, services, service catalog, offering | `Services` |
| setting, settings, configuration | `Settings` |
| staff | `Staff` |
| subscription, billing, plan, feature flag, feature gating, gating | `Admin - Subscription` |
| task, tasks, todo | `Tasks` |
| user, team, users and teams | `Users and Teams` |
| workflow, workflows | `Workflows` |
| workload, wlv, workload view | `Workload View` |
| *(no match)* | *(omit label; do not guess)* |

---

## Example Labels

```
Cases - Notes — Autosave not triggering on tab close
Cases - Workload View — Cases not loading for assigned staff
Cases - Service Plan — Bulk enrollment dialog not saving
Cases - Services — Service catalog not loading for tenant
Intake - Workload View — Referrals not appearing in workload
Track - Workload View — Provider list not reflecting filters
Track - Workflows — Provider status not updating after transition
Authentication — SSO login loop on Safari
Reporting — Chart missing data for date range filter
Intake - Forms — Required field not blocking submission
Notes — Date field behavior inconsistent across products
Cases — Unexpected error on case record load
Portal — External portal not loading for client users
Roles — Permission not applying after role reassignment
Users and Teams — User unable to be restricted to specific team
Admin - Subscription — Feature flag not applying after plan change
Admin - Audit Log — Admin audit log not capturing role changes
Communication — Email sync not pulling in latest messages (Nylas)
Meetings — Calendar sync missing recurring events (Nylas)
History — Activity log not showing latest case updates
Attachments — PDF not rendering in file preview
Service Plan — Enrollment not persisting after bulk action
```
