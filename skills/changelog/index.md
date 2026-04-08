# Skill: Changelog Procedure

> **PURPOSE:** End-of-session documentation for all agents. Uses a multi-level
> changelog system — write from the deepest relevant level outward. Each outer
> level summarizes and points back to the level below for full detail.

---

## The Multi-Level Changelog System

| Level | File | Granularity |
| :--- | :--- | :--- |
| Deepest | `skills/[name]/changelog.md` | Every file touch, exact values, KR-level detail |
| Root | `changelog.md` | Version-tagged milestones, one-liner per skill, pointer down |

Start at the deepest level. The root entry should be readable as a summary;
the subdirectory entry should be complete enough to reconstruct what happened.

---

## When to Run

- At the natural end of a work session
- When context window is approaching limit
- When handing off to a different agent (Gemma → Claude, Claude → Claude Code)
- After any significant structural change to the vault

---

## Procedure

### Stage 1 — Identify Active Skills

List which `skills/` subdirectories were touched this session. Each active
subdirectory gets its own changelog entry before the root entry is written.

### Stage 2 — Write Subdirectory Changelog Entries (Deepest First)

For each active subdirectory (e.g., `skills/okr-reporting/`):

1. Check if `skills/[name]/changelog.md` exists
   - If yes: read it first, then use `edit_file` to prepend a new entry
   - If no: create it with the starter format from `skills/changelog/entry_template.md`
2. Write with full granularity — exact paths, exact values, specific blockers
3. Include a **Next** line: what to do in this subdirectory next session

**Rule:** Always `read_text_file` before `edit_file`. Never `write_file` on an
existing changelog.

### Stage 3 — Write Root Changelog Entry

Read `changelog.md` at vault root. Find the highest `[X.Y.Z]` version and
determine the bump:

- **Patch** (`[X.Y.Z+1]`): routine work within existing skills
- **Minor** (`[X.Y+1.0]`): new skills, renamed files, structural changes
- **Major** (`[X+1.0.0]`): vault-wide rearchitecture

Prepend a new entry to root `changelog.md`:
- One-line summary per subdirectory touched
- Pointer to each subdirectory changelog: `See skills/[name]/changelog.md`
- Blockers and next tasks at vault level only — not granular KR detail

**Rule:** Use `edit_file` — never `write_file` on `changelog.md`.

### Stage 4 — Confirm and Report

State clearly:
- Subdirectory changelog(s) written (paths)
- Root `changelog.md` version and date
- Any blockers that prevented completion

---

## Creating a New Subdirectory Changelog

If `skills/[name]/changelog.md` does not exist, create it with:

```markdown
# [Skill Name] Changelog

> Detail log for `skills/[name]/`. See root `changelog.md` for version history.

---

## [Unreleased]
```

Then prepend the first entry immediately below `## [Unreleased]`.

---

## Entry Template

See `skills/changelog/entry_template.md` for copy-paste templates at both levels.
