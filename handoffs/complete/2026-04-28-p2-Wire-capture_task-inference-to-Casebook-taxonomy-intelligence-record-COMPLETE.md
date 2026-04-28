# Implementation Plan: Wire capture_task inference to Casebook taxonomy intelligence record

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

The capture_task tool is now dynamically powered by the Casebook taxonomy intelligence record. Hardcoded maps have been removed in favor of a runtime-parsed regex engine that adheres to the established Product-Feature naming conventions.

---

## Context

The `capture_task` MCP tool in `src/ben-cp.ts` currently uses a hardcoded keyword map to infer a `Product - Feature` label for Jira issue summaries. The authoritative taxonomy has now been defined and validated by Ben as an intelligence record.

**Taxonomy location:** `intelligence/casebook/taxonomy.md`

---

## Task

Replace the hardcoded keyword inference map in `capture_task` with logic that reads from (or is compiled from) `intelligence/casebook/taxonomy.md`.

---

## Label Format Convention

- `Product - Feature — Summary` (e.g. `Cases - Notes — Autosave not triggering`)
- `Product — Summary` — when only product is known
- `Feature — Summary` — when only feature is known
- No orphan dashes — never output `- Feature — Summary`
- Comma-separate multiple areas: `Cases - Notes, Attachments — Summary`
- Omit label entirely if nothing matches — do not guess

---

## Hardcoded labels (always use these regardless of context)

These two are always unambiguous — wire them as constants:

| Match | Label |
|---|---|
| `audit, audit log, admin audit` | `Admin - Audit Log` |
| `subscription, billing, plan, feature flag, feature gating, gating` | `Admin - Subscription` |

---

## Keyword → Label Map

Derived from `intelligence/casebook/taxonomy.md`. Implement as a lookup table or equivalent.

### Products
| Keywords | Label |
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

### Features (combine with product context when available)
| Keywords | Feature |
|---|---|
| account, account settings | `Account Management` |
| attachment, file upload, document, pdf | `Attachments` |
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
| service, services | `Services` |
| setting, settings, configuration | `Settings` |
| staff | `Staff` |
| task, tasks, todo | `Tasks` |
| user, team, users and teams | `Users and Teams` |
| workflow, workflows | `Workflows` |
| workload, wlv, workload view | `Workload View` |

---

## Expected Behavior

- Match product and feature independently from capture text
- If both matched: `Product - Feature — Summary`
- If product only: `Product — Summary`
- If feature only: `Feature — Summary`
- If neither: omit label, proceed with summary only
- Hardcoded pairs (`Admin - Audit Log`, `Admin - Subscription`) take precedence
