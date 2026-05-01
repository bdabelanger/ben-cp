---
title: Minify Asana Projects JSON for Token Economy
priority: P2
assigned_to: Code
status: READY — pick up 2026-05-01
date: 2026-05-01
---

# Implementation Plan: Minify Asana Projects JSON for Token Economy

# Context
The Asana raw project dump (`reports/asana/raw/all_projects.json`) has exceeded **1MB**, triggering the `bloat` sensor. This file is a major token consumer because it is read by multiple agents and pipelines to resolve project IDs and metadata.

# Logic
The goal is to minify the project list while preserving all fields required by the `status` and `intelligence` pipelines.

### Fields to Keep
- **Project Root**: `gid`, `name`, `permalink_url`, `current_status_update`.
- **Custom Fields (by GID)**:
  - `1208820967756795` (Team)
  - `1208822149019495` (Stage)
  - `1211631943113717` (QA Start)
  - `1210467277124544` (UAT Start)
  - `1208818118032458` (Beta Start)
  - `1210909549820601` (GA Month)
  - `1208818124273418` (GA Target)
  - `1208818005809198` (Jira Link)
  - `1211632504010030` (PRD Link)
  - `1211632748689814` (Launch Plan Link)

### Implementation Plan
1.  **Script Upgrade**: Update `skills/asana/scripts/01_fetch_projects.py` to include a `minify` loop after the fetch.
2.  **Field Filtering**: For each project, iterate through `custom_fields` and only retain the whitelist above.
3.  **Sub-object Minification**: Within the retained custom fields, keep only `gid`, `name`, `display_value`, `enum_value`, `date_value`, and `text_value`.
4.  **Verification**: 
    - Ensure the new file size is < 250KB.
    - Run `run_report(skill='status')` to verify GA/Beta dates are still correctly extracted.

# Execution Steps
- [ ] Review `01_fetch_projects.py` current fetch logic.
- [ ] Implement the minification whitelist loop.
- [ ] Run a fresh harvest via `run_report(skill='asana')`.
- [ ] Confirm `bloat` sensor is green for the file.
- [ ] Run `run_report(skill='status')` and check the GA/Beta milestones in the report.
