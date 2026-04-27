# Implementation Plan: 2026-04-27-p3-sanction-system-directories-and-update-drift-allowlist

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-27

---

# Context
The `drift` sensor flagged several root-level directories as "unsanctioned":
- `dist/`: Build output.
- `node_modules/`: npm dependencies.
- `src/`: Vault source code (Code domain).
- `reports/`: Nightly sensor outputs.

These are intentional system directories and should be allowlisted to prevent false positives in health reports.

# Logic
1. **allowlist (Ignore)**: `dist/` and `node_modules/` should be ignored by the drift sensor as they are ephemeral or external dependencies.
2. **Sanction (Structure)**: `src/` and `reports/` should be added to the sanctioned **Vault Structure** in `AGENTS.md` as they are core parts of the vault's operation.
3. **Sensor Sync**: Ensure `skills/dream/scripts/drift.py` reflects these changes.

# Execution Steps
- [ ] Update `AGENTS.md` Vault Structure tree to include `src/` and `reports/`.
- [ ] Ensure `dist/` and `node_modules/` are in the `IGNORE_DIRS` list in `skills/dream/scripts/drift.py`.
- [ ] Run `generate_report(skill='dream')` and verify `drift` sensor report shows 0 findings for these directories.
