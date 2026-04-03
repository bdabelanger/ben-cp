# SOP: Status Report Orchestrator (Final)

## Goal
Manage the multi-step relay for the Platform Weekly Status report using `manifest.json` as the state-of-record. This workflow is designed to minimize context-bloat and maximize reliability on local LLMs.

## 🛠️ Tooling Rules (STRICT)
1. **No Manual JSON Edits:** The Orchestrator MUST NOT use `write_file` to edit `manifest.json`. Use the dedicated script instead:
   `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/update_manifest.py [step_id] [status]`
2. **Absolute Pathing:** Every tool call (shell, filesystem, ben-cp) MUST use full absolute paths starting with `/Users/benbelanger/GitHub/ben-cp/`.
3. **Script Maintenance:** If a Python script fails due to logic, use `write_file` to update the script content before retrying the shell command.

## 🔄 Core Logic

### 1. The Clean Start (New Run Only)
* **Action:** Move existing files in `project-status-reports/inputs/processed/` to `project-status-reports/inputs/archive/`.
* **Action:** Run the reset command: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/update_manifest.py reset`
* **Result:** This automatically updates last_run and the Step 3 file path to the current date.

### 2. State Verification
* **Action:** Always read `manifest.json` first. Only execute steps marked `pending`.

### 3. Step 1: Asana Ingest
* **Requirement:** `inputs/raw/asana_all_projects.json` must exist.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_1_asana_platform_filter.py`.
* **Success:** `asana_active.json` is created. Update manifest to `complete`.

### 4. Step 2: Jira Harvest
* **Requirement:** Step 1 status is `complete`.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_2_jira_harvest.py`.
* **Success:** `jira_issues.json` is created. Update manifest to `complete`.

### 5. Step 3: Report Generation
* **Requirement:** Step 2 status is `complete`.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_3_report_generator.py`.
* **Convention:** The script dynamically names the file `Platform_Status_YYYY_MM_DD.md` in the `outputs/` folder.
* **Success:** Update manifest to `complete`.

## ⚠️ Error Handling
* **Permission Errors:** Verify you are inside the allowed root: `/Users/benbelanger/GitHub/ben-cp/`.
* **Path Traversal:** Use the `ben-cp` tool for reading SOPs to ensure security-cleared access.
* **Script Debugging:** If the terminal shows a Python Traceback, read the script file, correct the logic via `write_file`, and re-run.