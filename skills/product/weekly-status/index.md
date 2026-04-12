# Skill: Weekly Status Report

> **Purpose:** Generates the Platform weekly status report from Asana project data and linked Jira child issues.
> **Preferred Agent:** Claude (Cowork)
> **Cadence:** Weekly

---

## Overview

Fetches all Platform team Asana projects, pulls child Jira issues per linked CBP epic, and renders a structured report with data quality metrics, per-project cards, and a PM-written narrative summary.

Supports two modes:
- **Single-project mode** — Ben shares an Asana project URL; report scopes to that project only
- **Batch mode** — No URL; fetches all ~79 Platform projects and generates the full weekly report

---

## Contents

| File | Description |
| :--- | :--- |
| `index.md` | This file |
| `procedure.md` | Full step-by-step execution spec (data fetch, bucketing, card format, report structure) |
| `changelog.md` | Change history |

---

## Companion Skills

- [`task-capture`](../task-capture/index.md) — Routes new work items into Asana or Jira
- [`dod-helper`](../dod-helper/index.md) — Writes Definitions of Done back to tasks

---

## Key Config

| Item | Value |
| :--- | :--- |
| Asana workspace GID | `1123317448830974` |
| Jira cloud ID | `casecommons.atlassian.net` |
| Platform Team field GID | `1208820967756795` |
| Platform Team enum GID | `1208820967756799` |

---

## Source of Truth Note

> **Cowork plugin:** This skill is mirrored in the Cowork runtime plugin (`weekly-status-update/SKILL.md`). Update this vault version first; keep the plugin in sync manually until auto-sync is in place.
