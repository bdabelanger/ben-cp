# Skill: Definition of Done Helper

> **Purpose:** Interviews Ben about a specific task and writes a structured Definition of Done directly back to Asana or Jira.
> **Preferred Agent:** Claude (Cowork)
> **Cadence:** On-demand

---

## Overview

The DoD Helper operates in two modes:

**Single-task mode** — Ben shares a task URL. The skill fetches the task, reads existing content, asks a targeted set of questions based on task type, proposes subtasks for multi-step work, generates a structured DoD, and posts it back.

**Batch mode** — No URL shared. Fetches all of Ben's open Asana tasks and processes each one.

---

## Contents

| File | Description |
| :--- | :--- |
| `index.md` | This file |
| `procedure.md` | Full interview flow, question sets by task type, DoD format, posting behavior |
| `changelog.md` | Change history |

---

## Companion Skills

- [`task-capture`](../task-capture/index.md) — Routes new work items into Asana or Jira
- [`weekly-status`](../weekly-status/index.md) — Platform weekly status report

---

## Source of Truth Note

> **Cowork plugin:** This skill is mirrored in the Cowork runtime plugin (`task-dod-helper/SKILL.md`). Update this vault version first; keep the plugin in sync manually until auto-sync is in place.
