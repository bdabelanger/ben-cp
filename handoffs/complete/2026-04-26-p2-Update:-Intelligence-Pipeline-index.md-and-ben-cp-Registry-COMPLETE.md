---
title: "Update: Intelligence Pipeline index.md and ben-cp Registry After Harvest Refactor"
priority: P2
status: open
assigned_to: Code
created: 2026-04-26
depends_on: 2026-04-26-p1-Refactor:-Shared-Asana-Pipeline-+-Intelligence-Harvest.md
---

# Update: Intelligence Pipeline index.md and ben-cp Registry After Harvest Refactor

## Context

After the P1 handoff (shared Asana pipeline + intelligence harvest) is complete, the following documentation and tool registry updates are needed.

## Step 1 — Update `orchestration/pipelines/intelligence/index.md`

Revise the pipeline stages table to reflect the new `01_harvest.py` step and updated run signatures. Ensure the data flow diagram includes the Asana cache as an input.

## Step 2 — Update `orchestration/pipelines/asana/index.md`

Write a new `index.md` for the asana pipeline (same treatment as `projects` and `intelligence`):
- What it produces
- Pipeline stages table
- Data flow
- How to run
- Accessing via ben-cp (`get_report("asana")`)

## Step 3 — Add `asana` to ben-cp report registry

In `src/ben-cp.ts`, add `asana` to both `list_reports` and `get_report` registries:

```typescript
{
  name: "asana",
  file: "reports/asana/processed/platform_projects.json",
  description: "Shared Asana data cache. Fetches all active Asana projects and tasks once; downstream pipelines (projects, intelligence) read from this cache. Processed views: platform_projects.json, intelligence_queue.json.",
  pipeline: "orchestration/pipelines/asana/scripts/run.py",
  index: "orchestration/pipelines/asana/index.md"
}
```

## Step 4 — Rebuild ben-cp

```bash
cd /Users/benbelanger/Desktop/ben-cp && npm run build
```

## Verification

- [ ] `list_reports` returns `asana` entry with description
- [ ] `get_report("asana")` returns data + pipeline_context
- [ ] `orchestration/pipelines/asana/index.md` exists and is complete
- [ ] `orchestration/pipelines/intelligence/index.md` reflects new harvest step
