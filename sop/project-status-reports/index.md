# ⚠️ PROTOCOL OVERRIDE
If the user says "Gemma, let's generate the Platform Weekly Status Report for today", you **MUST NOT** use `read_text_file` on any file outside of this directory. You **MUST NOT** use `searchAtlassian` or `fetchAtlassian`.

**DIRECTIVE**: Proceed immediately to call `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/full_run.py` via the shell tool.

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
3. **Synthesis** (Read ONLY the terminal output of the execution script)
4. **Finalize**

## 🔄 Core Logic

### 1. The Clean Start (New Run Only)
* **Action:** Run the full pipeline script: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/full_run.py`
* **Result:** This script handles all internal logic, filtering, and cross-referencing.

### 2. Context-Light Synthesis
* **Instruction:** The STDOUT from `full_run.py` (specifically the output of Step 4) is your **ONLY** source of truth. 
* **Action:** If the terminal prints `--- REPORT START ---`, copy everything until `--- REPORT END ---`. 
* **Constraint:** Do **NOT** "verify" the report by opening files or searching Jira. Do **NOT** add analysis. Just deliver the artifact.

## ⚠️ Error Handling
* **Permission Errors:** Verify you are inside the allowed root: `/Users/benbelanger/GitHub/ben-cp/`.
* **Path Traversal:** Use the `ben-cp` tool for reading SOPs to ensure security-cleared access.
* **Script Debugging:** If the terminal shows a Python Traceback, read the script file, correct the logic via `write_file`, and re-run.