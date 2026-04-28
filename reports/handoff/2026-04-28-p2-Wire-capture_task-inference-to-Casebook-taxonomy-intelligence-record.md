# Implementation Plan: Wire capture_task inference to Casebook taxonomy intelligence record

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

`capture_task` in `src/ben-cp.ts` uses a hardcoded keyword map. Replace with inference reading from `intelligence/casebook/taxonomy.md`. The `loadTaxonomy()` function already exists and parses the file — wire it into `inferProductArea()` properly.

## Format Convention
- `Product - Feature — Summary` / `Product — Summary` / `Feature — Summary`
- No orphan dashes. Omit label entirely if no match.

## Hardcoded overrides (always win)
- `audit, audit log, admin audit` → `Admin - Audit Log`
- `subscription, billing, plan, feature flag, feature gating, gating` → `Admin - Subscription`

## Products
portal, external portal, client portal → `Portal` | admin, administration, admin panel → `Admin` | api, endpoint, webhook, rest → `API` | auth, login, sso, saml, password, sign in → `Authentication` | cases, case, case record → `Cases` | home, homepage, home screen → `Home` | intake, referral, referrals → `Intake` | notification, notify, alert, email alert → `Notifications` | people, person, client, participant → `People` | report, reporting, reveal, redshift → `Reporting` | search, search bar, search results → `Search` | track, provider, parent org, organization → `Track`

## Features
account, account settings → `Account Management` | attachment, file upload, document, pdf → `Attachments` | communication, email sync, sms sync, nylas email → `Communication` | dashboard → `Dashboard` | import, data import, bulk upload, csv → `Data Import` | dynamic page, dynamic pages → `Dynamic Pages` | form, forms → `Forms` | history, activity, record history → `History` | integration, zapier, third party → `Integrations` | meeting, meetings, calendar, calendar sync, nylas calendar → `Meetings` | note, notes, case note, service note, autosave → `Notes` | relationship, relationships → `Relationships` | role, roles, permission, access, access control, restrict → `Roles` | enrollment, enrollments, enroll, service plan → `Service Plan` | service, services, service catalog → `Services` | setting, settings, configuration → `Settings` | staff → `Staff` | task, tasks, todo → `Tasks` | user, team, users and teams → `Users and Teams` | workflow, workflows → `Workflows` | workload, wlv, workload view → `Workload View`

## Verification
- [ ] `add_task("Notes autosave broken")` → label `Notes — ...`
- [ ] `add_task("SSO login loop")` → label `Authentication — ...`
- [ ] `add_task("bulk enrollment not saving")` → label `Service Plan — ...`
- [ ] `add_task("zapier webhook timeout")` → label `Integrations — ...`
- [ ] `npm run build` passes
