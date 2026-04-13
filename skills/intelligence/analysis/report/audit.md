# Audit Procedure: Dream (Orchestration)

> **Owner:** Unified System Coordinator

## Requirements
- [ ] Every active skill must have a valid `report_spec.json`.
- [ ] No hardcoded character names or display strings in `run.py`.
- [ ] Output directory `outputs/dream/` must be git-ignored except for the latest digest.
- [ ] Archive rotation must be verified (reports > 7 days moved to sub-archives).

## Operating Procedure

### Pre-Flight
1. Scan all `skills/` subdirectories for `report_spec.json`.
2. Verify `report.md` contains a valid `## Report Config` JSON block.
3. Validate `vault.css` path is correct for HTML inlining.

### Step 1 — Discovery & Gating
1. Read all specs and filter by `cadence` (e.g. skip weekly if not Monday).
2. Sort by `run_order`.

### Step 2 — Execution Loop
1. **Draft Phase**: Run each skill's preferred agent.
2. **Revision Phase**: Share the draft pool with each agent for refinement.
3. **Editorial Phase**: Extract excerpts and quotes.

### Step 3 — Publication
1. Write Markdown version to `outputs/dream/`.
2. Inline CSS and write HTML version to `outputs/dream/`.
3. Archive previous day's report.
