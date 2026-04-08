# Data Sources Inventory: OKR Reporting Skill

> [!NOTE]
> ⚠️ **PROCESS TYPE:** Manual Workflow (Not API Driven)
> This document inventories all required inputs for the OKR reporting process. Since this is a manual workflow, 'Data Source' refers to the location or method of data acquisition.

---

## 📥 Required Inputs

The following items must be gathered before beginning the report generation:

### 1. Core OKR Data Set
*   **Source:** [Manual Collection / Specific Tool Export]
*   **Description:** The raw data containing all active Objectives and Key Results.
*   **Required Fields:** Objective Name, Target Metric, Current Value, Target Value, Reporting Period Start/End Date.
*   **Acquisition Method:** *[To be filled: e.g., Export from OKR Platform via CSV]*

### 2. Project Status Data (Contextual)
*   **Source:** [Manual Review / Jira Board]
*   **Description:** Contextual data on the projects tied to these OKRs, including current stage and completion status.
*   **Required Fields:** Project Name, Current Stage (e.g., Development, QA), Completion Status (Done/In Progress).
*   **Acquisition Method:** *[To be filled: e.g., Reviewing Jira Board Filter]*

### 3. Reporting Period Metadata
*   **Source:** [Manual Input]
*   **Description:** The specific date range the report covers.
*   **Required Fields:** Report Start Date, Report End Date.
*   **Acquisition Method:** *[To be filled: e.g., User input into a template]*

---

## ⚙️ Data Handling Notes

*   **Data Integrity Check:** Before proceeding to the Workflow phase, verify that all required fields listed above are present and non-null for every Objective.
*   **Versioning:** If the source data changes significantly between runs, note the version or date of the input file in the final report's metadata.