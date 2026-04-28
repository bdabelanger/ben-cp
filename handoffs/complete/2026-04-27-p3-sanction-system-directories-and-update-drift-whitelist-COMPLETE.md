# Implementation Plan: 2026-04-27-p3-sanction-system-directories-and-update-drift-allowlist

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-28

Sanctioned src/ and reports/ in AGENTS.md and updated drift.py to allowlist them while ignoring ephemeral build/node dirs. Drift sensor now reports 'clean'.

---

# Context
The `drift` sensor flagged several root-level directories as "unsanctioned":
- `dist/`: Build output.
- `node_modules/`: npm dependencies.
- `src/`: Repo source code (Code domain).
- `reports/`: Nightly sensor outputs.

These are intentional system directories and should be allowlisted to prevent false positives in health reports.

# Logic
1. **allowlist (Ignore)**: `dist/` and `node_modules/` should be ignored by the drift sensor as they are ephemeral or external dependencies.
2. **Sanction (Structure)**: `src/` and `reports/` should be added to the sanctioned **Repo Structure** in `AGENTS.md` as they are core parts of the repo's operation.
3. **Sensor Sync**: Ensure `skills/dream/scripts/drift.py` reflects these changes.

# Execution Steps
- [ ] Update `AGENTS.md` Repo Structure tree to include `src/` and `reports/`.
- [ ] Ensure `dist/` and `node_modules/` are in the `IGNORE_DIRS` list in `skills/dream/scripts/drift.py`.
- [ ] Run `generate_report(skill='dream')` and verify `drift` sensor report shows 0 findings for these directories.
