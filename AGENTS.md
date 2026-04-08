# AGENTS.md — Vault Agent Dispatch

> **All agents working in this vault must read this file before taking any action.**
> Last updated: 2026-04-08

---

## Who Are You?

Find your role file and read it next:

| Agent | Role file | Role summary |
| :--- | :--- | :--- |
| Claude (Cowork) | `agents/claude.md` | Architect, session lead, skill builder |
| Claude Code | `agents/claude-code.md` | Implementer, code executor, file engineer |
| Gemma | `agents/gemma.md` | Executor, pipeline tasks, data formatting |
| *(future)* Antigravity | `agents/antigravity.md` | TBD |

---

## Vault Structure

```
ben-cp/
├── AGENTS.md                        ← this file — read first, always
├── agents/                          ← role-specific instructions per agent
│   ├── claude.md
│   ├── claude-code.md
│   └── gemma.md
├── gemma-rules.md                   ← Gemma simplified rules (extends agents/gemma.md)
├── reports/                         ← generated Crypt-Keeper reports (never edit manually)
│   └── cleanup-report-YYYY-MM-DD.md
└── skills/                          ← all skill documentation
    ├── skill-builder/
    │   ├── index.md
    │   ├── mappings/
    │   │   └── status_mapping.md
    │   └── styles/
    │       └── emoji_key.md
    ├── okr-reporting/
    │   ├── index.md
    │   ├── procedure.md
    │   ├── data_sources.md
    │   ├── notes_datagrid_shortcuts.md
    │   ├── notes_quick_entry.md
    │   └── [kr-specific].md
    ├── crypt-keeper/
    │   ├── index.md
    │   ├── procedure.md
    │   └── report-template.md
    ├── rovo/
    ├── project-status-reports/
    └── casebook-reporting/
```

---

## Universal Rules (All Agents)

### Read → Write Protocol (MANDATORY)

1. **Before editing an existing file:** read it first with `read_text_file`
2. **Before creating a new file:** list the parent directory to confirm it doesn't exist
3. **For targeted changes:** use `edit_file`, never `write_file` on existing files
4. **`write_file` is for net-new files only** — using it on an existing file is a destructive overwrite
5. **If a read fails:** stop and report — do not proceed with a write

### File Placement

| Content type | Correct location |
| :--- | :--- |
| KR-specific measurement SOP | `skills/okr-reporting/[name].md` |
| Master OKR runbook (evergreen) | `skills/okr-reporting/procedure.md` |
| Quarterly KR reference | `skills/okr-reporting/[year]-[quarter]-kr-reference.md` |
| Data source inventory | `skills/okr-reporting/data_sources.md` |
| Status/transform logic | `skills/skill-builder/mappings/` |
| Visual/emoji standards | `skills/skill-builder/styles/` |
| Crypt-Keeper watchdog | `skills/crypt-keeper/` |
| Other skill SOPs | `skills/[skill-name]/` |
| Cleanup reports | `reports/cleanup-report-[YYYY-MM-DD].md` |

**Never create files at vault root** (except `AGENTS.md`, `gemma-rules.md`).

### File Naming

- Underscores for word separation: `notes_datagrid_shortcuts.md`
- KR SOPs: `[feature]_[metric_type].md`
- Quarterly references: `[year]-[quarter]-kr-reference.md`
- No spaces, no camelCase

### Index Maintenance

After creating or significantly modifying any file, update `index.md` in the same directory.

### Completion Reporting

Every session ends with an explicit summary of files created, modified, and any blockers.

---

## When in Doubt

Ask Ben rather than improvising structure. Do not delete files — flag for review.
