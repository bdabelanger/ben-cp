# Audit Procedure: Changelog

> **Owner:** Changelog Auditor (Yukon Cornelius)

## Requirements
- [ ] Log Alignment: Every modified file must have a corresponding changelog entry.
- [ ] Phantom Check: No log entries for files that do not exist in the physical tree.
- [ ] Chain Integrity: Skill-level logs must be linked correctly to the root ledger.

## Operating Procedures

### 1. Lumberjack Field Audit
1. **Saturation:** Read `changelog.md` (root) and active skill-level `changelog.md` files.
2. **Extraction:** Get the list of files claimed as "Completed" or "Modified."
3. **Validation:**
   - Use `ls` or `mcp_filesystem_directory_tree` to verify file existence.
   - Run `git log` (if applicable) to identify undocumented changes.
4. **Flagging:** Mark any discrepancies as "Ghost Tracks" (phantoms) or "Snowed In" (missing).

### 2. Manual Integrity Check
Verify that `write_changelog_entry` tool calls are using the correct relative paths and valid status enums (✅, 🟡, ⚠️).
