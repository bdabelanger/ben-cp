---
Status: active
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Skill: Vault Audit

> **Description:** Instruction-driven structural auditing and hygiene validation.
> **Preferred Agent:** Vault Auditor
> **Cadence:** Weekly / On-demand per skill audit requirement

## Connections
- **Input:** Target skill/domain path and its specific `audit.md` requirements.
- **Output:** Centralized hygiene reports and violation flags in `outputs/`.

## Tool Utility
- **mcp_filesystem_directory_tree**: Mapping the physical state of the vault.
- **list_dir**: Granular inspection of directory compliance (e.g., checking for index.md).

## Workflow Summary
1. **Targeting:** Identifying the domain or specific skill set for auditing.
2. **Requirements Loading:** Reading the `audit.md` file of the target domain.
3. **Validation:** Executing the procedural checks against live vault state.
4. **Reporting:** Surface findings in a standardized hygiene manifest.

## Constraints
- Does not fix errors; only identifies and flags them.
- All reports must be written to the root `outputs/memory/audit/` tree.
