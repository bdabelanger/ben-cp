# Skill: Dream (Orchestrator)

> **Description:** Nightly report orchestrator for the ben-cp vault. Discover, invoke, and assemble structured skill reports into a curated daily summary.
> **Preferred Agent:** Digest Editor (Unified System Coordinator)
> **Cadence:** Daily

## Connections
- **Input:** All skills in the `skills/` tree (via `report_spec.json`).
- **Output:** `outputs/dream/` (Markdown + HTML) and root `daily-summary.md` (if configured).

## Tool Utility
- **glob**: Used to recursively discover `report_spec.json` files and legacy skill stubs.
- **python_exec**: Orchestrates the Phase 1-4 execution loop.

## Workflow Summary
1. **Discovery:** Identifies participating skills via `report_spec.json` sorts by `run_order`.
2. **Execution:** Runs the Draft, Revision, and Editorial phases.
3. **Assembly:** Compiles edited excerpts into the final daily summary using display framing from `report.md`.

## Constraints
- `run.py` must remain persona-agnostic. All display strings and persona config must come from `report.md`.
- Never auto-fixes vault issues; flags only via participant skill reports.
