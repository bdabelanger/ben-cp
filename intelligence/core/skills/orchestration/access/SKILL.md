# Skill: Access Audit

> **Description:** Permission and access auditor for the ben-cp vault. Synthesizes findings from the changelog skill's Check 9 scan and git logs to flag vault violations. Runs nightly or on demand.
> **Preferred Agent:** Claude (Cowork)
> **Cadence:** Daily

## Connections
- **Input:** `intelligence/core/skills/orchestration/changelog/` (Check 9 reports).
- **Output:** `intelligence/core/skills/orchestration/access/outputs/reports/` (Flagged reports), feeds into Dream Cycle.

## Tool Utility
- **git_log**: Used to cross-reference agent file touches against authorized boundaries in `AGENTS.md`.
- **filesystem**: Used to perform the Supply Chain Audit and Resource Bloat checks.

## Workflow Summary
1. **Discovery:** Synthesis of findings from the changelog skill's field scans.
2. **Analysis:** Constructing violation narratives based on `AGENTS.md` compliance.
3. **Communication:** Producing a flagged report or delegated investigation (P3 handoff).

## Constraints
- Read before every write — no exceptions.
- Never delete, move, or modify vault files (produces flags only).
- Use absolute paths starting with `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/`.
