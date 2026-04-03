## Standard Operating Procedures

Atlassian Rovo - see /rovo/rovo-sop.md for full details:
*   **Finding CBP Issues:** Use `searchAtlassian` with the issue key (e.g., “CBP-XXXX”) to locate issues quickly.
*   **ARI Identification:** If a standard URL is not available, use `getJiraIssue` to retrieve detailed information using the ARI.
*   **Remote Links:** If no remote links are found, rely on `getJiraIssue` for comprehensive issue details.
*   **Jira Issue Link Types:** Use `getJiraIssueTypeMetaWithFields` to determine available link types.
*   **Jira Issue Transitions:** Use `getJiraIssue` to get available transitions for a given issue.
*   **Jira Search:** Use `searchAtlassian` with JQL queries for advanced searching.