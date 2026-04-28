---
title: 'Step 0: Jira Data Ingestion (Agent Guide)'
type: task
domain: skills/status/scripts
---


# Step 0: Jira Data Ingestion (Agent Guide)

This document provides instructions for LLMs/AI Agents on how to use the Atlassian Rovo MCP tools to populate the `inputs/raw/jira_issues.json` file.

## Protocol for Agents

### 1. Identify Target Keys
Load `inputs/processed/asana_active_YYYY_MM_DD.json` (or the equivalent file from Step 1).
- Extract all non-N/A values from the `"jira_link"` field.
- **Example Keys**: `CBP-3066`, `CBP-3121`, `CBP-2923`, etc.

### 2. Formulate JQL
Use a recursive hierarchy search to capture the Epic, its children, and its sub-tasks.
- **Draft JQL**:
  ```sql
  key in (EPIC_KEYS) OR parent in (EPIC_KEYS) OR parent.parent in (EPIC_KEYS)
  ```
- Replace `(EPIC_KEYS)` with the comma-separated keys identified in Step 1.

### 3. Fetch from Rovo
Call the `mcp_rovo_searchJiraIssuesUsingJql` tool:
- **cloudId**: `casecommons.atlassian.net`
- **jql**: The query formulated above.
- **maxResults**: 100+ (ensure you capture the full project scope).

### 4. Save to Raw
Write the resulting issues list to `skills/status/inputs/raw/jira_issues.json` in JSON format. Ensure the structure maintains the `{"key": ..., "fields": {...}}` pattern required by the harvest script.

---
> [!IMPORTANT]
> The `step_3_jira_harvest.py` script depends on the presence of a `parent` field in child issues to correctly associate them with the Epic. Do not skip the `parent in (...)` part of the JQL.
