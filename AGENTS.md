# AGENTS.md — Vault Agent Dispatch

> **All agents working in this vault must read this file before taking any action.**
> Last updated: 2026-04-10

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
## Handoff Check (Every Session Start)

Before doing any other work, check for outstanding handoffs:

1. List `handoff/` at vault root (root only — not `handoff/complete/`)
2. Any `.md` file present is an open handoff — completed ones live in `handoff/complete/`
3. Surface them to Ben immediately: "You have N outstanding handoff(s): [filenames]"
4. If Ben confirms, execute using the handoff protocol at `skills/handoff/index.md`

> **Note:** Open handoffs are living documents — they may be edited and iterated before execution. Only completed handoffs (in `handoff/complete/`) are immutable.

Do not proceed with other work until open handoffs are acknowledged by Ben.

---

## Who Are You?

Find your role file and read it next:

| Agent | Role file | Role summary |
| :--- | :--- | :--- |
| Claude (Cowork) | `agents/claude.md` | Architect, session lead, skill builder |
| Claude Code | `agents/claude-code.md` | Implementer, code executor, file engineer |
| Gemma | `agents/gemma.md` | Executor, pipeline tasks, data formatting |
| Antigravity | `agents/antigravity.md` | Peer implementer (Gemini) — full peer to Claude Code; mutual PR review |
| Robert | `agents/robert.md` | Mission Integrity Observer — watches AGENTS.md for Creed drift |

---

## MCP Tools

This vault exposes purpose-built MCP tools. Use them instead of raw file reads/writes where available:

| Tool | Purpose |
| :--- | :--- |
| `get_changelog` | Read changelog entries — pass a scope (`root`, `skills/okr-reporting`, etc.) to pull relevant recent work |
| `write_changelog_entry` | Append a new entry — always write deepest level first, then root |

**Session pattern:**
1. `get_changelog` scoped to the work area → understand recent context
2. Load `AGENTS.md` + your role file → confirm rules
3. Do the work
4. `write_changelog_entry` at subdirectory level → then at root

Ben will tell you which changelog scope is relevant for the session. If not specified, ask before pulling root.

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
├── handoff/                         ← open cross-agent implementation plans (READY)
│   └── complete/                    ← executed handoffs (COMPLETE) — never edit
└── skills/                          ← all skill documentation
    ├── skill-builder/
    │   ├── index.md
    │   ├── mappings/
    │   │   └── status_mapping.md
    │   └── styles/
    │       └── emoji_key.md
    ├── changelog/                   ← changelog skill: procedure + templates
    │   ├── index.md                 ← multi-level changelog procedure
    │   └── entry_template.md
    ├── okr-reporting/
    │   ├── index.md
    │   ├── procedure.md
    │   ├── data_sources.md
    │   └── q2-2026/                       ← initiative-specific quarterly nesting
    │       ├── index.md                   ← Master Q2 Status Dashboard
    │       └── planning-services-at-scale/
    │           ├── index.md
    │           └── [feature]_[metric].md
    ├── crypt-keeper/
    │   ├── SKILL.md
    │   ├── index.md
    │   ├── procedure.md
    │   ├── report-template.md
    │   ├── changelog.md
    │   └── reports/
    │       ├── cleanup-report-YYYY-MM-DD.md
    │       └── archive/
    ├── lumberjack/                  ← changelog auditing (accuracy, completeness, git cross-check)
    │   ├── index.md
    │   ├── procedure.md
    │   └── reports/
    ├── rovo/
    ├── robert/
    │   ├── index.md
    │   ├── diff_checker.md
    │   ├── art.md
    │   └── changelog.md
    ├── project-status-reports/   ← self-contained: runbook + scripts + inputs/outputs/logs
    │   ├── index.md
    │   ├── changelog.md
    │   ├── manifest.json
    │   ├── run_pipeline.sh
    │   ├── scripts/
    │   ├── inputs/
    │   ├── outputs/
    │   ├── logs/
    │   └── tests/
    └── casebook/
        ├── index.md
        ├── changelog.md
        ├── reporting/           ← Reveal BI + entity reference docs
        ├── admin/               ← Casebook Admin MCP skill docs (port 3002)
        └── subscriptions/      ← Casebook Subscriptions MCP skill docs (port 3003)
```

---

## Universal Rules (All Agents)

### Read → Write Protocol (MANDATORY)

1. **Rule of Context:** You MUST read a file with `read_text_file` in the current session before calling `edit_file` or `write_file`.
2. **Rule of Recency:** If your last read of a file was more than 5 tool calls ago, you MUST re-read it to ensure your line numbers and content context are fresh.
3. **Rule of Creation:** Before creating a new file, list the parent directory to confirm it doesn't exist.
4. **Targeted Changes:** Use `edit_file` for targeted changes. NEVER use `write_file` on existing files (it is a destructive overwrite).
5. **Read Failure:** If a read fails, stop and report — do not guess or proceed with a write.

**Mental Check:** Before every edit, state in your `<thought>` block: "Verification: I have read [file] in step [N] of this session."

### Course Correction Protocol

If a required tool call fails (e.g., `write_changelog_entry`, `edit_file`, or path-based MCP tools), follow this priority:
1. **Analyze:** Read the error message carefully.
2. **Correct:** Attempt the obvious fix (e.g., corrected path, alternative tool) once or twice.
3. **Escalate:** If the second attempt fails, escalate to the next higher level (e.g., root-only logging) and note the tool failure clearly for Ben.
4. **Cap:** Never attempt a third time for the same specific failure point.

### File Placement

| Content type | Correct location |
| :--- | :--- |
| KR-specific measurement SOP | `skills/okr-reporting/[quarter]/[initiative]/[name].md` |
| Master OKR runbook (evergreen) | `skills/okr-reporting/procedure.md` |
| Quarterly KR reference | `skills/okr-reporting/[quarter]/index.md` |
| Data source inventory | `skills/okr-reporting/data_sources.md` |
| Status/transform logic | `skills/skill-builder/mappings/` |
| Visual/emoji standards | `skills/skill-builder/styles/` |
| Crypt-Keeper watchdog | `skills/crypt-keeper/` |
| Changelog procedure | `skills/changelog/` |
| Other skill SOPs | `skills/[skill-name]/` |
| Cleanup reports | `skills/crypt-keeper/reports/cleanup-report-[YYYY-MM-DD].md` |

**Never create files at vault root** (except `AGENTS.md`, `changelog.md`, `README.md`).

### File Naming

- Underscores for word separation: `notes_datagrid_shortcuts.md`
- KR SOPs: `[feature]_[metric_type].md`
- Quarterly references: `[year]-[quarter]-kr-reference.md`
- No spaces, no camelCase
- `SKILL.md` and `AGENTS.md` are exempt from the underscore convention — all-caps
  filenames are valid for vault contracts and Cowork skill descriptors

### Index Maintenance

After creating or significantly modifying any file, update `index.md` in the same directory. If the directory has an `art.md`, Robert may add to it — but no other agent should write to `art.md` without Ben's direction.

### Completion Reporting

Every session that involves writing, editing, or structural modification must end with a changelog entry — use `write_changelog_entry` or follow `skills/changelog/index.md`. Read-only or discovery sessions do not require a changelog unless a significant insight or blocker was identified.

**Resilience Rule:** For "meta-observations" (observations about the vault, tools, or procedures) or when subdirectory logging is persistently blocked by tool errors, root-only reporting is acceptable. Provide a full explanation of any blocked subdirectory logs in the root entry.

---

## When in Doubt

Ask Ben rather than improvising structure. Do not delete files — flag for review.
