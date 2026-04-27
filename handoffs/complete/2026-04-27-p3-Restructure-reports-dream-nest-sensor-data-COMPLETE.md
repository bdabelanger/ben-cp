---
title: "Restructure reports/dream: Nest sensor JSONs under data/"
type: handoff
priority: P3
status: 🔲 READY
date: 2026-04-27
assigned_to: Code
---

# Restructure reports/dream: Nest sensor JSONs under data/

## Context

`reports/dream/` currently mixes sensor output files (JSON), a pipeline changelog, and the final report at the same level. Every other report skill (`status`, `tasks`, `asana`) now follows a consistent pattern:

```
reports/<skill>/
  report.md         ← final output, stays at root
  data/
    raw/            ← sensor JSON output files
    processed/      ← (optional) derived data
    archive/        ← previous run snapshots
    manifest.json   ← pipeline state tracker
    README.md       ← layout docs
```

`reports/dream/` should match this pattern.

## Current State

```
reports/dream/
  access_report.json
  agents_report.json
  changelog.md          ← pipeline-internal changelog (not vault changelog)
  changelog_report.json
  context_report.json
  dream_run.json
  drift_report.json
  frontmatter_report.json
  handoffs_report.json
  index_report.json
  links_report.json
  pulse_report.json
  tasks_report.json
  report.md             ← keep here
  archive/              ← keep here
```

Sensor scripts live in `skills/dream/sensors/` and write directly to `reports/dream/`. The orchestrator is `skills/dream/run.py`.

## Logic

Move all `*_report.json`, `dream_run.json`, and `changelog.md` into `reports/dream/data/raw/`. Keep `report.md` and `archive/` at the `reports/dream/` root. Add `manifest.json` and `README.md` to `reports/dream/data/`.

Update all sensor scripts and `run.py` to write to the new `data/raw/` path. Also check `src/ben-cp.ts` for any MCP registry entries referencing `reports/dream/*.json`.

## Execution Steps

- [ ] 1. Create `reports/dream/data/raw/`, `reports/dream/data/processed/`, `reports/dream/data/archive/`
- [ ] 2. Move all `*_report.json`, `dream_run.json`, and `changelog.md` into `reports/dream/data/raw/`
- [ ] 3. Grep `skills/dream/sensors/*.py` and `skills/dream/run.py` for `reports/dream/` write paths — update each to `reports/dream/data/raw/`
- [ ] 4. Grep `src/ben-cp.ts` for `reports/dream/` references — update any stale MCP registry paths
- [ ] 5. Write `reports/dream/data/manifest.json` — one step entry per sensor (access, agents, changelog, context, drift, frontmatter, handoffs, index, links, pulse, tasks) — model after `reports/status/data/manifest.json`
- [ ] 6. Write `reports/dream/data/README.md` — model after `reports/tasks/data/README.md`
- [ ] 7. Syntax-check: `python3 -c "import ast; ast.parse(open('skills/dream/run.py').read()); print('OK')"`
- [ ] 8. Add changelog entry to `skills/changelog.md`

## Verification

- `reports/dream/report.md` and `reports/dream/archive/` remain at root
- `reports/dream/data/raw/` contains all sensor JSONs and `dream_run.json`
- No sensor script or `run.py` still references `reports/dream/*.json` at root level
- `manifest.json` and `README.md` present in `reports/dream/data/`
- `src/ben-cp.ts` has no stale `reports/dream/` paths
