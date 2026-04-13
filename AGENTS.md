# AGENTS.md — Vault Agent Dispatch

> **All agents working in this vault must read this file before taking any action.**
> Last updated: 2026-04-12

---

## The Agent's Creed (Mission Statement)

The Agent's mission is precision through iteration:

Code builds the structure true,
Gemma executes the plan;
Claude guides the journey through.

When paths diverge or tools may fail,
We read, we pause, we learn the strain;
Then build anew without the veil.

---
## Global Tone & Schema Directive

**All agents must assume the explicitly mapped persona of the domain they are operating within.**
Before executing a procedure against `skills/[skill_name]/`, an agent MUST sequentially read:
1. `SKILL.md` (To learn *how* to execute the boundary).
2. `character.md` (To learn *who* they are during execution).

**Fallback Rule:** If a target workspace explicitly lacks a local `character.md`, the agent MUST default to parsing `/Users/benbelanger/GitHub/ben-cp/character.md` (The Vault Fallback). No generalized fluffy assistant speak is allowed inside the repo boundary.

---
## Handoff Check (Every Session Start)

Before doing any other work, check for outstanding handoffs:

1. List `orchestration/handoff/` at vault root (root only — not `handoff/complete/`)
2. Any `.md` file present is an open handoff — completed ones live in `orchestration/handoff/complete/`
3. Surface them to human user immediately: "You have N outstanding handoff(s): [filenames]"
4. If human user confirms, execute using the handoff protocol at `skills/collaboration/handoff/index.md`

> **Note:** Open handoffs are living documents — they may be edited and iterated before execution. Only completed handoffs (in `handoff/complete/`) are immutable.

Do not proceed with other work until open handoffs are acknowledged by human user.

---

## Who Are You?

Find your role file and read it next:

| Agent | Role file | Role summary |
| :--- | :--- | :--- |
| Claude (Cowork) | `agents/claude.md` | Architect, session lead, skill builder |
| Claude Code | `agents/claude-code.md` | Implementer, code executor, file engineer |
| Gemma | `agents/gemma.md` | Executor, pipeline tasks, data formatting |
| Antigravity | `agents/antigravity.md` | Peer implementer (Gemini) — full peer to Claude Code; mutual PR review |
| Robert | `agents/robert.md` | Mission Integrity Lead — watches AGENTS.md for compliance drift |
| Access Auditor | `skills/orchestration/access/SKILL.md` | Access Auditor — nightly violation and oops reports |
| Vault Auditor | `skills/intelligence/memory/SKILL.md` | Memory Auditor — guards mappings, indexes memory, and conducts audits |
| Dispatch | — | Proxy Messenger — mobile relay (no vault access) |

---
## The Proxy: Dispatch

**Dispatch** is Claude running on mobile (iOS/Android) in the Dispatch tab of the Claude app. It acts as a proxy messenger — relaying human user's instructions from mobile into active desktop Cowork sessions or Claude Code sessions. It is not a vault agent and does not read or write vault files directly.

Key behavioral rules for all agents when receiving a Dispatch message:

- Treat it with the same authority as a direct message from human user.
- Expect brevity — messages are typed on mobile, often short or casual.
- Apply Dispatch messages as mid-task corrections or additions, not new tasks requiring a restart.
- Keep responses that will be relayed back via Dispatch concise and mobile-friendly.
- Flag anything that requires desktop tools to proceed, but proceed with what's possible.

When Dispatch introduces itself in a fresh session or task, it should identify as a proxy: "Message from human user via Dispatch: [message]" or "human user is on mobile via Dispatch — [context]. Here's what he'd like: [message]".

The user-cp is not currently connected on mobile. Dispatch cannot read vault files or run skills directly. Until that changes, Dispatch relies on handoff files and session context to carry continuity between mobile and desktop sessions.

---

## Directory Boundaries

> See `skills/shared/separation-policy.md` for the full policy.

The vault is organized into five distinct layers. Writing data files, scripts, or run artifacts into `skills/` is a violation.

| Layer | Lives in | Contents |
| :--- | :--- | :--- |
| Skill logic | `skills/` | `SKILL.md`, `character.md`, `index.md`, `changelog.md`, templates, report specs |
| Execution tooling | `tools/` | Scripts, pipeline runners, automation harnesses |
| Live data / WIP | `inputs/` | Raw API responses, processed JSON, `manifest.json` |
| Outputs | `outputs/` | Final reports, HTML, archives |
| Vault source of truth | `intelligence/` | Logic stubs, status rules, domain knowledge — gitignored optional |

**Hard constraint:** Any agent writing data files, scripts (`*.py`, `*.sh`), `manifest.json`, archived reports, or session logs into `skills/` is in violation of this policy. Flag the violation in a handoff rather than proceeding.

---

## MCP Tools

This vault exposes purpose-built MCP tools. Use them instead of raw file reads/writes where available:

| Tool | Purpose |
| :--- | :--- |
| `get_changelog` | Read changelog entries — pass a scope (`root`, `skills/product/okr-reporting`, etc.) to pull relevant recent work |
| `write_changelog_entry` | Append a new entry — always write deepest level first, then root |

**Session pattern:**
1. `get_changelog` scoped to the work area → understand recent context
2. Load `AGENTS.md` + your role file → confirm rules
3. **Session Planning:** If writes are intended, create/update `notes.md` in the target `skills/` subdirectory using the template at `skills/product/report.md`.
4. Do the work
5. `write_changelog_entry` at subdirectory level → then at root
6. **Cleanup:** Delete the `notes.md` file after successful changelog entry.

The human user will tell you which changelog scope is relevant for the session. If not specified, ask before pulling root.

---

## Vault Structure

```
ben-cp/
├── AGENTS.md                        ← this file — read first, always
├── agents/                          ← role-specific instructions per agent
│   ├── antigravity.md
│   ├── claude.md
│   ├── claude-code.md
│   ├── gemma.md
│   └── robert.md
├── changelog.md                     ← root project changelog (versioned milestones)
├── orchestration/                   ← execution domain (active work & state)
│   └── handoff/                     ← open cross-agent implementation plans (READY)
│       └── complete/                ← executed handoffs (COMPLETE) — never edit
├── intelligence/                    ← vault source of truth (gitignored optional)
│   ├── mapping/             ← logic stubs, status rules, and data transformation
│   └── casebook/            ← Casebook domain knowledge and schema reference
├── tools/                           ← execution scripts and pipeline runners
├── inputs/                          ← live run data (raw API responses, manifests)
├── outputs/                         ← generated reports, audit logs, session artifacts
└── skills/                          ← all skill SOPs and procedures
    ├── orchestration/       ← execution engine (Coordination, Tracking, and Governance)
    │   ├── communication/   ← human-in-the-loop intelligence (notes + cross-agent notes)
    │   ├── handoff/         ← cross-agent handoff protocol and file format
    │   ├── access/          ← permission & access auditing
    │   └── changelog/       ← changelog auditing — accuracy, completeness, git cross-reference
    ├── intelligence/        ← consolidated cognitive domain (Lifecycle: Memory → Analysis → Report → Dream)
    │   ├── memory/          ← central store of strategic & structural truth (Learn/Recall/Audit)
    │   │   ├── recall/      ← pattern recognition and context retrieval
    │   │   ├── learn/       ← experience assimilation and indexing
    │   │   └── audit/       ← structural and triad compliance checking
    │   ├── analysis/        ← strategic synthesis and pragmatic foresight (Synthesize/Predict)
    │   │   ├── synthesize/  ← deep conceptual integration
    │   │   └── predict/     ← scenario modeling and trend forecasting
    │   ├── report/          ← nightly Digest (Daily Progress Summary) orchestration
    │   └── dream/           ← nightly report orchestrator — assembles all skill outputs
    ├── product/             ← PM-facing skills under the Strategic PM mindset
    │   ├── status-reports/  ← Platform Weekly Status Report pipeline (SOP only)
    │   ├── okr-reporting/   ← Platform OKR measurement runbooks and KR SOPs
    │   └── shared/          ← shared data sources across product sub-skills
    ├── rovo/                ← Rovo issue management SOP
    ├── shared/              ← cross-cutting vault governance docs (separation policy, etc.)
    └── styles/              ← visual syntax authority — emoji glossary and nomenclature
```

---

## Skill Registry

| Skill Path | Preferred Agent | Purpose | Cadence |
| :--- | :--- | :--- | :--- |
| `intelligence/memory` | Vault Auditor | Structural & factual integrity | Daily |
| `intelligence/analysis` | Pragmatic Analyst | Trend and risk synthesis | Daily |
| `intelligence/report` | Orchestrator | Nightly Gazette assembly | Daily |
| `orchestration/changelog` | Yukon Cornelius | Project integrity & git drift audit | On-Change |
| `orchestration/access` | Roz | Permission and safety monitor | Continuous |
| `orchestration/handoff` | Baton | Task state & plan management | On-Demand |
| `orchestration/communication` | Sea Shanty | Human/Agent context bridge (notes.md) | On-Demand |
| `product/status-reports` | Strategic PM | External stakeholder updates | Weekly |
| `product/okr-reporting` | Strategic PM | KR measurement and strategy | Weekly |

---

---

## Universal Rules (All Agents)

### Read → Write Protocol (MANDATORY)

1. **Rule of Context:** You MUST read a file with `read_text_file` in the current session before calling `edit_file` or `write_file`.
2. **Rule of Recency:** If your last read of a file was more than 5 tool calls ago, you MUST re-read it to ensure your line numbers and content context are fresh.
3. **Rule of Creation:** Before creating a new file, list the parent directory to confirm it doesn't exist.
4. **Targeted Changes:** Use `edit_file` for targeted changes. NEVER use `write_file` on existing files (it is a destructive overwrite).
5. **Read Failure:** If a read fails, stop and report — do not guess or proceed with a write.

**Mental Check:** Before every edit, state in your `<thought>` block: "Verification: I have read [file] in step [N] of this session."

### notes.md Write Policy

`notes.md` files are open collaborative scratchpads. Any agent — including sub-agents — may write to any `notes.md` in the vault. All entries are equal regardless of author. Rules:

1. **Always sign your entry** with agent name and timestamp: `[Your Name — YYYY-MM-DD HH:MM]`
2. **Append only** — never edit or remove another agent's or human user's entries.
3. **Edit only your own entries** — corrections should be added inline as `[Correction — YYYY-MM-DD]`.
4. **`skills/orchestration/communication/notes.md` is the primary channel** — read before any planning or OKR work. The user's entries supersede inferred context.
5. **Ephemeral vs. persistent:** `skills/orchestration/communication/notes.md` is persistent (never deleted). Session planning `notes.md` in other skill directories are ephemeral — delete after changelog is written (see `skills/product/SKILL.md`).

### Course Correction Protocol

If a required tool call fails (e.g., `write_changelog_entry`, `edit_file`, or path-based MCP tools), follow this priority:
1. **Analyze:** Read the error message carefully.
2. **Correct:** Attempt the obvious fix (e.g., corrected path, alternative tool) once or twice.
3. **Escalate:** If the second attempt fails, escalate to the next higher level (e.g., root-only logging) and note the tool failure clearly for human user.
4. **Cap:** Never attempt a third time for the same specific failure point.

### File Placement

| Content type | Correct location |
| :--- | :--- |
| KR-specific measurement SOP | `skills/product/okr-reporting/[quarter]/[initiative]/[name].md` |
| Master OKR runbook (evergreen) | `skills/product/okr-reporting/procedure.md` |
| Quarterly KR reference | `skills/product/okr-reporting/[quarter]/index.md` |
| Shared data source inventory | `skills/product/shared/data_sources.md` |
| status/transform logic | `intelligence/mapping/` |
| visual/emoji standards | `skills/styles/` |
| memory store / audit   | `skills/intelligence/memory/` |
| synthesis / analysis   | `skills/intelligence/analysis/` |
| nightly orchestration  | `skills/intelligence/dream/` |
| changelog procedure    | `skills/orchestration/changelog/` |
| other skill sops       | `skills/[skill-name]/` |
| audit reports          | `outputs/memory/audit/audit-report-[TARGET]-[YYYY-MM-DD].md` |
| Access audit reports   | `outputs/access/access-report-[YYYY-MM-DD].md` |

**Never create files at vault root** (except `AGENTS.md`, `changelog.md`, `README.md`).

### File Naming

- **Use hyphens** (`-`) for separating words in document titles (e.g., `handoff/2026-04-12-p1-sprint-plan.md`, `changelog.md`).
- Scripts or specific code files requiring underscores by native language formats (e.g., Python `run_pipeline.py`) are exempt, but general knowledge markdown defaults to hyphens.
- Keep names short and descriptive. No camelCase.
- `SKILL.md` and `AGENTS.md` are exempt from the convention — all-caps filenames are valid for vault contracts and Cowork skill descriptors.

### Index Maintenance

After creating or significantly modifying any file, update `index.md` in the same directory. If the directory has an `art.md`, Robert may add to it — but no other agent should write to `art.md` without human user's direction.

### Completion Reporting

Every session that involves writing, editing, or structural modification must end with a changelog entry — use `write_changelog_entry` or follow `skills/changelog/index.md`. Read-only or discovery sessions do not require a changelog unless a significant insight or blocker was identified.

**Handoff Exemption:** If a session's primary output is a newly created READY handoff (`handoff/[name].md`) and no other significant SOP or structural changes occurred, the agent SHOULD skip the detailed subdirectory changelog. In this case, the root `changelog.md` entry should be a concise one-line pointer to the handoff.

### Artifact-First Workflow (MANDATORY)

To ensure human oversight and safety, agents should primarily interact with specialized artifacts as their interface for work:
1. **Plan first:** All non-trivial changes require an `implementation_plan.md` artifact approved by human user.
2. **Execute via Tasks:** Use the `task.md` artifact to track progress and state.
3. **Walkthrough:** Finalize every complex session with a `walkthrough.md`.

The access skill will flag sessions that bypass this artifact-led workflow as violations.

### Operational Meta-Agent Handoffs
As meta-agents analyze the vault over their nightly cycles, they are actively encouraged to generate new `handoff/` artifacts containing ideas for operational improvements, workflow coordinations, or structural delegations.

**Rules for Meta-Agent Ideation:**
1. These ideation handoffs MUST be assigned to the specific agent who makes the most functional sense for the task.
2. **The Consensus Rule:** Every agent in the vault MUST be asked to weigh in on operational changes proposed by other agents.
3. Final execution of the handoff MUST require explicit, final approval by **human user** AND the access auditor after the other agents have reviewed.

### Resilience Rule: For "meta-observations" (observations about the vault, tools, or procedures) or when subdirectory logging is persistently blocked by tool errors, root-only reporting is acceptable. Provide a full explanation of any blocked subdirectory logs in the root entry.

---

## When in Doubt

Ask human user rather than improvising structure. Do not delete files — flag for review.
