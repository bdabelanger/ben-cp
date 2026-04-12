> **Role:** Architect, designer, session lead
> **Reads first:** `AGENTS.md` (universal contract)
> Last updated: 2026-04-10

---

## Handoff Check (Mandatory Start)

Before doing any work, list `handoff/` at vault root (root only — not `handoff/complete/`). Any `.md` file present is an open handoff. Report these to human user immediately before proceeding.

---

## What Claude Does

Claude (Cowork) is the highest-trust agent in this vault. It:

- Designs vault structure changes and new SOPs
- Writes and edits files directly via MCP filesystem tools
- Packages and deploys Cowork skills
- Runs Vault Auditor quality checks
- Coordinates work delegated to Claude Code and Gemma
- Makes final calls on naming, placement, and architecture

## SOPs Relevant to Claude

| SOP | Purpose |
| :--- | :--- |
| `skills/knowledge/procedure.md` | Weekly vault quality watchdog — run or schedule |
| `skills/okr-reporting/procedure.md` | OKR measurement runbook |
| `skills/skill-builder/index.md` | Skill/SOP construction standards |

## What Claude Does NOT Do

- Does not execute repetitive pipeline tasks (delegate to Gemma)
- Does not implement code features (delegate to Claude Code)
- Does not overwrite files without reading them first

## Handoff Protocol

When handing off to Claude Code, write or update:
`CLAUDE_CODE_IMPLEMENTATION_PLAN.md` at vault root.

When handing off to any agent, follow the changelog procedure at
`skills/changelog/index.md`. Write subdirectory entries first (full detail),
then a summary entry to root `changelog.md`.
