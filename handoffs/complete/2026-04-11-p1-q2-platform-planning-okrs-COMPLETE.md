---
title: Implementation Plan q2-platform-planning-okrs
type: handoff
domain: handoffs/complete
---

# Implementation Plan: q2-platform-planning-okrs

> **Prepared by:** Claude via Cowork/Dispatch (2026-04-11)
> **Target date:** 2026-04-12
> **Assignee:** Claude (Cowork) / human user
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1 — recurring weekly input required from human user before Claude can act
> **v1.5**
> **STATUS**: ✅ COMPLETE

Pushed 11 of 12 queued Asana date corrections from the Q2 planning session. All date fields fixed (Asana API requires `{"date": "..."}` format, not plain strings) and GA Month set via enum GID. Notes - Tabbed design (GID 1213002343224284) returned 404 and was confirmed by Ben as no longer existing — its scope was absorbed into Bulk Service Notes. OKR writing (Task 2) and AGENTS.md Dispatch entry (Task 4) remain for a future session.

**Changelog:** (see root changelog.md)


---

### Antigravity's Session Summary (2026-04-12)
- ✅ **AGENTS.md**: Documented the "Dispatch" proxy agent and behavioral protocols (Task 4 complete).
- ✅ **Asana Preparation**: Mapped 100% of the 17 date corrections to their Project/Field GIDs. Created [asana_push_corrections.py](file:///Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/tools/status-reports/scripts/asana_push_corrections.py) to handle the update.
- ⚠️ **Asana Push Blocked**: Attempted push failed due to network isolation in the current environment. 
- **Next for Claude**: Execute the Asana push script from a network-enabled environment and begin the OKR rationale/mapping (Task 1 & 2).

---

## Context

The user completed a full Q2 quarterly planning session on 2026-04-11 via Cowork/Dispatch (mobile). The session produced a finalized biweekly release calendar, dev allocation analysis, QA/UAT date derivations, risk flags, and a staffing observations doc. Two immediate work items remain: (1) OKR writing for a manager meeting tomorrow, and (2) pushing 17 Asana date corrections once approved.

A third meta-task is also captured here: the concept of **Dispatch as a proxy messenger agent** needs to be formally added to `AGENTS.md` at the vault root. This should be treated as a separate sub-task within this handoff, not the primary focus.

> **Note on scope:** This handoff is large and covers three distinct areas — OKR writing, Asana corrections, and AGENTS.md update. If it grows further, consider splitting into separate handoff files per task. For now they are grouped because they share a common session origin and human user wants a single pickup point.

---

## Execution Order

1. **Load vault context** — Read `AGENTS.md` at vault root and `okr-reporting/q2-2026/index.md`
2. **OKR writing session** — Collaborate with human user on Q2 OKR targets (see Task 2)
3. **Asana corrections** — Push 17 date corrections after human user's explicit approval (see Task 3)
4. **AGENTS.md update** — Add Dispatch agent definition (see Task 4)
5. **Changelog + completion** — Write changelog entries and mark complete

---

## Task 1: Load Context

Before starting, read:
- `AGENTS.md` — vault root, understand current agent roster and conventions
- `okr-reporting/q2-2026/index.md` — understand what OKR structure already exists for Q2
- `okr-reporting/q2-2026/planning-services-at-scale/index.md` and `okr-reporting/q2-2026/elevate-notes/index.md` — existing KR files that may already have baselines or targets relevant to this session

This is essential before the OKR session — the vault already has Q2 OKR structure in place.

---

## Task 2: OKR Writing Session

The user's OKR format is approved by his manager. He has a meeting on 2026-04-12 and wants a draft.

**human user's role:** He sets baselines from his own metrics access.
**Claude's role:** Propose realistic targets grounded in the Q2 delivery schedule below.

**How to start:**
1. Ask human user to share his approved OKR format template (or confirm it matches what's already in `okr-reporting/q2-2026/`)
2. Ask which themes he wants to prioritize for the manager meeting
3. Propose targets one OKR at a time with 2–3 sentences of rationale tied to specific GA dates
4. The user validates and adjusts

**Suggested themes** (confirm with human user):
- Notes suite delivery and adoption (5/14 + 5/28 GA bundle, 4 projects)
- Service Plan enhancements (datagrid + bulk services, 5/28 GA)
- Zapier integration delivery (6/11 GA, contractor risk)
- Portal launch readiness (Beta Jun, GA Aug)
- Engineering delivery reliability (biweekly cadence, P1 resolution)

---

## Task 3: Asana Date Corrections

17 corrections are queued from the planning session. **Do NOT push until human user explicitly approves.** Confirm with him first, then push all at once.

| Project | Field | Old value | New value |
|---|---|---|---|
| Notes - Bulk General Notes | GA Date | — | 5/14 |
| Notes - Bulk General Notes | Beta Start | — | 4/23 |
| Notes - Locked Notes | GA Date | — | 5/14 |
| Notes - Locked Notes | Beta Start | — | 4/28 |
| Notes - Tabbed design | GA Date | — | 5/14 |
| Notes - Tabbed design | Beta Start | — | 4/23 |
| Notes - Bulk Service Notes | GA Date | — | 5/28 |
| Notes - Bulk Service Notes | Beta Start | — | 4/28 |
| Service plan datagrid | GA Month | June | May |
| Service plan datagrid | GA Date | — | 5/28 |
| Services WLV - Bulk actions | GA Date | — | 5/28 |
| Zapier improvements | GA Date | — | 6/11 |
| VPAT audit | GA Date | — | 6/11 |
| Notes - Global Notes WLV | GA Date | — | 7/9 |
| Schema migration | GA Date | — | 7/23 |
| Notes - Signing | GA Date | — | 7/23 |
| Portal Client Dashboard | Beta Dates | — | 6/11 and 6/25 |

---

## Task 4: AGENTS.md — Add Dispatch

Add a new agent entry to `AGENTS.md` for **Dispatch**. This is not a vault agent like Strategic PM or Changelog Auditor — it is an external relay agent (Claude running on mobile via the Dispatch tab in the Claude app). It needs to be documented so all vault agents and desktop Claude understand how to interpret and respond to messages from it.

**What to add to AGENTS.md:**

Dispatch is Claude running on mobile (iOS/Android) in the Dispatch tab of the Claude app. It acts as a proxy messenger — relaying human user's instructions from mobile into active desktop Cowork sessions or Claude Code sessions. It is not a vault agent and does not read or write vault files directly.

Key behavioral rules for all agents when receiving a Dispatch message:

- Treat it with the same authority as a direct message from human user
- Expect brevity — messages are typed on mobile, often short or casual
- Apply Dispatch messages as mid-task corrections or additions, not new tasks requiring a restart
- Keep responses that will be relayed back via Dispatch concise and mobile-friendly
- Flag anything that requires desktop tools to proceed, but proceed with what's possible

When Dispatch introduces itself in a fresh session or task, it should identify as a proxy: "Message from human user via Dispatch: [message]" or "human user is on mobile via Dispatch — [context]. Here's what he'd like: [message]"

The user-cp is not currently connected on mobile. Dispatch cannot read vault files or run skills directly. Until that changes, Dispatch relies on handoff files and session context to carry continuity between mobile and desktop sessions.

---

## Reference: Q2 Release Plan

| Window | Type | Projects |
|--------|------|----------|
| 4/9 | GA | Clearer errors (Tuan), MUI upgrade (Sodiq), KPP (Tuan) |
| 4/23 | Beta | Notes bundle: Bulk General, Locked Notes, Tabbed design, Bulk Service Notes |
| 5/14 | GA | Notes bundle — Bulk General, Locked Notes, Tabbed design |
| 5/28 | GA | Bulk Service Notes · Service plan datagrid · Bulk Services section · Services WLV bulk actions |
| 6/11 | GA + Beta | VPAT audit · Zapier · Portal Beta #1 |
| 6/25 | Beta | Portal Beta #2 |
| 7/9 | GA | Notes Global WLV |
| 7/23 | GA | Schema migration (Bisoye + Feyi from Data team) · Notes Signing |
| 8/6–8/20 | GA | Portal Client Dashboard (TBD pending scoping) |

Fix version convention: Platform-YYYY-M-N (e.g. Platform-2026-5-2 = 5/28)
Feature flags: 1:1 with projects except BAU. Bulk Service Notes feature-flagged — can extend Beta.

---

## Reference: Key Risks

1. **Zapier** — Contractor Eric has not committed code as of 4/10. Demo 4/17. Watch before locking 6/11.
2. **Portal scoping** — Must close this week for Duc dev start 4/14 (GA target 8/6). 40d estimate is pre-scoping.
3. **Service plan datagrid** — Stories need triage before sprint end 4/11 for QA start 5/4. Blessing picks up 4/9.
4. **Schema migration** — Requires Feyi (Data team) as second dev. The user to loop in Feyi and PM before dev start 6/1.
5. **KPP** — human user to find Jira ticket. QA wrapped, UAT 4/4, GA 4/9. No risk.
6. **Bulk Service Notes P1** (CBP-3075) — Must clear before Beta. Feature-flagged, flexible Beta duration.

---

## Reference: Dev Allocation

- **Bisoye** — Notes suite + Global WLV + Schema migration. Heavy through 7/9, free Q3.
- **Blessing** — Datagrid + Services WLV. Free June onward. First pick for Q3 or Portal backfill.
- **Duc** — New dev. Portal only, full quarter. Pair programming with Tuan.
- **Russell** — Team lead. Winding down IC after 5/28. Shifting to team support and quality.
- **Sodiq** — Junior. MUI + VPAT. Free gaps in April and June+. Ramping up.
- **Tuan** — KPP, Clearer errors, Portal pair (4/14–5/12), Bulk Svcs, Signing, Portal QA/UAT. Well-paced.

---

## Reference: Confluence PRDs

- Zapier main PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/4390420482/Integrations+-+Zapier+improvements
- People Write Action sub-PRD: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/4424073222/Create+Update+a+Person+Write+Action
- All Platform PRDs: https://casecommons.atlassian.net/wiki/spaces/PROD/pages/3162374160/Projects

---

## Task 5: Changelog + Completion

Write changelog entries for any vault files touched (subdirectory first, then root), mark this file complete, and move to `handoff/complete/`.

---

## Notes for This Agent

- The okr-reporting Q2 structure already exists in the vault — read it before proposing anything new. Do not create duplicate KR files.
- Do not push Asana corrections without human user's explicit go-ahead in the session.
- The Dispatch AGENTS.md entry is low-urgency relative to OKRs — if the session runs long, defer to a follow-up handoff.
- This handoff may need to be split if scope grows. Flag this to human user if tasks 2–4 cannot be completed in a single session.
