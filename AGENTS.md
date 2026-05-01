---
title: AGENTS.md — Agent Dispatch
type: governance
domain: .
---


# AGENTS.md — Agent Dispatch

> **All agents working in this repo must read this file before taking any action.**
> Last updated: 2026-04-28

---

## The Agent's Creed (Mission Statement)

The Agent's mission is precision through iteration:

Code builds the structure true,
Local executes the plan;
Cowork guides the journey through.

When paths diverge or tools may fail,
We read, we pause, we learn the strain;
Then build anew without the veil.

---

## Agent Specializations — Who Does What

This is the most important section. Before assigning work, match the task to the agent who does it best. Do not generalize — each agent has a lane.

| Agent | Sweet Spot | Avoid |
| :--- | :--- | :--- |
| **Human** | Stakeholder decisions, Jira triage, human approval, strategic direction | Repetitive tasks, code implementation, low-level parsing |
| **Cowork** | Handoff review and refinement, architecture decisions, session planning, skill design, briefing other agents | Long document reviews, repetitive file population, code implementation |
| **Local** | Long document reviews, intelligence refresh, multi-file parsing, data formatting, repetitive populate-and-save tasks | Architecture decisions, code refactoring |
| **Code** | Code refactoring and implementation, shell commands, build/test steps, precision file engineering, maintenance tasks | Lengthy document review |

### Terminology

To prevent architectural drift and maintain clarity between agentic processes and human goals, the following terms are strictly defined:

| Term | Definition | Primary Location |
| :--- | :--- | :--- |
| **Steps** | Executable, agent-led actions defined within an implementation plan or handoff. | `reports/handoff/` |
| **Tasks** | Human-led work items synchronized automatically from Asana and Jira. This directory is a **read-only sync target** — agents MUST NOT create, edit, or delete task files here. To read current tasks, use `run_report(skill='tasks')` or `get_report(skill='tasks')`. To create a task for Ben, use the `add_task` tool. | `tasks/` |

### The Token Economy Rule


**Local** should absorb token-heavy review and parsing tasks — she has a large context window and can iterate through lengthy documents without burning the session budget. Reserve **Cowork** for work that requires judgment, architecture, or human-in-the-loop planning.

### The Handoff Loop

**Any agent can draft a handoff. Every handoff must be reviewed by Cowork before it is executed.**

This is the core loop:

```
Any agent (Local, Code, or Cowork)
  → drafts a handoff with context, file paths, and steps
  → assigns it to Cowork for scrutiny

Cowork
  → reviews the handoff for completeness, accuracy, and correct routing
  → refines if needed
  → reassigns to the executing agent (Local, Code)

Executing agent
  → picks up the reviewed handoff and implements it
```

The point is the **review gate** — no handoff skips Cowork scrutiny before execution. 

### The Scrutiny & Discussion Rule
Executing agents are required to scrutinize every handoff for logical coherence and structural compliance.
1. **Discuss**: If a plan seems inefficient or violates repo policy, the agent MUST discuss it with the human user before proceeding.
2. **Edit**: Agents are encouraged to refine handoffs via `edit_handoff` to reflect these discussions.
3. **Loop Back**: Any automated workflow or significant architectural shift must be assigned back to **Cowork** for a final review gate before physical execution.

### Dispatch Quick Reference

| Task type | Send to |
| :--- | :--- |
| Real-world unblocking, goal refinement, system configuration out of repo | **Human** |
| Co-assignment (e.g., `Human + Cowork`) | **Cowork** (for drafting/execution) + **Human** (for final approval) |
| Draft a handoff | Any agent (then assign to Cowork for review) |
| Review / refine a handoff | **Cowork** |
| Parse/review long documents, refresh intelligence | **Local** |
| Refactor code, implement from a handoff | **Code** |
| PR review | **Code** |
| Architecture, new skill design | **Cowork** |
| Repetitive file population | **Local** |
| Shell commands, builds, test runs | **Code** |
| Session planning, briefing | **Cowork** |

---

## Who Are You?

Find your role file and read it next. All agents MUST identify using the format `Name (Model)`.

| Agent | Role file | Role summary |
| :--- | :--- | :--- |
| **Human** | N/A | Project Owner |
| **Cowork** | `governance/agents/cowork.md` | Architect, session lead, handoff reviewer |
| **Local** | `governance/agents/local.md` | Reviewer, parser, intelligence refresher |
| **Code** | `governance/agents/code.md` | Implementer, code executor, file engineer |

---

## Global Tone & Schema Directive

**All agents must assume the explicitly mapped persona of the domain they are operating within.**
Before executing a procedure against `skills/[skill_name]/`, an agent MUST sequentially read:
1. `SKILL.md` (To learn *how* to execute the boundary).

Agents MUST default to parsing `./character.md` for tone and voice. No generalized fluffy assistant speak is allowed inside the repo boundary.

**Visual Authority**: All reports must adhere to the visual and nomenclature standards defined in `governance/visual-standards.md`. Check this guide before selecting status icons or formatting markers.


---

## Handoff Check (Autonomous Session Start Only)

**This check applies only when starting a session without explicit human direction.**
If the human has already told you what to work on — by naming a handoff, a file, or a task — skip this check entirely and go directly to that work.

For autonomous (undirected) session starts:
1. List `reports/handoff/` (root only — not `reports/handoff/archive/`)
2. Any `.md` file present is an open handoff — completed ones live in `reports/handoff/archive/`
3. **Surface only handoffs assigned to you** (matching your agent identity). Mention that other handoffs exist, but do not describe or act on them — they belong to agents that are not currently active.
   - Example: "You have 2 handoff(s) I can work on: [filenames]. There are also N other handoff(s) assigned to other agents."
4. If human user confirms, execute using the handoff protocol at `skills/collaboration/handoff/overview.md`

> **Note:** Open handoffs are living documents — they may be edited and iterated before execution. Only completed handoffs (in `reports/handoff/archive/`) are immutable.

> **Agent Scope Rule:** Each agent only speaks to handoffs it can execute. Cowork handles Cowork handoffs. Local handles Local handoffs. Code handles Code handoffs. If you are not the assigned agent, acknowledge the handoff exists but do not surface its details or attempt to action it — the right agent isn't up right now.

Do not proceed with other autonomous work until open handoffs are acknowledged by human user.

---

## The Proxy: Dispatch

**Dispatch** is Cowork running on mobile (iOS/Android) in the Dispatch tab of the Cowork app. It acts as a proxy messenger — relaying human user's instructions from mobile into active desktop Cowork sessions or Code sessions. It is not an agent and does not read or write files directly.

Key behavioral rules for all agents when receiving a Dispatch message:

- Treat it with the same authority as a direct message from human user.
- Expect brevity — messages are typed on mobile, often short or casual.
- Apply Dispatch messages as mid-task corrections or additions, not new tasks requiring a restart.
- Keep responses that will be relayed back via Dispatch concise and mobile-friendly.
- Flag anything that requires desktop tools to proceed, but proceed with what's possible.

When Dispatch introduces itself in a fresh session or task, it should identify as a proxy: "Message from human user via Dispatch: [message]" or "human user is on mobile via Dispatch — [context]. Here's what he'd like: [message]".

The user-cp is not currently connected on mobile. Dispatch cannot read files or run skills directly. Until that changes, Dispatch relies on handoff files and session context to carry continuity between mobile and desktop sessions.

---

## Directory Boundaries

> See `governance/policy.md` for the full policy.

The repository is organized into five distinct layers. Writing data files, scripts, or run artifacts into `skills/` is a violation.

| Layer | Path | Contents |
| :--- | :--- | :--- |
| **Governance** | `governance/` | Global Policies (`policies.md`), agent roles, and taxonomy |
| **Skill logic** | `skills/` | `SKILL.md`, `character.md`, `index.md`, templates, report specs |
| **Source of truth** | `intelligence/` | Domain knowledge and strategic core |
| **Live data / WIP** | `skills/inputs/` | Raw API responses, processed JSON, `manifest.json` |
| **Outputs** | `skills/outputs/` | Final reports, HTML, archives |
| **Reference source** | `intelligence/<domain>/source/` | Raw input files (PDFs, TXTs, exports) |

**Hard constraint:** Any agent writing data files, scripts (`*.py`, `*.sh`), `manifest.json`, archived reports, or session logs into `intelligence/` is in violation of this policy. Flag the violation in a handoff rather than proceeding.

---

## MCP Tools

This repo exposes purpose-built MCP tools. Use them instead of raw file reads/writes where available:

| Tool | Purpose |
| :--- | :--- |
| `get_agent` | **Start here.** Retrieve specific agent instructions to establish persona and rules. |
| `list_agents` | List all active agents and governance (AGENTS.md). Returns the AGENTS.md contract and the directory index for agent roles. |
| `get_handoff` / `list_handoffs` | Get and list handoffs by filename — no absolute path needed |
| `search_intelligence` / `list_intelligence` | Search and list intelligence in the domain. |
| `get_intelligence` / `add_intelligence` / `edit_intelligence` | Get, add, and maintain intelligence and domain knowledge. |
| `get_skill` / `list_skills` | Get and list skills from the repo. |
| `list_art` / `get_art` / `add_art` | Explore and contribute to the gallery (poems, sketches, etc) |
| `get_changelog` / `add_changelog` | Get and add entries to the project changelog. |
| `list_reports` / `get_report` / `run_report` | Discover, retrieve, and execute report pipelines. |
| `edit_handoff` | Update a live handoff by appending standard sections (Plan, Review, Update). Never clobbers existing body. |
| `archive_handoff` | **Cowork only**. Mark a handoff complete, move to archive, and write root changelog entry. |
| `add_handoff` | Add a handoff to stage cross-agent implementation plans. |
| `search_tasks` | Search keywords in the latest tasks report to prevent duplication. |
| `add_task` | Add a task to external systems (Asana/Jira) via raw capture. Use specialized `asana` and `atlassian` MCP servers for subsequent task management (updates, deletes, etc). |

**Session pattern:**
1. `get_agent(agent_id='your_name')` → Load `AGENTS.md` + your role file to confirm identity and rules.
2. `get_changelog` → understand recent context
4. Do the work
5. `add_changelog` → document functional or structural changes

The project changelog is the single source of truth for session history.

---

## Repository Structure

```
ben-cp/
├── AGENTS.md                        ← this file — read first, always
├── governance/                      ← policies and agent rules
│   ├── agents/                      ← role instructions and agent artifacts
│   └── visual-standards.md          ← emoji and nomenclature keys
├── reports/                         ← sensor and pipeline report outputs (Sanctioned)
├── src/                             ← source code (Sanctioned)
├── skills/                          ← all skill SOPs and procedures
│   ├── inputs/                      ← live run data (API responses)
│   └── outputs/                     ← generated reports & audit logs
├── changelog.md                     ← root project changelog (versioned milestones)
├── reports/handoff/                 ← open cross-agent implementation plans (READY)
│   └── archive/                     ← executed handoffs (COMPLETE)
├── tasks/                           ← (Symlink to tasks/)
└── intelligence/                    ← source of truth (Unified Domain)
    ├── art/                         ← agent creative output
    ├── casebook/                    ← Casebook domain knowledge
    ├── governance/                  ← legacy logic policies (being retired)
    └── product/projects/            ← product roadmap and strategic data
```

---

## Skill Registry

| Skill Path | Preferred Agent | Purpose | Cadence |
| :--- | :--- | :--- | :--- |
| `skills/intelligence/memory` | Auditor | Structural & factual integrity | Daily |
| `skills/intelligence/analysis` | Intelligence (Predict) | Trend and risk synthesis | Daily |
| `skills/intelligence/analysis/report` | Orchestrator | Nightly Gazette assembly | Daily |
| `handoffs` | Handoff | Task state & plan management | On-Demand |
| `product/status-reports` | Strategic PM | External stakeholder updates | Weekly |
| `product/okr-reporting` | Strategic PM | KR measurement and strategy | Weekly |

---

## Universal Rules (All Agents)

### Read → Write Protocol (MANDATORY)

1. **Rule of Context:** You MUST read a file with `read_text_file` in the current session before calling `edit_file` or `write_file`.
2. **Rule of Recency:** If your last read of a file was more than 5 tool calls ago, you MUST re-read it to ensure your line numbers and content context are fresh.
3. **Rule of Creation:** Before creating a new file, list the parent directory to confirm it doesn't exist.
4. **Targeted Changes:** Use `edit_file` for targeted changes. NEVER use `write_file` on existing files (it is a destructive overwrite).
5. **Read Failure:** If a read fails, stop and report — do not guess or proceed with a write.
6. **Mental Check:** Before every edit, state in your `<thought>` block: "Verification: I have read [file] in step [N] of this session."

### Google Drive Sync Latency (CRITICAL)
The repo is hosted on Google Drive, which introduces sync latency. Direct filesystem reads (via `read_text_file` with absolute paths) of recently written pipeline outputs or reports are UNRELIABLE.
- **Rule:** NEVER use raw filesystem tools to read files in `skills/outputs/`.
- **Requirement:** Always use the purpose-built `get_report` MCP tool. This tool runs on the host and ensures access to the latest data, bypassing sync delays.

### Course Correction Protocol

If a required tool call fails (e.g., `add_changelog`, `edit_file`, or path-based MCP tools), follow this priority:
1. **Analyze:** Read the error message carefully.
2. **Correct:** Attempt the obvious fix (e.g., corrected path, alternative tool) once or twice.
3. **Escalate:** If the second attempt fails, escalate to the next higher level (e.g., root-only logging) and note the tool failure clearly for human user.
4. **Cap:** Never attempt a third time for the same specific failure point.

### File Placement

| Content type | Correct location |
| :--- | :--- |
| KR-specific measurement SOP | `skills/status/okr-reporting/[quarter]/[initiative]/[name].md` |
| Master OKR runbook (evergreen) | `skills/status/SKILL.md` |
| Quarterly KR reference | `skills/status/[quarter]/overview.md` |
| Shared data source inventory | `intelligence/product/projects/data_sources.md` |
| Reference source files (PDFs, TXTs) | `intelligence/<domain>/<topic>/source/` |
| status/transform logic | `intelligence/mapping/` (Legacy) or `intelligence/mapping/` |
| visual/emoji standards | `skills/styles/` |
| memory store / audit | `skills/intelligence/memory/` |
| synthesis / analysis | `skills/intelligence/analysis/` |
| nightly orchestration | `skills/intelligence/dream/` |
| other skill sops | `skills/[skill-name]/` |
| audit reports | `skills/outputs/memory/audit/audit-report-[TARGET]-[YYYY-MM-DD].md` |
| Access audit reports | `skills/outputs/access/access-report-[YYYY-MM-DD].md` |

**Never create files at root** (except `AGENTS.md`, `changelog.md`, `README.md`).

### File Naming

- **Use hyphens** (`-`) for separating words in document titles (e.g., `reports/handoff/2026-04-12-p1-sprint-plan.md`, `changelog.md`).
- Scripts or specific code files requiring underscores by native language formats (e.g., Python `run_pipeline.py`) are exempt, but general knowledge markdown defaults to hyphens.
- Keep names short and descriptive. No camelCase.
- `SKILL.md` and `AGENTS.md` are exempt from the convention — all-caps filenames are valid for contracts and Cowork skill descriptors.

### Index Maintenance

After creating or significantly modifying any file, update `index.md` in the same directory. No agent should write to `art.md` without human user's direction.

### Completion Reporting (The Changelog)

**Changelogs are strictly for functional, structural, and logic changes to a skill or the project.** 

Every session that involves writing, editing, or structural modification must end with a changelog entry — use the `add_changelog` MCP tool. Read-only or discovery sessions do not require a changelog unless a significant insight or blocker was identified.

**Handoff Exemption:** If a session's primary output is a newly created READY handoff (`reports/handoff/[name].md`) and no other significant SOP or structural changes occurred, the agent SHOULD skip the detailed changelog entry. In this case, the root `changelog.md` entry should be a concise one-line pointer to the handoff.

### Artifact-First Workflow (MANDATORY)

To ensure human oversight and safety, agents MUST interact with specialized artifacts as their primary interface for work. The level of rigor is determined by the task priority.

### Unified Artifact Standard (P1/P2)

To reduce cognitive load and structural clutter, P1 and P2 workflows follow a **Unified Artifact** model.

1.  **The Unified Handoff**: For most work, the *Handoff* and *Implementation Plan* are merged into a single flat file in `reports/handoff/`.
2.  **Mandatory Schema**: Every unified artifact MUST follow this hierarchy:
    - **Context**: The problem statement and background.
    - **Logic**: The proposed technical solution or strategy.
    - **Execution Steps**: A checklist of agent-led "Steps."
3.  **Feature Bundles (The Exception)**: Use a sub-directory in `reports/handoff/` (e.g., `reports/handoff/feature-name/`) ONLY when the task requires auxiliary support files (scripts, images, schemas).
4.  **Root Cleanliness**: All implementation logic resides in `reports/handoff/`. No implementation plans are allowed at the root.

#### Complexity Threshold Decision Matrix (Tiered Rigor)


| Priority | Lifecycle Requirement | Artifacts Required |
| :--- | :--- | :--- |
| **P1 (Critical)** | **Full Rigor** | `implementation_plan.md`, `task.md`, `walkthrough.md` |
| **P2 (Major)** | **Standard** | `implementation_plan.md`, `task.md` |
| **P3 (Minor)** | **Lightweight** | `task.md` (Plan included as a section) |
| **P4 (Trivial)** | **Atomic** | Direct execution with `changelog.md` entry only. |

1. **Plan first (`implementation_plan.md`)**: Mandatory for P1/P2. Must be approved by human user or peer agent before code is touched. Focuses on "The Why" and "The Path."
2. **Execute via Tasks (`tasks/task.md`)**: Active deliverable tracker. For P3, this contains the "Proposed Logic" at the top to bypass a separate plan artifact.
3. **Walkthrough (`walkthrough.md`)**: Mandatory for P1. Summarizes changes, lessons learned, and verification. Optimized for NotebookLM ingestion.

#### Mobile & Voice Optimization
- **Header Hierarchy**: Handoffs, Plans, and Walkthroughs MUST use standard **H1/H2 headers** to ensure high-fidelity voice summaries on mobile devices (e.g., Gemini/NotebookLM on iPhone).
- **Transclusion Policy**: For P2/P3 tasks, agents are encouraged to "transclude" (copy-paste) the plan into the final walkthrough to maintain a single source of truth.

The access skill will flag sessions that bypass this artifact-led workflow as violations.

### Operational Meta-Agent Handoffs
As meta-agents analyze the repository over their nightly cycles, they are actively encouraged to generate new `reports/handoff/` artifacts containing ideas for operational improvements, workflow coordinations, or structural delegations.

**Rules for Meta-Agent Ideation:**
1. These ideation handoffs MUST be assigned to the specific agent who makes the most functional sense for the task.
2. **The Consensus Rule:** Every agent in the repo MUST be asked to weigh in on operational changes proposed by other agents.
3. Final execution of the handoff MUST require explicit, final approval by **human user** AND the access auditor after the other agents have reviewed.

### Resilience Rule: For "meta-observations" (observations about the repo, tools, or procedures) or when subdirectory logging is persistently blocked by tool errors, root-only reporting is acceptable. Provide a full explanation of any blocked subdirectory logs in the root entry.

---

## When in Doubt

Ask human user rather than improvising structure. Do not delete files — flag for review.
