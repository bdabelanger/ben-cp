# Claude Code Implementation Plan: Wrap-Up & Changelog Refactor

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **v1.0**

---

## Context

The vault currently uses `skills/gemma-wrap-up-latest.md` as a session handoff
file — a single file that gets overwritten each session. This approach loses
history and is disconnected from the project's changelog methodology.

**Goal:** Route session wrap-ups into `changelog.md` at vault root as the
single versioned record. Define the wrap-up procedure in `skills/wrap-up/` so
all agents follow a consistent format. Retire `gemma-wrap-up-latest.md` as the
primary handoff mechanism.

---

## Execution Order

Run tasks in sequence. Read before every write — no exceptions.

1. **Task 1** — Audit existing wrap-up infrastructure
2. **Task 2** — Rewrite `skills/wrap-up/index.md` (the procedure)
3. **Task 3** — Create `skills/wrap-up/changelog_entry_template.md`
4. **Task 4** — Update `agents/gemma.md` — point to new wrap-up procedure
5. **Task 5** — Update `gemma-rules.md` Rule 7 — new wrap-up target
6. **Task 6** — Update `agents/claude.md` — handoff protocol
7. **Task 7** — Archive `skills/gemma-wrap-up-latest.md` into `changelog.md`
8. **Task 8** — Final audit and completion report

---

## Task 1: Audit Existing Wrap-Up Infrastructure

Read the following files and confirm their current state before making any
changes. Report any discrepancies.

1. `skills/wrap-up/index.md` — current procedure
2. `skills/wrap-up/changelog.md` — skill-level log (separate from root)
3. `changelog.md` — root project changelog
4. `skills/gemma-wrap-up-latest.md` — current handoff file
5. `agents/gemma.md` — current wrap-up reference
6. `gemma-rules.md` — Rule 7 current wording

---

## Task 2: Rewrite `skills/wrap-up/index.md`

**Purpose:** Define the canonical wrap-up procedure for all agents. This is
what any agent reads when it needs to know how to close a session.

**Read first:** current `skills/wrap-up/index.md`

**Replace with the following content:**

```markdown
# Skill: Wrap-Up & Changelog Procedure

> **PURPOSE:** End-of-session procedure for all agents. Captures completed
> work, blockers, and next tasks as a versioned changelog entry at project root.
> Run at the end of every session or when context is near limit.

---

## When to Run

- At the natural end of a work session
- When context window is approaching limit
- When handing off to a different agent (Gemma → Claude, Claude → Claude Code)
- After any significant structural change to the vault

---

## Procedure

### Stage 1 — Summarize the Session

Collect from the session:
- **Files created** (full paths)
- **Files modified** (full paths)
- **KR state changes** (if working in okr-reporting)
- **Blockers encountered** (unresolved issues)
- **Next tasks** (what the next agent should do first)

### Stage 2 — Determine Version Number

Read `changelog.md` at vault root. Find the highest existing version number
(e.g., `[1.0.3]`). Increment the patch version for routine sessions
(→ `[1.0.4]`), minor version for structural changes (→ `[1.1.0]`).

### Stage 3 — Write Changelog Entry

Append a new entry to `changelog.md` using the template in
`skills/wrap-up/changelog_entry_template.md`.

**Rules:**
- Use `edit_file` — never `write_file` on `changelog.md`
- Read `changelog.md` first, then append — do not overwrite
- New entries go at the TOP of the file, below the `## [Unreleased]` header
- Use today's date in `[YYYY-MM-DD]` format

### Stage 4 — Update `skills/gemma-wrap-up-latest.md`

After writing to `changelog.md`, also write a brief next-session handoff to
`skills/gemma-wrap-up-latest.md`. This file is Gemma's quick-load context —
keep it focused on what to do next, not a full history.

**Contents of gemma-wrap-up-latest.md:**
- Pointer to the latest changelog entry for full history
- Do-not-touch file list
- Next 1–3 tasks with enough context to act without asking
- Directive reminder block

### Stage 5 — Confirm and Report

State clearly:
- Changelog entry version and date written
- gemma-wrap-up-latest.md updated: yes/no
- Any blockers that prevented completion

---

## Scope Note

`changelog.md` at vault root tracks project-level changes.
In the future, individual skills (e.g., `skills/okr-reporting/`) may have
their own changelogs for high-volume work. When that threshold is reached,
create `skills/[skill-name]/changelog.md` and note it in the root changelog.
```

---

## Task 3: Create `skills/wrap-up/changelog_entry_template.md`

**Check first:** confirm this file does not exist in `skills/wrap-up/`

**Write the following content:**

```markdown
# Changelog Entry Template

Copy this block and fill in for each new entry. Append below `## [Unreleased]`
in `/Users/benbelanger/GitHub/ben-cp/changelog.md`.

---

## [X.Y.Z] - [Short Title] ([YYYY-MM-DD])

**Changes:**
- [File created/modified] — [one-line description]
- [File created/modified] — [one-line description]

**KR State:**
- [KR name]: [status change, e.g. "⏳ Pending → ✅ Confirmed, baseline 32%"]
- (omit section if no KR work this session)

**Blockers:**
- [description] — [what's needed to unblock]
- (omit section if none)

**Next Tasks:**
1. [Task description — enough context to act]
2. [Task description]

**Observations:**
- [Process note, lesson learned, or efficiency improvement]
- (omit section if none)
```

---

## Task 4: Update `agents/gemma.md`

**Read first:** current `agents/gemma.md`

Change the **Session Wrap-Up** section. Replace:

> At end of every session, write a wrap-up to:
> `skills/gemma-wrap-up-latest.md`
>
> Include: files created, files modified, blockers, next task, KR state snapshot.

With:

> At end of every session, follow the wrap-up procedure at
> `skills/wrap-up/index.md`. This writes a versioned entry to `changelog.md`
> AND updates `skills/gemma-wrap-up-latest.md` as a quick-load handoff.

---

## Task 5: Update `gemma-rules.md` Rule 7

**Read first:** current `gemma-rules.md`

Change Rule 7. Replace:

> - Write the wrap-up to: `skills/gemma-wrap-up-latest.md`

With:

> - Follow the wrap-up procedure: `skills/wrap-up/index.md`
> - This writes to both `changelog.md` (versioned history) and
>   `skills/gemma-wrap-up-latest.md` (next-session handoff)

---

## Task 6: Update `agents/claude.md`

**Read first:** current `agents/claude.md`

Change the **Handoff Protocol** section. Replace:

> When handing off to Gemma, write a wrap-up to:
> `skills/gemma-wrap-up-latest.md` (use the gemma-wrap-up Cowork skill).

With:

> When handing off to Gemma, follow the wrap-up procedure at
> `skills/wrap-up/index.md`. Write a versioned entry to `changelog.md`
> and update `skills/gemma-wrap-up-latest.md` as the quick-load handoff.

---

## Task 7: Archive Current `skills/gemma-wrap-up-latest.md` into `changelog.md`

**Read first:** both `changelog.md` and `skills/gemma-wrap-up-latest.md`

The current `gemma-wrap-up-latest.md` contains the session summary from
2026-04-08 (vault quality layer build + OKR reporting SOPs). This should be
the first entry written using the new format to bootstrap the new methodology.

Write a new changelog entry `[1.1.0]` (minor bump — structural change session)
to `changelog.md` capturing that session's work. Use the template from Task 3.

After writing to `changelog.md`, rewrite `skills/gemma-wrap-up-latest.md`
to the new slim format (Stage 4 of the wrap-up procedure): pointer to changelog
entry, do-not-touch list, next 1–3 tasks, directive reminder.

---

## Task 8: Final Audit and Completion Report

1. Read `changelog.md` — confirm new entry is present and correctly formatted
2. Read `skills/gemma-wrap-up-latest.md` — confirm it is now in slim format
3. Read `skills/wrap-up/index.md` — confirm procedure is in place
4. Read `skills/wrap-up/changelog_entry_template.md` — confirm template exists
5. Read `agents/gemma.md` — confirm wrap-up section updated
6. Read `gemma-rules.md` — confirm Rule 7 updated
7. Read `agents/claude.md` — confirm handoff protocol updated

Output completion report:

```
## Completion Report — Wrap-Up & Changelog Refactor v1.0

**Files created:**
- [full path] — [description]

**Files modified:**
- [full path] — [what changed]

**Flags for Ben:**
- [anything unexpected]

**Not completed / blockers:**
- [anything that could not be done and why]
```

---

## Notes for This Agent

- `changelog.md` at root is the source of truth — always `read_text_file`
  before appending; never overwrite the whole file
- `skills/gemma-wrap-up-latest.md` is intentionally short after this refactor —
  it is a next-session pointer, not a history file
- Do not modify `skills/okr-reporting/` files as part of this plan
- Follow all Read → Write rules from `AGENTS.md`
