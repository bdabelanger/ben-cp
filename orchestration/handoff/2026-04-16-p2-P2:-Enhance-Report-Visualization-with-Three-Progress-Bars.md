While investigating the JIRA data accuracy issue, please also implement enhancements to the report visualization for better usability and clarity.

**Goal:** Standardize and enhance the progress bar display per project by implementing three distinct bars.

**Bar Specifications (Order: 1st, 2nd, 3rd):**

1. **Status Bar (PRESERVE EXISTING LOGIC):**
    - **Source Data:** Jira issue status category.
    - **Grain:** Count of work items.
    - **Purpose:** Indicates general forward movement of work. **(This bar should remain functionally unchanged from the current implementation.)**

2. **Readiness Bar (NEW - Positioned 2nd):**
    - **Source Data:** The existing 'Readiness' table data.
    - **Grain:** Count of work items.
    - **Visualization Rules:** Must be a progress bar with specific color coding:
        - Done stories: Green
        - On track: Blue
        - At Risk: Yellow
        - Off Track: Red
        - Not Set: Gray

3. **Estimate Bar (Positioned 3rd):**
    - **Source Data:** Actual vs. Project Estimate.
    - **Grain:** Count of days.
    - **Purpose:** Indicates budget/timeline adherence. **(This bar should remain functionally unchanged from the current implementation.)**

**Documentation Note:** Please ensure the grain for each chart is explicitly documented alongside its visualization to maintain consistency in future report generation.