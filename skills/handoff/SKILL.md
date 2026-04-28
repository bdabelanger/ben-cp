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

### Step 4 — Write Changelog
Before marking complete, write a changelog entry using `add_changelog`:
- **Root level** — detailed summary of structural or logic changes.
- **Handoff Pointer:** Include `**Handoff:** reports/handoff/archive/[filename]-ARCHIVE.md` in the entry.

### Step 5 — Mark Complete
When all tasks are done (or fully attempted with blockers documented):
1. Update the STATUS line from `🔲 READY` to `✅ COMPLETE — [date]`
2. Add a one-paragraph summary below the STATUS block: what was done, any flags for human user
3. Add a **Changelog** line: `**Changelog:** [X.Y.Z] — [date] (see root changelog.md)`
4. Move the file to `reports/handoff/archive/` via `edit_handoff`.

---

## Handoff File Format (for creating agents)

When creating a handoff for another agent, use this structure:

```markdown
# [Receiving Agent] Implementation Plan: [Short Title]

> **Prepared by:** [Agent] ([context], [YYYY-MM-DD])
> **Assigned to:** [Claude | Code (Claude Code / Antigravity) | Gemma | Any]
> **Priority:** P[N] — [one-line reason]
> **v1.0**
> **STATUS: 🔲 READY — pick up [YYYY-MM-DD]**

---

## Context
[Why this work is needed — 2–4 sentences]

---

## Execution Order
1. **Task 1** — [short label]
2. **Task 2** — [short label]
...
N. **Task N** — Write changelog and mark complete

---

## Task 1: [Title]
[Detailed instructions — what to read first, what to write, exact content if needed]

---

## Task N: Changelog + Completion

Write changelog entry, then mark this file complete via `edit_handoff`.

---

## Notes for This Agent
- [Constraints, do-not-touch files, edge cases]
```

**File naming:** `reports/handoff/YYYY-MM-DD-p[N]-[kebab-title].md`

Priority levels (governed by `AGENTS.md` Thresholds):
- **P1 (Critical)** — agent navigation broken (orphaned files, missing overview.md, misplaced files) or core pipeline logic failure. Requires `implementation_plan.md` + `walkthrough.md`.
- **P2 (Major)** — structural violations (AGENTS.md compliance, root-level stubs, duplicates). Requires `implementation_plan.md`.
- **P3 (Minor)** — data quality gaps (data_sources.md sync, stale flags, low-urgency cleanup). Plan included within handoff.
- **P4 (Trivial)** — Typos, formatting, or atomic dependency updates. No handoff required (Atomic execution).

---

## Audit Requirements
- [ ] **Continuity**: Every session must starting with a handoff check and end with a handoff update/creation.
- [ ] **Traceability**: All handoff files must follow the kebab-case naming convention.
- [ ] **Closure**: Completed work must be explicitly noted in the final call to the handoff tool.

---

## Tool Utility
- **add_handoff**: Primary tool for creating the persistent context for the next agent.
- **list_handoffs**: Used to scan for the most recent queue of active work.
- **edit_handoff**: Update a handoff or mark it as complete.

---

## Links
- [Audit logic (run.py)](run.py)
