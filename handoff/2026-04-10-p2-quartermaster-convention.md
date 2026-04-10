# Any Agent Implementation Plan: Establish Quartermaster Convention

> **Prepared by:** Antigravity (Initial Concept, 2026-04-10)
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P2 — Process refinement
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-10**

---

## Context

We are spinning up a new concept called **"Quartermaster"** to handle session-specific implementation planning and dependency tracking. This replaces the previous habit of agents writing "planning" entries into the changelog upfront. Quartermaster files are ephemeral and should only exist during active work.

---

## Execution Order

1. **Verify Infrastructure** — Check `skills/quartermaster/index.md` and `AGENTS.md` for the new rules.
2. **First Load-Out** — In the next work-active session, create a `quartermaster.md` in the target skill directory using the template.
3. **Execution & Cleanup** — Follow the new Session Pattern in `AGENTS.md`: Plan → Work → Log → Delete Plan.
4. **Audit Verification** — Run `Lumberjack` to ensure it correctly flags any lingering `quartermaster.md` files as "Field Notes" for cleanup.

---

## Task 1: Verify Skill & Rules
Confirm the following files exist and match the intended convention:
- `skills/quartermaster/index.md`
- `skills/quartermaster/quartermaster_template.md`
- `AGENTS.md` (Check Step 3 and Step 6 of the Session Pattern)

---

## Task 2: Audit Check
Run the Lumberjack procedure (now including Check 8) on a directory with a decoy `quartermaster.md` to ensure it is flagged.

---

## Task 3: Changelog + Completion
Write changelog entries (subdirectory first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Quartermaster is intended to eventually become an MCP-level tool. For now, it is a manual documentation convention.
- Always delete the `quartermaster.md` file *after* the changelog is written but *before* ending the session.
