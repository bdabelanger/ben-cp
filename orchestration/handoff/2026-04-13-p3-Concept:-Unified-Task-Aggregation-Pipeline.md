# Implementation Plan: Concept: Unified Task Aggregation Pipeline

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude (Conceptual)
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P3
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

## Objective
Establish a unified task aggregation pipeline to harvest "Assigned to Human" work from external systems (Asana, Jira, etc.) and stage it in the vault for agent-assisted execution.

## Context
The user has tasks scattered across multiple platforms. We want to bring these into the vault's new root `/tasks/` domain so agents can help prioritize, draft deliverables, and codify results.

## Proposed Architecture
1. **Pipeline Home:** `orchestration/pipelines/tasks/unified/`
2. **Standard Structure:**
   - `pipeline/`: Python logic for multi-service harvesting.
   - `inputs/`: Raw API seeds.
   - `outputs/`: Staged `.md` task files mapped to `tasks/incoming/`.
   - `schemas/`: Unified Task Schema (Title, Source System, Due Date, Priority, Context).
3. **Execution Mode:**
   - Script should identify "New" tasks and "Updates" to existing ones.
   - Agents can then use `get_task` / `edit_task` to help the user clear the backlog.

## Next Steps
- Research Asana/Jira API endpoints for "User's My Tasks."
- Draft the Unified Task Schema.
- Implement a MVP harvester for a single source (e.g., Asana).
