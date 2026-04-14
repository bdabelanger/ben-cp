# Implementation Plan: Establish Strategic PM Convention

> **Prepared by:** Antigravity (Gemini) (2026-04-10), updated Claude (Cowork) (2026-04-12)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2
> **v1.3**
> **STATUS: 🔲 READY — pick up 2026-04-10**

---

## Context

The **"product"** skill (officially named `product` in all skill references and paths) handles session-specific implementation planning and dependency tracking. It replaces the old habit of agents writing planning entries into the changelog upfront. The session planning artifact is an ephemeral `notes.md` file that lives only during active work, then gets deleted after the changelog entry is written.

> **Naming convention (enforced):**
> - The skill is named **"product"** — used in all skill calls, paths, and documentation.
> - "Quartermaster" is a character/report style name only — never used in skill references, file paths, or AGENTS.md rules.
> - Example: `mcp__ben-cp__get_skill("product")` — not `quartermaster`.

---

## Session Pattern (Plan → Work → Log → Delete)

1. At session start: create `notes.md` in the target skill directory using the template in `skills/product/report.md`
2. Work: use `notes.md` as the live scratchpad
3. At session end: write the changelog entry from `notes.md`
4. Delete `notes.md` **before** ending the session

---

## Execution Steps

1. **Verify Infrastructure** — Confirm `skills/product/index.md` and `AGENTS.md` contain the new rules. All references must use the name **"product"**.
2. **Rename artifact references** — Update `product/index.md` and `product/report.md` to reference `notes.md` consistently throughout (not any prior artifact name).
3. **Audit Check** — Run the changelog skill procedure (including Check 8) on a directory with a decoy `notes.md` to confirm it gets flagged.
4. **Cross-register with access audit** — Add lingering `notes.md` detection to the access audit procedure (Roz) as a secondary safety net. Two independent checks reduces risk of orphaned notes accumulating silently.
5. **Digest hook** — Note in `skills/dream/run.py` that lingering `notes.md` files at compile time should surface as a flag in the Digest output. This catches sessions that started work but didn't complete cleanup.
6. **Changelog + Completion** — Write changelog entries, then mark this file complete.

---

## Design Notes (for future MCP migration)

When this graduates to MCP-level, the natural shape is a session-scoped key/value store:
- `product.set(key, value)` / `product.get(key)` / `product.close()` — which auto-writes the changelog entry and self-destructs

The current file-based convention maps cleanly onto that future interface. Design the template fields with that migration in mind so they translate directly.

---

## Notes for This Agent
- The skill name is **"product"** — always. Character/report style names are never used in skill references.
- Always delete `notes.md` *after* the changelog is written but *before* ending the session.
- If `notes.md` is found lingering anywhere at session start: read it, incorporate any useful context into the changelog, then delete it before beginning new work.
