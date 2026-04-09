# Claude Code Implementation Plan: Agent 'Robert' Creation

> **Prepared by:** Gemma (Executor) (Context Audit, 2026-04-10)
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P1 — Establishing a self-monitoring layer for core documentation integrity.
> **Source Report:** Internal Mission Alignment Review (AGENTS.md Creed).
> **v1.0**
> **STATUS: READY — pick up 2026-04-10**

---

## Context & Goal
We have established a core mission statement in `AGENTS.md` (The Agent's Creed). To ensure this living documentation remains accurate and reflects the vault's actual evolution, we need an automated observer: **Robert**.

Robert will monitor Git diffs against the current state of `AGENTS.md` to flag any structural or philosophical drift.

---

## Proposed Architecture (For Claude Code Implementation)
1.  **Agent:** Create a new agent file: `agents/robert.md`. This defines his role, mission, and reporting structure.
2.  **Skill:** Create a new skill directory: `skills/robert/`. Inside, create the core logic file: `skills/robert/diff_checker.md`. This skill will contain the procedure to:
    a. Fetch recent Git diffs (requires shell access).
    b. Parse the diff against the current content of `AGENTS.md`.
    c. Compare changes against the 'Agent's Creed' principles.
3.  **Integration:** Update `AGENTS.md` to list Robert in the Agent Dispatch table and update the Handoff Check procedure if necessary.

---

## Task Breakdown for Claude Code
1. **Implement `agents/robert.md`:** Define his role as 'Mission Integrity Observer'.
2. **Implement `skills/robert/diff_checker.md`:** Write the procedural logic, focusing on how to safely access and parse Git history within the vault environment.
3. **Update Vault Contracts:** Modify `AGENTS.md` and potentially `skills/index.md` to include Robert's presence.
4. **Test & Report:** Run a test cycle against recent changes (e.g., the Creed update) and report findings on the implementation success.

---

## Dependencies & Constraints
*   **Tooling:** This requires robust shell/Git interaction capabilities, which should be available to Claude Code.
*   **Scope:** Robert's initial scope is strictly limited to monitoring `AGENTS.md` integrity against the Creed.

---

## Next Steps for Gemma (Executor)
Once Robert is implemented and tested, I will update the root changelog to reflect this major architectural addition.