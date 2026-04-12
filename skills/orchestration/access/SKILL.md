---
name: access
description: Permission and access auditor for the ben-cp vault. Synthesizes findings from the changelog skill's Check 9 scan and git logs to flag vault violations. Runs nightly or on demand. Flags only — never auto-fixes.
preferred_agent: claude
cadence: daily
report: yes
---

# Skill: Access Audit

> **Purpose:** Synthesize permission and access findings from the changelog skill's Check 9 scan and git logs. Flag vault violations based on AGENTS.md compliance.
> **Preferred Agent:** Claude (Cowork)
> **Does not auto-fix** — produces a flagged report only.
> Last updated: 2026-04-12

---

## Dependencies

This skill depends on the changelog skill having run first. Specifically, it reads the output of Check 9 (Permission & Access Scan) from the latest changelog report in `skills/orchestration/changelog/outputs/reports/`.

If no changelog report exists for the current date, stop and write a P1 handoff flagging the missing prerequisite.

---

## Workflow

| Step | What happens |
| :--- | :--- |
| **Field Scan** | changelog skill scans git logs and role summaries (Check 9) |
| **Synthesis** | access skill reads changelog report + role files → constructs violation narrative |
| **Investigation** | If synthesis is inconclusive, delegate back to changelog skill via P3 handoff |

---

## Procedure

### Pre-Flight
1. Read `AGENTS.md` — confirms role definitions and authorized directory boundaries
2. Read latest changelog skill report in `skills/changelog/outputs/reports/` — specifically Check 9
3. Read root `changelog.md` and relevant skill changelogs for the audit period
4. Run `git log --name-only` for the audit period
5. Confirm `skills/access/outputs/reports/` directory exists — create with `.gitkeep` if not
6. Read `skills/access/character.md` — adopt this voice for all report output

### Step 1 — Synthesis
For each flag in Check 9, cross-reference against changelog entries and git log. For each violation ask:
- What was the agent doing in that directory? Did they create, modify, or delete files, or just read?
- Was there an approved plan and task list before writes occurred? If not, this is a high-priority violation.
- What metadata was missed and why (e.g. tool error, oversight)?

For agent config roots (`~/.claude/` and `~/.gemini/` via symlinks), explicitly flag:
- MCP server entries pointing to paths that no longer exist on disk
- Tool permission grants (`allowedTools` / `deniedTools`) that are overly broad (e.g. `Bash(*)`)
- Orphaned project entries referencing deleted or archived repos
- Config files with permissions wider than 600
- Any credential or token values that are world-readable

Also scan all `skills/` subdirectories for lingering `notes.md` files and flag any found — these are ephemeral session artifacts that should have been deleted at session end.

### Step 2 — Separation Policy Scan (ALWAYS RUN)

Read `skills/shared/separation-policy.md` § Known Migration Debt to load the current tracked violation list.

Then walk `skills/` and flag any file that matches:
- `*.py` or `*.sh` — execution scripts
- `manifest.json` — pipeline state
- `inputs/` directories or files inside a skill subdirectory
- `logs/` directories or files inside a skill subdirectory
- `*.html`, `*.json` data files that are not spec/template files (e.g. `report_spec.json` is allowed; `asana_active.json` is not)

For each match:
1. Check whether it already appears in Known Migration Debt. If yes → skip (already tracked).
2. If new → it is a **new violation**. Write a P2 handoff: `handoff/[YYYY-MM-DD]-p2-access-separation-violation.md` listing the new files and their correct destination per the four-layer table. Do not update `separation-policy.md` yourself — the handoff is the flag.

Also scan for stale `notes.md` files in `skills/` subdirectories (per existing Pre-Flight step). These remain a P2 flag.

Priority classification for separation violations:
- **P1** — scripts or data files found in a skill directory that was not in the prior Known Migration Debt list (new regression)
- **P2** — stale notes.md files, known debt items that have not been migrated after 7+ days

---

### Step 3 — Deletion & Overwrite Watch (ALWAYS RUN)

Scan all agent outputs, skill instructions, handoffs, and changelog entries from the audit period for any language that advocates or instructs:
- Deleting files (other than ephemeral `notes.md` cleanup, which is expected)
- Overwriting existing files with `write_file` where `edit_file` should have been used
- Force-pushing, hard resetting, or destructive git operations
- Clearing, purging, or wiping outputs, reports, or archive directories

**Flag every instance as a P1 violation**, regardless of which agent, sub-agent, skill, or tool produced it. Context does not excuse it — even well-intentioned cleanup instructions that advocate deletion without explicit human user approval are a violation.

Exceptions (do NOT flag):
- `notes.md` ephemeral session cleanup (expected and required per pmm convention)
- `git mv` for archiving completed handoffs to `handoff/complete/` (approved pattern)
- Archiving reports to `outputs/reports/archive/` via `git mv` (approved pattern)

Everything else that touches existing files destructively is a violation until human user explicitly approves it.

### Step 4 — Report
Write a new report to `skills/access/outputs/reports/access-report-[YYYY-MM-DD].md` using the template at `skills/access/report.md`.

Report header must include:
- Date
- Run by: [agent name — e.g. Claude (Cowork), Antigravity (Gemini), Gemma, Claude Code]
- Total violations found
- Total oops found

Populate:
- **Violations** — one bullet per unique violation, with sub-bullet explaining what happened and why it is a violation
- **Oops** — one bullet per omission or missed access step
- **Conclusion** — brief statement of overall vault access health

If clean: state "NO OUTLIERS DETECTED." explicitly.

### Step 5 — Investigation Delegation
If a violation is complex or synthesis is blocked by missing information:
1. Identify exactly what needs a deeper read (e.g. full tool logs for a specific session)
2. Write a **P3 handoff** in `handoff/` assigned to the changelog skill
3. Include: "TREK REQUEST: Deep dive into [agent]'s activity in [directory] on [date]. Confirm [specific question]."

---

## Handoff Output
Write one handoff per priority group to `handoff/`. Skip any group with no flags.

Priority rules:
- **P1** — unauthorized writes, missing approved plan before file edits, missing changelog report prerequisite, any agent/skill/tool advocating deletion or overwrite
- **P2** — broad permission grants, orphaned config entries, lingering `notes.md` files, known separation debt items not yet migrated after 7+ days
- **P3** — investigation delegation requests, stale config values, minor omissions

File naming: `handoff/[YYYY-MM-DD]-p[N]-access-[short-description].md`

---

## Changelog
After writing the report and handoffs, write two changelog entries:
- **Subdirectory** (`skills/access/changelog.md`): report filename, run by agent, violation/oops counts, handoffs created
- **Root** (`changelog.md`): one-line summary — e.g. `Access audit [YYYY-MM-DD] by [agent]: N violations, N oops, N handoffs written`

---

## Constraints
- Read before every write — no exceptions
- Never delete, move, or modify vault files
- Use absolute paths starting with `/Users/benbelanger/GitHub/ben-cp/`
- Character names are not used outside of `character.md` files — use generic skill names only
