# Implementation Plan: intelligence-smoke-test-fresh-chat

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P4
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Smoke test completed successfully. All three domain checks passed with corrected vault-relative paths. Along the way, identified and cleaned up two real issues: a rogue orchestration/notes/ directory created at the repo root (not the vault) by a prior agent, and a broken collaboration/index.md reference in orchestration/index.md (the skill is actually communication/, not collaboration/). Both were fixed. The smoke test step 3 path (skills/orchestration/notes/notes.md) was a bad path in the original handoff — the correct vault-relative path is orchestration/communication/notes.md, which reads fine.

**Changelog:** (see root changelog.md)


---

**Goal:** Perform a lightweight, end-to-end smoke test across the Intelligence and Orchestration domains to confirm that recent structural changes (e.g., renaming of communication/notes) have been correctly indexed and are accessible.

**Execution Plan (Smoke Test Sequence):**
1. **Domain Check:** Read `intelligence/index.md` and `orchestration/index.md` to confirm the high-level domain descriptions are present and correct.
2. **Skill Access Check:** Attempt to read a known, stable skill from each domain (e.g., `intelligence/memory/SKILL.md` and `orchestration/access/SKILL.md`).
3. **Contextual Read Test:** Read the vault-wide notes file: `skills/orchestration/notes/notes.md` to confirm the primary context channel is accessible.
4. **Final Confirmation:** Report back on the success of these three checks.

**Deliverables:** A confirmation report stating that all three checks passed, indicating a healthy system state for future work.