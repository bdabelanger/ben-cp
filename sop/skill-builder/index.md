# Skill: Guide to Documenting Workflows (The Procedural Documentation Standard)

> [!IMPORTANT]
> 💡 **PURPOSE** — This document establishes the mandatory structure and level of detail required when creating a 'Skill' for any complex process, whether it is automated (a 'Pipeline') or manual (a 'Procedure'). The goal is to ensure that any future team member can understand, replicate, and maintain the entire procedure without needing tribal knowledge.

---

## 🧭 Overview: Modular Documentation Philosophy

We enforce a modular approach. Instead of one monolithic document, we treat documentation as a library of reusable components. A new Skill is assembled by referencing these standardized modules.

**When documenting a new Skill, you will assemble it using:**

*   `index.md`: The **Guide**. High-level overview and Table of Contents linking to all other modules.
*   `data_sources.md`: The **Inventory**. A detailed list of every external system or required manual input for the process.
*   `procedure.md`: The **Runbook & Flow**. Combines execution steps (manual actions) with the step-by-step data flow logic.
*   `styles/`: The **Visual Contract**. Contains reusable files defining presentation standards (e.g., `emoji_key.md`, `progress_bar_syntax.md`).
*   `mappings/`: The **Logic Engine**. Contains reusable files defining business constraints and transformation rules (e.g., `status_mapping.md`).
*   `changelog.md`: The **History**. Tracks all significant structural or content changes to this Skill suite.

---

## 🧱 Component Breakdown (What Each Module Covers)

### 1. Index.md (The Guide) - *This File*
*   **Focus:** The 'Why' and the high-level process flow. It serves as the entry point and Table of Contents for the entire Skill suite.
*   **Content Goal:** To orient the reader to the complexity and modularity of the documentation set.

### 2. Data Sources (`data_sources.md`)
*   **Focus:** The 'Inputs'. A comprehensive inventory of all external dependencies (e.g., Jira API, Manual Input Forms). 
*   **Content Goal:** To provide a single source of truth for required inputs and access methods.

### 3. Procedure (`procedure.md`)
*   **Focus:** The 'How'. This module details the sequence of actions.
    *   **Runbook Section:** Contains exact manual steps, decision points, and failure handling procedures (e.g., "If X happens, perform Y").
    *   **Mapping Section:** Details the step-by-step data journey: *Raw Data $\rightarrow$ Transformation Logic $\rightarrow$ Final State*. This is where status overrides are defined.

### 4. Styles (`styles/`) - *Reusable Assets*
*   **Focus:** The 'Contract'. Defines presentation standards for the final output artifact (e.g., how emojis should be used).
*   **Content Goal:** To ensure visual consistency across all reports by referencing standardized files.

### 5. Mappings (`mappings/`) - *Reusable Assets*
*   **Focus:** The 'Logic Engine'. Defines business constraints and transformation logic (e.g., mapping a status string to a Green/Yellow/Red state).
*   **Content Goal:** To ensure logical consistency across all reports.

---

## 🚀 Future Automation Note (For Review)

As we build these Skills, if a manual 'Procedure' becomes sufficiently stable and repeatable, the next step will be to convert it into an automated 'Pipeline'. When this conversion is complete, I will notify you with a draft of the new automated Skill for your review and approval before deployment.