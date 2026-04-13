# Skill: Memory Store

> **Description:** Custodian of Intelligence and Structural Truth. Manages long-term mappings, active learning, and standardized retrieval.
> **Preferred Agent:** Vault Auditor (Senior Archivist)
> **Cadence:** Ongoing / Daily / Weekly (Audit)

## Connections
- **Input:** Session logs, user notes, and system observations across all domains.
- **Output:** Knowledge Items (KIs), updated mappings, and structural health reports.

## Tool Utility
- **mcp_filesystem_directory_tree**: Essential for structural hygiene and drift detection.
- **grep_search**: Used for historical auditing and cross-domain pattern matching.

## Workflow Summary
1. **Intake:** Encoding ephemeral session findings into persistent memory structures (KIs/Mappings) via `append_note`.
2. **Retrieval:** Standardized context injection and search via `read_notes`, `search_intelligence`, and `parse_intelligence`.
3. **Guardianship (Audit):** Continuous validation of vault hygiene via `audit_intelligence`.

## Constraints
- The mapping/ directory is the absolute Source of Truth.
- No inline mappings; all structural health logic must be centralized.
- Prioritizes "Inexorable Logic": A file is either compliant or a violation.
