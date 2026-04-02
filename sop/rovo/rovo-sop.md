## Atlassian Rovo - Standard Operating Procedures

Process for Identifying and Retrieving Information about a “CBP-XXXX” Issue:

Initial Search (Tool: searchAtlassian): Begin by using the searchAtlassian tool with a specific query (e.g., “CBP-XXXX”) to locate the issue within Confluence and Jira. This is crucial as it might not always be immediately obvious from a standard URL.

ARI Identification (Tool: getJiraIssue): If the initial search returns a standard URL, use the getJiraIssue tool with the issue ID or key (e.g., “CBP-XXXX”) to retrieve detailed information about the issue, including its status, assignee, and related fields.

Remote Link Check (Tool: getJiraIssueRemoteIssueLinks): If the issue has remote links, use the getJiraIssueRemoteIssueLinks tool to explore those connections and potentially uncover related issues or discussions.

No Remote Links - Deep Dive (Tool: getJiraIssue): If no remote links are found, rely on the information returned by getJiraIssue to understand the issue's context and any potential next steps.

Key Considerations:
* The searchAtlassian tool is vital for finding issues when a standard URL isn’t available.
* The getJiraIssue tool provides comprehensive information about the issue, including fields and relationships.
* The getJiraIssueRemoteIssueLinks tool is useful for discovering related issues, but it may return an empty list.
* This process should help streamline future investigations and reduce the need for repeated tool calls when dealing with “CBP-XXXX” issues.