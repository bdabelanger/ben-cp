---
title: 'Skill: Handoff Protocol'
type: index
domain: skills/handoff
---


# Skill: Handoff Protocol

> **PURPOSE:** Cross-agent implementation plan execution. Any agent receiving
> a handoff from another agent follows this protocol. Also defines the format
> for creating handoff files.

---

## Receiving a Handoff

### Step 1 — Orient
Before reading the handoff file, load vault context:
1. Read `AGENTS.md` at vault root — confirms current structure and rules
2. Read your role file (`agents/[your-agent].md`) if not already loaded

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
Before marking complete, write a changelog entry using `write_changelog_entry`:
- **Subdirectory level** for each `skills/` directory touched — full detail.
- **Root level** — one-line summary + pointer to subdirectory changelog(s).
- **Resilience Policy:** If a subdirectory changelog write fails, follow the **Course Correction Protocol** in `AGENTS.md`. 1-2 attempts to fix, then escalate to root-only logging with a clear flag for human user about the failure.
- Include `**Handoff:** handoff/complete/[filename]-COMPLETE.md` in the root entry.

### Step 5 — Mark Complete
When all tasks are done (or fully attempted with blockers documented):

1. Update the STATUS line from `🔲 READY` to `✅ COMPLETE — [date]`
2. Add a one-paragraph summary below the STATUS block: what was done, any flags for human user
3. Add a **Changelog** line: `**Changelog:** [X.Y.Z] — [date] (see root changelog.md)`
4. Move the file to `handoff/complete/`:
   `git mv handoff/[filename].md handoff/complete/[filename]-COMPLETE.md`
   — Anything remaining in `handoff/` root is treated as open

---

## Editability Rules

- **Open handoffs** (`handoff/*.md`) — fully editable. Iterate freely as plans evolve.
- **Completed handoffs** (`handoff/complete/*.md`) — never edit. Historical record only.
- **Changelogs** — append-only always. This rule does NOT extend to handoffs.

---

## Handoff File Format (for creating agents)

When creating a handoff for another agent, use this structure:

```markdown
# [Receiving Agent] Implementation Plan: [Short Title]

> **Prepared by:** [Agent] ([context], [YYYY-MM-DD])
> **Assigned to:** [Claude | Code (Claude Code / Antigravity) | Gemma | Any]
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P[N] — [one-line reason]
> **Source report:** [path to report if Vault Auditor origin, else omit]
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

Write changelog entries (subdirectory first, then root), then mark this file
complete and move to `handoff/complete/`.

---

## Notes for This Agent
- [Constraints, do-not-touch files, edge cases]
```

**File naming:** `handoff/YYYY-MM-DD-p[N]-[kebab-title].md`

Priority levels (governed by `AGENTS.md` Thresholds):
- **P1 (Critical)** — agent navigation broken (orphaned files, missing index.md, misplaced files) or core pipeline logic failure. Requires `implementation_plan.md` + `walkthrough.md`.
- **P2 (Major)** — structural violations (AGENTS.md compliance, root-level stubs, duplicates). Requires `implementation_plan.md`.
- **P3 (Minor)** — data quality gaps (data_sources.md sync, stale flags, low-urgency cleanup). Plan included within handoff.
- **P4 (Trivial)** — Typos, formatting, or atomic dependency updates. No handoff required (Atomic execution).

Examples:
- `handoff/2026-04-14-p1-crypt-keeper-orphaned-index-entries.md`
- `handoff/2026-04-14-p2-fix-root-violations.md`
- `handoff/2026-04-14-p3-data-sources-portal-gaps.md`

**Completion naming:** `handoff/complete/YYYY-MM-DD-p[N]-[kebab-title]-COMPLETE.md`
**Open handoffs:** anything in `handoff/` root
**Closed handoffs:** anything in `handoff/complete/`

---

## Completion File Format

After execution, the file header should look like:

```markdown
> **STATUS: ✅ COMPLETE — [YYYY-MM-DD]**

[One paragraph: what was done, any flags for human user, any blockers that remain.]

**Changelog:** [X.Y.Z] — [YYYY-MM-DD] (see root `changelog.md`)
```

- [Audit](audit.md)
- [Skill](SKILL.md)
