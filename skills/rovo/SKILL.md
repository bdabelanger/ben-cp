---
title: 'Skill: Atlassian Rovo SOP (CBP-XXXX)'
type: skill
domain: skills/rovo
---


# Skill: Atlassian Rovo SOP (CBP-XXXX)

**Objective:** To efficiently locate and gather comprehensive data on "CBP-XXXX" issues using available tools.

### 🔍 Investigation Workflow

1.  **The Great Hunt (Tool: searchAtlassian):** Initiate the investigation by calling `searchAtlassian`. **Crucially, structure your query to include both the issue key AND a relevant context keyword** (e.g., `"CBP-XXXX" "status_keyword"`). This maximizes discovery beyond simple URL matching.
    *   **🛑 Fallback:** If `searchAtlassian` returns zero results for a known issue, immediately escalate or verify the issue key's existence outside of Rovo tools.

2.  **Data Retrieval (Tool: getJiraIssue):** Once a standard URL is found via Step 1, use `getJiraIssue` with the precise ID/Key (`CBP-XXXX`) to pull core data (status, assignee, fields). This is your primary source of truth.

3.  **Link Exploration (Tool: getJiraIssueRemoteIssueLinks):** If available, execute this tool to map out related discussions or linked entities. Note that an empty list here is a common occurrence and does not indicate failure.

### 💡 Key Takeaways & Best Practices
*   `searchAtlassian` is your initial compass; always refine the query for precision.
*   `getJiraIssue` provides the bedrock data—treat its output as definitive context.
*   This streamlined process minimizes unnecessary tool calls, making investigations faster and less prone to guesswork when tackling "CBP-XXXX" issues.