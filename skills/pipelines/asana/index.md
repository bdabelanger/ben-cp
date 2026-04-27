---
title: Asana Pipeline
type: index
domain: skills/pipelines/asana
---

# Asana Pipeline

## Purpose
Fetches raw data from Asana and produces shared data caches for downstream pipelines (`projects`, `intelligence`).

## Outputs
- `reports/asana/raw/all_projects.json` (all active projects)
- `reports/asana/raw/all_tasks.json` (Ben's tasks)
- `reports/asana/processed/platform_projects.json` (filtered)
- `reports/asana/processed/intelligence_queue.json` (filtered)

## Pipeline Stages
| # | Script | Mode | What it does |
|---|--------|------|--------------|
| 01 | `01_fetch_projects.py` | Automated | Fetches all active projects from Casebook workspace |
| 02 | `02_fetch_tasks.py` | Automated | Fetches tasks assigned to Ben |
| 03 | `03_normalize.py` | Automated | Derives filtered views from raw cache |

## Data Flow
`Asana API` -> `raw/all_projects.json` -> `processed/platform_projects.json`

## How to run
```bash
python3 skills/pipelines/asana/scripts/run.py
```

## Access via ben-cp
Available in the TS SDK via:
```typescript
import { get_report } from 'ben-cp';
const data = get_report("asana");
```
