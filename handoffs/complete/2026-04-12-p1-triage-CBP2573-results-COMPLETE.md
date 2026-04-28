---
title: 'Bug Triage: CBP-2573'
type: handoff
domain: handoffs/complete
---


# Bug Triage: CBP-2573

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Ben
> **Repo root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-26

Converted to task: triage-cbp-2573. No agent execution required — this is a human action item for Ben.

---

**Project Context:** CBP-2924 (Notes - Bulk Service Notes)
**Bug:** CBP-2573 — intermittent failure when adding multiple services to a single note

## Findings

- **Intermittency**: Suggests a race condition or state synchronization issue during the bulk service note creation phase.
- **Scope**: Exclusive to adding *multiple* services on a single note — points to the loop logic or API batch processing in the frontend/backend for CBP-2924.
- **Project Affiliation**: Not an independent regression — a maturing bug within active development of Bulk Service Notes. Should stay as a sub-task of CBP-2924.

## Recommended Actions for Ben

1. **Developer Triage**: The assigned developer for CBP-2924 should inspect the `service_interaction` payload generation logic.
2. **Reproduction**: Attempt to trigger the bug by adding 5+ services rapidly to a note in dev/QA.
3. **Tracking**: Keep as a sub-task of CBP-2924 — do not split into a separate initiative, as this blocks the primary GA criteria for that project.

## Verification Notes

- Repo `jira_issues.json` confirms parentage and status.
- No direct source code for service creation logic found in this repo (external dependency or sibling project).
