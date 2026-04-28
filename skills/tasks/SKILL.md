---
title: 'Skill: Task Management (Deliverable Governance)'
type: skill
domain: skills/tasks
---


# Skill: Task Management (Deliverable Governance)

- **agent:** Antigravity
- **status:** 🟢 Codified
- **type:** Execution Skill

## Skill: Task Management

> **Description:** Governance standard for managing strategic, human-led deliverables and project work items.
> **Domain:** Orchestration / Tasks
> **Preferred Agent:** Code (Engineering) / Cowork (Planning)

## Connections
- **Input:** Implementation Plans (P1/P2) or direct human user requests.
- **Output:** Final project deliverables and repo-ready artifacts.

## The Hierarchy
Tasks are centralized at `tasks/`. 
- **Active Tasks**: Root of the directory.
- **Archive**: `tasks/archive/` (moved here upon completion).

## Workflow Summary
1. **Initiation:** Create a new task file using `add_task`. Use a hyphenated, descriptive name (e.g., `prd-migration-q2.md`).
2. **Metadata Standard:** Every task MUST contain a YAML block with:
    - `status`: [DRAFT, ACTIVE, BLOCKED, COMPLETED]
    - `priority`: [P1, P2, P3, P4]
    - `owner`: (Human user or assigned agent)
3. **Execution:** Agents update the task status and "Progress" section as work is completed.
4. **Completion:** Upon final approval, the task is marked `COMPLETED` and moved to the archive. A root changelog entry MUST point to the completed task file.

## Constraints
- **Human Authority:** Tasks are "Strategic." Agents SHOULD NOT unilaterally create or modify Task goals without explicit direction from the human user.
- **No Duplication:** Do not create a Task for something that is already covered by an active Handoff. Tasks are for *outcomes*, Handoffs are for *execution steps*.

