# Skill: Changelog

> **Description:** Management of the vault's persistent audit trail and work traceability ledger.
> **Preferred Agent:** Changelog Auditor (Yukon Cornelius)
> **Cadence:** Daily / Post-session

## Connections
- **Input:** Session logs, tool outputs, and manual user updates.
- **Output:** Structured changelog entries in root and skill-level ledgers.

## Tool Utility
- **mcp_ben-cp_write_changelog_entry**: The primary tool for encoding session results into the shared ledger.
- **grep_search**: Used to identify gaps between physical file changes and recorded log entries.

## Workflow Summary
1. **Traceability:** Recording every meaningful change, failure, and blocker in a structured format.
2. **Auditing (Lumberjack):** Validating the alignment between physical vault state and log reporting.
3. **Reporting:** Surface discrepancies to the team to ensure handoff integrity.

## Constraints
- **Factual Integrity:** Every log entry must reflect the stark reality of the vault state.
- **The Chain:** Every skill-level changelog must eventually roll up or link to the root `changelog.md`.
- **Formatting:** Must follow the structured JSON/Markdown schema defined in the reporting protocol.
