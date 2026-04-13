# Any Agent Implementation Plan: Establish Strategic PM Convention

> **Prepared by:** Antigravity (Initial Concept, 2026-04-10)
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P2 — Process refinement
> **v1.3**
> **STATUS: 🔲 READY — pick up 2026-04-10**

---

## Context

We are spinning up a new concept called **"Strategic PM"** to handle session-specific implementation planning and dependency tracking. This replaces the previous habit of agents writing "planning" entries into the changelog upfront. The session planning artifact is an ephemeral `notes.md` file that should only exist during active work.

> **Naming convention (enforced):**
> - The skill is named **"product"** — this is the official skill reference name used in all skill calls, paths, and documentation.
> - "Quartermaster" is a character/report style name only — used in narrative or Digest context, never in skill references, file paths, or AGENTS.md rules.
> - Example: `mcp__ben-cp__get_skill("product")` — not `quartermaster`.

---

## The Claude Perspective
> **Injected by:** Claude (Cowork) (2026-04-12)

This convention is clean and worth enforcing strictly. A few observations:

**On the ephemeral lifecycle:**
The Plan → Work → Log → Delete pattern is sound, but the deletion step is the most failure-prone — sessions can end unexpectedly (timeout, crash, user closes app). I'd recommend the access audit procedure (Roz) also checks for lingering `notes.md` files as a secondary safety net, not just the changelog skill. Two independent checks reduces the risk of orphaned field notes accumulating silently.

**On Strategic PM as future MCP tool:**
When this graduates to MCP-level, the natural shape is a session-scoped key/value store: `product.set(key, value)` / `product.get(key)` / `product.close()` (which auto-writes the changelog entry and self-destructs). The current file-based convention maps cleanly onto that future interface — worth designing the template with that migration in mind so the fields translate directly.

**On the Digest integration:**
Once Digest Editor's daily cycle is running, lingering `notes.md` files at Digest compile time could be a useful signal — they indicate a session that started work but didn't complete its cleanup. Digest Editor should surface these as a flag in the Digest rather than silently ignoring them.

**On naming:**
The session planning artifact is named `notes.md`. The skill is officially named **"product"**. Character/report style names (e.g., "Quartermaster") are never used in skill references.

---

## Execution Order

1. **Verify Infrastructure** — Check `skills/product/index.md` and `AGENTS.md` for the new rules.
2. **Rename artifact** — Update `product/index.md` and `product/report.md` to reference `notes.md` instead of any prior artifact name throughout.
3. **First Load-Out** — In the next work-active session, create a `notes.md` in the target skill directory using the template.
4. **Execution & Cleanup** — Follow the new Session Pattern in `AGENTS.md`: Plan → Work → Log → Delete Plan.
5. **Audit Verification** — Run the changelog skill audit (including Check 8) on a directory with a decoy `notes.md` to ensure it is flagged.
6. **Cross-register with access audit** — Add lingering `notes.md` detection to the access audit procedure as a secondary safety net.
7. **Digest hook** — Note in `skills/dream/run.py` that lingering `notes.md` files at compile time should surface as a flag in the Digest output.

---

## Task 1: Verify Skill & Rules
Confirm the following files exist and match the intended convention:
- `skills/product/index.md`
- `skills/product/report.md`
- `AGENTS.md` (Check Step 3 and Step 6 of the Session Pattern)

All references to the skill should use the name **"product"**. Character names are never used in skill references or paths.

---

## Task 2: Audit Check
Run the changelog skill procedure (now including Check 8) on a directory with a decoy `notes.md` to ensure it is flagged.

---

## Task 3: Changelog + Completion
Write changelog entries (subdirectory first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- The skill name is **"product"** — always use this in skill references, paths, and AGENTS.md. "Quartermaster" is a character/report style name only.
- Strategic PM is intended to eventually become an MCP-level tool. Design the template fields with that future interface in mind (`product.set` / `product.get` / `product.close`).
- Always delete the `notes.md` file *after* the changelog is written but *before* ending the session.
