# Bug Triage: CBP-2573 — Intermittent Failure Adding Multiple Services to a Note

- **priority:** P1
- **assigned_to:** Ben
- **source_handoff:** 2026-04-12-p1-triage-CBP2573-results.md
- **jira:** CBP-2573
- **parent_project:** CBP-2924
- **created:** 2026-04-25

# Bug Triage: CBP-2573 — Intermittent Failure Adding Multiple Services to a Note

> **Priority:** P1
> **Assigned to:** Ben
> **Jira:** CBP-2573 (sub-task of CBP-2924 — Notes: Bulk Service Notes)
> **Source handoff:** 2026-04-12-p1-triage-CBP2573-results.md
> **Created:** 2026-04-25

## Context

Intermittent failure when adding multiple services to a single note. Likely a race condition or state sync issue in the bulk service note creation phase. Scoped to CBP-2924 — not a standalone regression.

## Actions

1. **Developer triage**: Assigned dev for CBP-2924 should inspect the `service_interaction` payload generation logic
2. **Reproduce**: Attempt to trigger by adding 5+ services rapidly to a note in dev/QA
3. **Tracking**: Keep as sub-task of CBP-2924 — do not split; this blocks GA criteria for that project

