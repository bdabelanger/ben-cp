---
title: Platform Status Report — Skill
type: skill
domain: skills/status
---


# Platform Status Report — Skill

> **Purpose:** Weekly synthesis of project status across Asana and Jira.
> **Preferred Agent:** Cowork (Claude)
> **Cadence:** Weekly (Thursday/Friday)

---

## Overview

The Status Report skill orchestrates the gathering of project health, milestones, and blockers from the Platform engineering team. It merges Asana project data (stages, owners) with Jira issue data (velocity, blockers) into a premium HTML and Markdown report.

---

## Usage

### Step 1 — Run the Pipeline
```bash
# Fresh weekly run (wipes stale Jira cache, resets manifest)
python3 skills/status/run.py --force

# Re-render only (use when Jira data is still fresh)
python3 skills/status/run.py
```
This script will:
1. Fetch latest Asana project stages.
2. Pull Jira issue status for all linked tickets.
3. Synthesize findings into `reports/status/report.md`.

---

## Tooling Layout

- **scripts/**: Pipeline steps (step_0 through step_4) + orchestrator (run.py).
- **tests/**: Unit tests for report generation logic.
- **Data locations**:
    - Live inputs: `skills/inputs/` (raw API responses, processed JSON).
    - Generated reports: `reports/status/` (HTML, logs).

---

## Step 2 — Review and Refine
Agents should read the generated report and use **Atlassian Rovo** (`skills/rovo/`) to add qualitative context for projects marked as "At Risk" or "Off Track."

---

## Connections
- **Input:** Asana Project GIDs, Jira CBP project.
- **Output:** `reports/status/report.md`.
- **Reference:** `intelligence/product/projects/data_sources.md`.

---

## Links
- [Master Runner (run.py)](run.py)
- [Legacy Scripts (scripts/)](scripts/)
- [Schemas (schemas/)](schemas/)
