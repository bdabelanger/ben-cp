---
title: Implementation Plan dream-cycles
type: handoff
domain: handoffs/complete
---

# Implementation Plan: dream-cycles

> **Prepared by:** Claude via Cowork/Dispatch (2026-04-11)
> **Assigned to:** Claude (desktop)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1 — introduces the nightly automation system for the vault
> **v1.1**
> **STATUS**: ✅ COMPLETE

Finalized the architectural design for "Daily Progress Digest," establishing the flow sequence (Strategic PM -> Changelog Auditor -> Vault Auditor -> Roz -> Robert -> Bryan -> Digest Editor) and character voices for the vault's nightly orchestration report. Broke down the build phase into discrete P1 and P2 handoffs to preserve focus during execution.

**Changelog:** (see root changelog.md)


---

## Context

Human user wants to introduce "dream cycles" — a nightly local automation that runs all meta-agents in sequence to close loops, surface gaps, and keep the vault healthy after each day's work. The concept mirrors how large language models consolidate learning during rest cycles: each night, the system reviews the day's changes, checks for drift, updates indexes, audits changelogs, and prepares a clean state for the next session.

Dream cycles run locally (on human user's machine, not in the cloud). They are scheduled, automated, and largely silent — flagging issues for human user to review in the morning rather than requiring real-time interaction.

**Key dependency:** `handoff/2026-04-12-p1-roz-agent-definition.md` must be completed before finalizing the agent roster here. Roz is a new agent whose role and character are being defined separately.

---

## Execution Order

1. **Load context** — Read `AGENTS.md`, all existing meta-agent index files, and the scheduler skill if available
2. **Design the dream cycle architecture** — Produce a proposed design for human user's review before implementing anything (see Task 2)
3. **Implement the scheduler/orchestrator** — Once human user approves the design
4. **Create `character.md` for each participating agent** — New convention, see Task 4
5. **Register all participating meta-agents** — Confirm each agent's role in the cycle
6. **Test a dry run** — Verify the cycle runs without errors before enabling nightly scheduling
7. **Changelog + completion**

---

## Task 1: Load Context

Before designing anything, read:
- `AGENTS.md` — understand all current meta-agents and their roles
- `robert/index.md` and `robert/diff_checker.md` — Robert monitors AGENTS.md for Creed drift
- `lumberjack/index.md` and `lumberjack/procedure.md` — Changelog Auditor audits changelogs
- `crypt-keeper/index.md` and `crypt-keeper/procedure.md` — Vault Auditor runs 7-check vault quality watchdog
- `rovo/index.md` — Rovo synthesizes Atlassian context (on-demand only, not nightly)
- `quartermaster/index.md` — Strategic PM is session-level and ephemeral, not nightly
- `handoff/2026-04-12-p1-roz-agent-definition.md` — Roz's role and character (must be defined first)
- `handoff/2026-04-12-p2-product-skill-consolidation.md` — product skill restructure may affect agent paths

Also check whether a scheduler script or launchd plist already exists (there is a `project-status-reports/logs/launchd.log` which suggests one is in place).

---

## Task 2: Design the Dream Cycle Architecture

Produce a written design proposal for human user's review before any implementation.

### Cycle trigger
- Nightly schedule (suggested: 2am local time)
- Runs locally via launchd (macOS)
- Can also be triggered manually: `python3 skills/dream/run.py`

### Participating agents and phases

| Phase | Agent | What it does |
|---|---|---|
| 1 | Robert | Diffs AGENTS.md against the Creed, flags drift |
| 2 | Changelog Auditor | Audits changelogs for accuracy, completeness, and cross-references |
| 3 | Vault Auditor | Runs 7-check vault quality watchdog |
| 4 | Roz | Checks external connectors and integrations, logs outliers only |
| 5 | Strategic PM cleanup | Flags any lingering quartermaster.md files from today's sessions |
| 6 | Handoff queue review | Surfaces open P1 handoffs older than 3 days |
| 7 | Dream report | Compiles all agent segments into the nightly report |

### Dream report format — "The Show"

The dream report is structured as a recurring show, not a flat log. Each meta-agent is a character with their own segment, delivered in their own voice and format. Human user reads it like tuning into each character's update.

The report opens with a brief header and episode number, then cuts to each agent in phase order. Agents with nothing to report are skipped (no "all clear" noise). The report closes with a brief summary of any P1 flags requiring action tomorrow.

**Format reference per agent:**

**Changelog Auditor** — field notes, bulleted list, written from the perspective of a logger in the field. Factual, observational, slightly gruff. Example:

```
LUMBERJACK — Field Notes, April 12
-- skills/okr-reporting/changelog.md: entry at v2.3.1 references "KR-4 baseline update" but no such file was touched this session
-- root changelog.md: missing pointer for handoff/2026-04-11-p1-q2-platform-planning-okrs.md (marked complete Apr 11)
-- version sequence clean across all other subdirectories
```

**Vault Auditor** — structured report with check numbers and flags, clinical and precise. Matches the existing `report-template.md` format already defined in `skills/knowledge/`.

**Robert** — spare, philosophical. Short observation on whether the Creed held today. If nothing drifted, silence. If something drifted, a single measured paragraph.

**Roz** — short access log, outliers only. No narrative, no summary. Timestamp, system, anomaly. Example:

```
ROZ — 2026-04-12 02:14
[02:14:03] Asana: project 1213496879668016 missing "JIRA Link" field value — expected on all Platform projects
[02:14:07] Confluence: page 4424073222 returned stale cache (last modified 3d ago, no edits expected) — informational
[02:14:11] Jira: CBP-3075 status "Done" but linked Asana task stage still "In QA" — possible sync gap
END
```

**General rules for the show:**
- Each agent's segment is self-contained — reads cleanly even without the others
- Agents with nothing to flag do not appear (silence = clean)
- The report closes with a "Tomorrow" section listing any items requiring human user's attention, numbered by priority

### What dream cycles are NOT
- No external system writes (no Asana, Jira, or Confluence)
- No autonomous vault changes
- Flag and surface only — human user or desktop Claude acts the next day

### Agents excluded from the nightly cycle
- **Rovo** — requires Atlassian connectivity, runs on demand only
- **Skill-builder** — runs on demand when skills are being authored
- **Strategic PM** — ephemeral session tool, not a cycle participant (only its cleanup check runs)

### Stretch goals for future cycles
- A synthesis phase where an LLM reviews the day's handoff completions and updates a rolling knowledge summary
- Cross-referencing open Jira P1s against vault flags to surface patterns
- A morning briefing file human user can open with his coffee

---

## Task 3: Implement the Orchestrator

Once human user approves the design:

1. Create `skills/dream/` with:
   - `index.md` — purpose, participating agents, cycle phases, show format spec
   - `run.py` — orchestrator that calls each agent phase in sequence
   - `reports/` — output directory for nightly reports
   - `changelog.md`

2. The orchestrator must:
   - Accept `--dry-run` (runs all checks, writes no output)
   - Log each phase start/end time and exit status
   - Catch failures per-phase — one agent failing does not abort the cycle
   - Write the dream report even if some phases fail (with failure noted in that agent's segment)
   - Skip silent agents (nothing to report) cleanly from the output

3. Integrate with launchd for nightly scheduling. Extend or create a `.plist` based on what exists at `project-status-reports/logs/launchd.log`.

---

## Task 4: Create `character.md` for Each Participating Agent

This is a new convention being introduced with dream cycles. Every meta-agent that participates in the dream report needs a `character.md` file in their skill directory. The file defines their voice, persona, and the exact format they use in the dream report.

Create `character.md` for:
- **Robert** — `skills/synthesis/character.md`
- **Changelog Auditor** — `skills/changelog/character.md`
- **Vault Auditor** — `skills/knowledge/character.md`
- **Roz** — `skills/access/character.md` (created as part of the Roz handoff, verify it exists)

Each `character.md` must include:
- Name and role (one line)
- Voice description (2-3 sentences: tone, register, style)
- Dream cycle segment format (the exact template they use)
- A sample segment entry

This file is the authoritative reference for how each agent sounds. The dream report orchestrator uses it when generating each segment.

---

## Task 5: Register Participating Meta-Agents

For each agent in the cycle:
- Confirm their procedure file is runnable autonomously (no interactive input required)
- Confirm their output format matches their `character.md`
- Update their `index.md` with a dream cycle participation note (phase number, role)

---

## Task 6: Dry Run

1. Run `python3 skills/dream/run.py --dry-run` — verify all phases complete cleanly
2. Run a full cycle — review the output report as human user would see it in the morning
3. Confirm the show format reads correctly and each agent's voice is distinct

---

## Task 7: Changelog + Completion

Write changelog entries for all new and modified files. Mark complete and move to `handoff/complete/`.

---

## Notes for This Agent

- Design-first. No code until human user approves the Task 2 architecture proposal.
- Roz must be defined (see `handoff/2026-04-12-p1-roz-agent-definition.md`) before finalizing the agent roster here.
- Product skill consolidation should complete before dream cycles are finalized — dream cycles will reference the new `product/` paths.
- The `character.md` convention is new. When creating files for existing agents, read their existing `index.md` and any prior reports to infer their voice accurately before writing. Do not invent a voice that contradicts what's already established.
- Dream cycles are local-first. No design that requires cloud connectivity to run.
- Priority is P1 because this becomes the nightly heartbeat — but quality matters more than speed. The show format must feel intentional, not procedural.
