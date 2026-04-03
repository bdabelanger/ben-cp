## Standard Operating Procedures

Atlassian Rovo - see /rovo/rovo-sop.md for full details:
*   **Finding CBP Issues:** Use `searchAtlassian` with the issue key (e.g., “CBP-XXXX”) to locate issues quickly.
*   **ARI Identification:** If a standard URL is not available, use `getJiraIssue` to retrieve detailed information using the ARI.
*   **Remote Links:** If no remote links are found, rely on `getJiraIssue` for comprehensive issue details.
*   **Jira Issue Link Types:** Use `getJiraIssueTypeMetaWithFields` to determine available link types.
*   **Jira Issue Transitions:** Use `getJiraIssue` to get available transitions for a given issue.
*   **Jira Search:** Use `searchAtlassian` with JQL queries for advanced searching.

---

# Atlassian Rovo SOP: Status Report Synthesis

## Integration Guidelines
When acting as part of the **Status Report Orchestrator**, use Rovo tools to provide qualitative context that Jira tickets alone cannot capture.

## Tooling Usage
* **Search Context:** Use `searchAtlassian` with project names found in Step 1 to locate high-level decisions in Confluence or Slack.
* **Sentiment Analysis:** Use `getJiraIssue` on "Anchor" issues or Epics to determine the current 'vibe' of the project.
* **Synthesis:** Group findings into a "Decisions & Context" block for each project to be consumed by the final report generator.