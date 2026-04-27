---
Status: active
Priority: P3
Date: 2026-04-26
Owner: Ben
---
# Audit Procedure: Vault Audit

> **Owner:** Vault Auditor

## Global Structural Requirements (Watchdog)
- [ ] Orphaned Files: No files without index.md documentation or logical parent.
- [ ] Misplaced Files: All files must reside in their mapped skill or domain directories.
- [ ] Index Compliance: Every directory must contain an index.md.
- [ ] Duplicate Files: No redundant copies of documentation or logic stubs.
- [ ] Stale Flags: Status flags in `index.md` must match active OKR state.

## Operating Procedure

1. **Load Standard**: Reference `skills/memory/audit/structural_requirements.md` (if specialized) or the parent `memory/audit.md`.
2. **Scan Tree**: Execute a full recursive tree view of the target path.
3. **Validate**:
   - Check per-directory for `index.md`.
   - Grep for `status:` or `Agent:` to verify standard metadata presence.
4. **Log Violations**: Record every mismatch as a numbered flag.
