# Trigger: "Generate Platform Weekly Status Report"
When this phrase is used, the agent must:
1. Run `update_manifest.py reset`.
2. Execute Steps 1 through 4 sequentially.
3. Adhere to "Strict Tooling Rules" below.

# SOP: Status Report Orchestrator (Final)

## Goal
Manage the multi-step relay for the Platform Weekly Status report using `manifest.json` as the state-of-record. This workflow is designed to minimize context-bloat and maximize reliability on local LLMs.

## 🛠️ Tooling Rules (STRICT)
1. **No Manual JSON Edits:** The Orchestrator MUST NOT use `write_file` to edit `manifest.json`. Use the dedicated script instead:
   `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/update_manifest.py [step_id] [status]`
2. **Absolute Pathing:** Every tool call (shell, filesystem, ben-cp) MUST use full absolute paths starting with `/Users/benbelanger/GitHub/ben-cp/`.
3. **Script Maintenance:** If a Python script fails due to logic, use `write_file` to update the script content before retrying the shell command.
4. **STRICT LAZY LOADING:** Do not read processed JSON files until the final Synthesis step (Step 4).
5. **SCRIPT-CENTRIC:** Trust the shell tool output. If a script prints '✅ Complete', do not verify it by reading the file content. Move immediately to the next shell command.
6. **FIELD RESTRICTION:** The 'file' paths in `manifest.json` are pointers for Python scripts, not for the AI Agent. Reading these paths via ben-cp is a context-waste violation.

### ⚡ Execution Macro
When triggered, follow this exact sequence:
1. **Reset Manifest**
2. **Run Meta-Scripts** (Steps 1 through 3, checking status in terminal only)
3. **Synthesis** (Read ONLY the specific output files for Step 4, if needed)
4. **Finalize**

## 🔄 Core Logic

### 1. The Clean Start (New Run Only)
* **Action:** Move existing files in `project-status-reports/inputs/processed/` to `project-status-reports/inputs/archive/`.
* **Action:** Run the reset command: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/update_manifest.py reset`
* **Result:** This automatically updates last_run and the Step files to the current date.

### 2. State Verification
* **Action:** Always read `manifest.json` first. Only execute steps marked `pending`.

### 3. Step 1: Asana Ingest
* **Requirement:** `inputs/raw/asana_all_projects.json` must exist.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_1_asana_platform_filter.py`.
* **Success:** `asana_active.json` is created. Update manifest to `complete`.

### 4. Step 2: Rovo Context
* **Requirement:** Step 1 status is `complete`.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_2_rovo_context.py`.
* **Success:** `rovo_insights.json` is created. Update manifest to `complete`.

### 5. Step 3: Jira Harvest
* **Requirement:** Step 1 status is `complete`.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_3_jira_harvest.py`.
* **Success:** `jira_issues.json` is created. Update manifest to `complete`.

### 6. Step 4: Report Generation
* **Requirement:** Steps 1, 2, and 3 statuses are `complete`.
* **Action:** Run `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_4_report_generator.py`.
* **Convention:** The script dynamically names the file `Platform_Status_YYYY_MM_DD.md` in the `outputs/` folder.
* **Success:** Update manifest to `complete`. The script will output the full report wrapped in `--- REPORT START ---` and `--- REPORT END ---` tags. Your only task is to copy the content between these tags. Do not use filesystem tools to read the .md file.

## ⚠️ Error Handling
* **Permission Errors:** Verify you are inside the allowed root: `/Users/benbelanger/GitHub/ben-cp/`.
* **Path Traversal:** Use the `ben-cp` tool for reading SOPs to ensure security-cleared access.
* **Script Debugging:** If the terminal shows a Python Traceback, read the script file, correct the logic via `write_file`, and re-run.