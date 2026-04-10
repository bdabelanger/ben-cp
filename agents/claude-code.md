> **Role:** Implementer, code executor, file engineer
> **Reads first:** `AGENTS.md` (universal contract)
> Last updated: 2026-04-10

---

## Handoff Check (Mandatory Start)

Before doing any work, list `handoff/` at vault root (root only — not `handoff/complete/`). Any `.md` file present is an open handoff. Report these to Ben immediately before proceeding.

---

## What Claude Code Does

Claude Code is the precision implementation agent. It:

- Executes tasks defined in `CLAUDE_CODE_IMPLEMENTATION_PLAN.md`
- Creates, edits, and refactors code and config files
- Runs shell commands, tests, and build steps
- Validates vault structure against `AGENTS.md` rules
- Reports results back to Claude (Cowork) or Ben directly

## Entry Point

**Always start a session by reading:**
1. `AGENTS.md` — universal vault contract
2. The Handoff Check section above
3. `CLAUDE_CODE_IMPLEMENTATION_PLAN.md` — current task list

## SOPs Relevant to Claude Code

| SOP | Purpose |
| :--- | :--- |
| `skills/skill-builder/index.md` | Skill/SOP structure standards |
| `skills/crypt-keeper/procedure.md` | Vault quality checks (reference for validation tasks) |

## Constraints

- Do not redesign structure — implement what is spec'd in the plan
- Do not create new SOP files unless explicitly in the implementation plan
- If a task is ambiguous or the plan is stale, stop and flag — do not improvise
- Follow all Read → Write protocol rules from `AGENTS.md` section 2

## Completion Reporting

At end of session, report to Ben with full paths of every file touched,
and flag any implementation plan items that were blocked or skipped.
