---
title: Triage Overdue Tasks
priority: P2
assigned_to: Cowork (Sonnet 4.6)
status: READY
date: 2026-04-27
---

# Implementation Plan: Triage Overdue Tasks

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Cowork (Sonnet 4.6)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

## Context

The latest Dream report (2026-04-27) identifies **24 overdue tasks** synchronized from Asana and Jira. These tasks appear concentrated in the vault normalization and intelligence harvest domains. Given the recent major architectural shifts (migrating logic to `skills/`, normalizing `intelligence/` records), many of these tasks may be stale, superseded by already-executed handoffs, or requiring re-routing to new owners.

## Logic

Cowork should perform a strategic review of the overdue task list to clean up the orchestration layer and ensure the task backlog accurately reflects the post-normalization state of the vault.

## Execution Steps

1. **Review Task Report**: Read `reports/tasks/report.md` (or use `list_tasks`) to extract the list of 24 overdue items.
2. **Categorization**: Match tasks against the current vault state:
   - **Stale/Superseded**: Tasks referencing legacy paths (`orchestration/`, `intelligence/core/skills/`) or goals already completed by recent P1/P2 handoffs.
   - **Active/Blocked**: Legitimate work items that were delayed by dependencies (like the frontmatter sensor or pyyaml installation).
   - **Re-route**: Tasks that need to be assigned to specific agents (Code, Local) for execution based on the `AGENTS.md` lanes.
3. **Draft Updates**: For each task, propose a status update or archival path. Note: Tasks are read-only sync targets from Asana; use the Asana MCP tool to update the source of truth where appropriate.
4. **Coordinate**: Present the triaged list to Ben for confirmation before executing bulk updates.

## Verification

- [ ] Overdue task count in Dream report drops from 24.
- [ ] Task backlog reflects only active, non-superseded work.
- [ ] Stale architectural references are eliminated from the active task set.
