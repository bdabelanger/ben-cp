# SOP: Status Report Orchestrator

## Goal
Manage the multi-step relay for the Platform Weekly Status report using the `project-status-reports/manifest.json` as the state-of-record.

## Core Logic
1. **Always Read Manifest First:** Before starting any step, read `project-status-reports/manifest.json` to check `status` and `last_run`.
2. **Step 1 (Ingest):** - REQUIREMENT: `data/raw/asana_all_projects.json` must exist.
   - ACTION: Run `python3 project-status-reports/scripts/step_1_asana_platform_filter.py`.
   - SUCCESS: `data/processed/asana_active.json` is created. Update manifest `status` to "complete".
3. **Step 2 (Harvest):**
   - REQUIREMENT: Step 1 is "complete".
   - ACTION: Batch Jira JQL queries (5 parents at a time) based on keys in `asana_active.json`.
   - SUCCESS: `data/processed/jira_issues.json` is created.

## Error Handling
If a Python script fails, read the terminal output using the shell tool, fix the script if it's a path issue, and retry. Do not move to Step 2 if Step 1 is "pending".