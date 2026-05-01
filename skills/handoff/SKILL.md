---
title: 'Skill: Handoff Protocol'
type: skill
domain: skills/handoff
---


# Skill: Handoff Protocol

> **Purpose:** Management of the asynchronous agent relay system to ensure perfect continuity across session gaps. Any agent receiving a handoff from another agent follows this protocol.
> **Preferred Agent:** Cowork / Code
> **Cadence:** Start and End of every session

---

## Receiving a Handoff

### Step 1 — Orient
Before reading the handoff file, load repo context:
1. Read `AGENTS.md` at repo root — confirms current structure and rules
2. Read your role file (`governance/[your-agent].md`) if not already loaded

### Step 2 — Read and Scrutinize
Read the full handoff file. Note:
- **STATUS line** — confirms it's `🔲 READY` (not already complete)
- **Priority** — P1 first, then P2, P3
- **Scrutiny Policy**: Treat handoffs as proposals, not mandates. If you identify a structural violation or a more efficient path, discuss it with the human user or propose specific edits to the handoff before proceeding.
- **Source report** — read it for full context before executing (if present)
- **Execution Order** — tasks must run in the specified sequence
- **Notes for This Agent** — read last; contains constraints specific to this plan

### Step 3 — The Review Gate
1. **Tiered Validation**: Use the **Decision Matrix** in `AGENTS.md` to determine if mandatory artifacts (Plan/Walkthrough) are present for the given priority.
2. **Small Changes**: Minor adjustments or human-approved edits can move directly into execution.
3. **Automated Workflows / P1-P2**: Any task involving an automated pipeline, complex ingestion, or P1/P2 architectural shifts MUST be assigned back to **Cowork** for a final review gate before physical execution. **P1/P2 handoffs MUST refer to an `implementation_plan.md`.**
4. **Execution**: Follow the plan's Execution Order exactly after the review gate is clear.
   - Read before every write — no exceptions
   - If a task remains ambiguous, stop and flag — do not improvise.

## Step 4 — Write Changelog
Changelog writing is now handled automatically by the `archive_handoff` tool. You do not need to call `add_changelog` separately when closing a handoff.

### Step 5 — Mark Complete
When all tasks are done (or fully attempted with blockers documented):
1. Use the `archive_handoff` tool.
2. Provide a `summary` of work done.
3. The tool will automatically:
   - Update frontmatter to `✅ COMPLETE`
   - Move the file to `reports/handoff/archive/`
   - Write a structured entry to the root `changelog.md`

---

## Lifecycle & Status

Handoffs follow a strict state machine:

1. **READY**: Handoff is created and waiting for an agent.
2. **IN_PROGRESS**: Agent has picked it up and appended an `## Implementation Plan`.
3. **COMPLETE**: Work is finished, summary is appended, and file is archived.

To transition a handoff from `READY` to `IN_PROGRESS`, call `edit_handoff` with `status: 'IN_PROGRESS'` when appending your implementation plan.

---

## Standard Sections

To maintain an auditable, chronological record, agents MUST use these standard section headers when appending content via `edit_handoff`:

### `## Implementation Plan ([Agent], [YYYY-MM-DD])`
- **Required** when picking up a `READY` handoff.
- Set `status: 'IN_PROGRESS'` in the same call.
- Contains the "How" — specific files, steps, and logic.

### `## Update ([Agent], [YYYY-MM-DD])`
- Used for mid-session progress, blockers, or deviations.
- Use `[x]` to mark progress in your steps.

### `## Review: [State] ([Agent], [YYYY-MM-DD])`
- **[Requested]**: Any agent needing input or approval.
- **[Approved]**: **Cowork only**. Sign-off to proceed or archive.
- **[Needs Revision]**: **Cowork only**. Stop work and address feedback.

---

## Tool Utility

| Tool | Who | When |
| :--- | :--- | :--- |
| `add_handoff` | Any agent | Create a new cross-agent relay. |
| `list_handoffs` | Any agent | Discover open work. Filter by `READY` or `IN_PROGRESS`. |
| `get_handoff` | Any agent | Read the full content and history of a plan. |
| `edit_handoff` | Any agent | Update a live handoff. Always use `append: true`. |
| `archive_handoff` | **Cowork only** | Mark complete, move to archive, and write changelog. |

---

## Handoff File Format

```markdown
---
title: "[Short Title]"
priority: P[N]
assigned_to: [Agent]
status: READY
date: YYYY-MM-DD
---
# Implementation Plan: [Short Title]

> **Prepared by:** [Agent] ([YYYY-MM-DD])
> **Assigned to:** [Agent]
> **Priority:** P[N]
> **STATUS: 🔲 READY**

---

## Context
[Problem statement and background]

## Execution Steps
- [ ] Step 1
- [ ] Step 2
```

**File naming:** `reports/handoff/YYYY-MM-DD-p[N]-[kebab-title].md`

---

## Links
- [Audit logic (handoffs.py)](../dream/scripts/handoffs.py)
