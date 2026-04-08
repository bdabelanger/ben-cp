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

### Step 2 — Read the Handoff File
Read the full handoff file. Note:
- **STATUS line** — confirms it's `🔲 READY` (not already complete)
- **Execution Order** — tasks must run in the specified sequence
- **Notes for This Agent** — read last; contains constraints specific to this plan

### Step 3 — Execute
Follow the plan's Execution Order exactly. For each task:
- Read before every write — no exceptions
- If a task is ambiguous or the prerequisite state doesn't match what the plan
  expects, stop and flag — do not improvise
- Report unexpected findings inline as you go

### Step 4 — Mark Complete
When all tasks are done (or fully attempted with blockers documented):

1. Update the STATUS line from `🔲 READY` to `✅ COMPLETE — [date]`
2. Add a one-paragraph summary below the STATUS block: what was done, any flags for Ben
3. After the changelog entry is written (root `changelog.md`), add a **Changelog** line to the completion summary:
   `**Changelog:** [X.Y.Z] — [date] (see root changelog.md)`
4. Move the file: `handoff/YYYY-MM-DD-[name]-COMPLETE.md` → `handoff/complete/YYYY-MM-DD-[name]-COMPLETE.md`
   - Anything remaining in `handoff/` root is treated as open — moving to `complete/` is what closes it

---

## Handoff File Format (for creating agents)

When creating a handoff for another agent, use this structure:

```markdown
# [Receiving Agent] Implementation Plan: [Short Title]

> **Prepared by:** [Agent] ([context], [YYYY-MM-DD])
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
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

---

## Task 1: [Title]
[Detailed instructions — what to read first, what to write, exact content if needed]

---

## Task N: Final Audit and Completion Report
[What to verify, what to output]

---

## Notes for This Agent
- [Constraints, do-not-touch files, edge cases]
```

**File naming:** `handoff/YYYY-MM-DD-[kebab-title].md`
**Completion naming:** `handoff/complete/YYYY-MM-DD-[kebab-title]-COMPLETE.md`
**Open handoffs:** anything in `handoff/` root
**Closed handoffs:** anything in `handoff/complete/`

---

## Completion File Format

After execution, the file header should look like:

```markdown
> **STATUS: ✅ COMPLETE — [YYYY-MM-DD]**

[One paragraph: what was done, any flags for Ben, any blockers that remain.]

**Changelog:** [X.Y.Z] — [YYYY-MM-DD] (see root `changelog.md`)
```
