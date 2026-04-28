---
title: 'Governance: Global Policies'
type: governance
domain: .
---


# Governance: Global Policies

> **Authority:** Human (Ben)
> **Last updated:** 2026-04-28

---

## 1. Directory Boundaries

The repository is organized into five distinct layers. Writing data files, scripts, or run artifacts into `skills/` is a violation.

| Layer | Path | Contents |
| :--- | :--- | :--- |
| **Governance** | `governance/` | Policies, agent role files, and taxonomy |
| **Skill logic** | `skills/` | `SKILL.md`, `character.md`, `index.md`, templates, report specs |
| **Source of truth** | `intelligence/` | Domain knowledge and strategic core |
| **Live data / WIP** | `skills/inputs/` | Raw API responses, processed JSON, `manifest.json` |
| **Outputs** | `skills/outputs/` | Final reports, HTML, archives |

### Sanctioned Write Zones

Agents are permitted to write to the following directories without prior approval, provided the files follow the defined naming conventions:

- `reports/handoff/` (New implementation plans)
- `reports/` (Generated reports)
- `intelligence/` (Updating knowledge records)
- `skills/inputs/` (Live data snapshots)

---

## 2. Retention & Archival

To maintain performance and prevent token inflation, the following retention limits are enforced:

| Category | Retention Period | Action |
| :--- | :--- | :--- |
| **Handoffs (Archive)** | 30 Days | Move to `reports/handoff/archive/` (Done via `edit_handoff`) |
| **Dream Reports** | 7 Days | Automated cleanup |
| **Live Data (Inputs)** | 48 Hours | Overwritten on next run |
| **Session Logs** | 14 Days | Archived to `intelligence/history/` |

---

## 3. Read → Write Protocol

1. **Context First**: You MUST read a file in the current session before calling `edit_file` or `write_file`.
2. **Recency**: If your last read was >5 tool calls ago, re-read.
3. **No Guessing**: If a read fails, stop and report.
4. **Targeted Edits**: Use `edit_file` for precision; avoid `write_file` on existing files.

---

## 4. Documentation Standard

- **Markdown-First**: All documentation must be valid Github Flavored Markdown.
- **Frontmatter**: Every file must contain valid YAML frontmatter (title, type, domain).
- **No Narrative**: Keep documentation staccato and technical. No conversational "fluff."
