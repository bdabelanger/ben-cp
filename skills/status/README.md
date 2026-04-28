---
title: tools/status-reports
type: task
domain: skills/status
---


# tools/status-reports

Execution tooling for the Platform Weekly Status Report pipeline. This directory contains the scripts and shell wrapper that *run* the pipeline — the skill SOP (what the pipeline does and how to interpret it) lives in `skills/product/status-reports/index.md`.

## Invoke

```bash
# Fresh weekly run (wipes stale Jira cache, resets manifest)
python3 tools/status-reports/scripts/full_run.py --force

# Re-render only (use when Jira data is still fresh from a prior run)
python3 tools/status-reports/scripts/full_run.py

# Shell wrapper (loads .env, logs to outputs/status-reports/logs/)
./tools/status-reports/run_pipeline.sh --force
```

Run from repo root (`ben-cp/`). Requires `ASANA_API_TOKEN`, `ATLASSIAN_USER_EMAIL`, and `ATLASSIAN_API_TOKEN` in `.env` at repo root.

## Layout

```
scripts/        Pipeline steps (step_0 through step_4) + orchestrator (full_run.py)
tests/          Unit tests for report generation logic
run_pipeline.sh Shell wrapper: loads .env, invokes full_run.py, appends to run log
```

## Data locations

- Live inputs: `inputs/status-reports/` (raw API responses, processed JSON, manifest)
- Generated reports: `outputs/status-reports/` (HTML, logs)
